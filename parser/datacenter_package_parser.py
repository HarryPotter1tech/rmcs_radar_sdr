from typing import Union
from dataclasses import dataclass, field


@dataclass
class RadarMessageAutoDecisionSynchronization:
    cmd_id: int = 0x020E
    EncryptionRank: int = 1
    IsModifierKeyAble: bool = False


@dataclass
class RadarInfo:
    radar_message_auto_decision_synchronization: RadarMessageAutoDecisionSynchronization = field(
        default_factory=RadarMessageAutoDecisionSynchronization
    )


PackageParseResult = Union[RadarInfo, None]


class DataCenterPackageParser:
    def __init__(self):
        self.message_package: bytes = b""

    def package_parse(self, input_data: bytes) -> PackageParseResult:
        self.message_package = input_data
        if self.message_package is None or len(self.message_package) < 4:
            return None
        for i in range(0, len(self.message_package) - 3):
            cmd_id = int.from_bytes(self.message_package[i : i + 2], byteorder="big")
            if cmd_id != 0x020E:
                continue
            encryption_rank = self.message_package[i + 2]
            is_modifier_key_able = bool(self.message_package[i + 3] & 0x01)
            radar_message_autodecision_synchronization = (
                RadarMessageAutoDecisionSynchronization(
                    EncryptionRank=encryption_rank,
                    IsModifierKeyAble=is_modifier_key_able,
                )
            )
            return RadarInfo(
                radar_message_auto_decision_synchronization=radar_message_autodecision_synchronization,
            )
        return None
