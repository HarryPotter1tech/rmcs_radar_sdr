from typing import Union
from dataclasses import dataclass


@dataclass
class RadarMarkProcess:
    cmd_id: int = 0x020C
    IsOpponentHeroDebuffed: bool = False
    IsOpponentEngineerDebuffed: bool = False
    IsOpponentInfantry3Debuffed: bool = False
    IsOpponentInfantry4Debuffed: bool = False
    IsOpponentAerialMarked: bool = False
    IsOpponentSentryDebuffed: bool = False
    IsAllyHeroMarked: bool = False
    IsAllyEngineerMarked: bool = False
    IsAllyInfantry3Marked: bool = False
    IsAllyInfantry4Marked: bool = False
    IsAllyAerialMarked: bool = False
    IsAllySentryMarked: bool = False


@dataclass
class RadarMessageAutoDecisionSynchronization:
    cmd_id: int = 0x020E
    EncryptionRank: int = 1
    IsModifierKeyAble: bool = False


@dataclass
class RadarInfo:
    radar_mark_process: RadarMarkProcess
    radar_message_auto_decision_synchronization: RadarMessageAutoDecisionSynchronization


PackageParseResult = Union[RadarInfo, None]


class DataCenterPackageParser:
    def __init__(self):
        self.message_package: bytes = b""

    def package_parse(self, input_data: bytes) -> PackageParseResult:
        self.message_package = input_data
        if self.message_package is None or len(self.message_package) < 12:
            return None
        radar_markerprocess = RadarMarkProcess()
        radar_message_autodecision_synchronization = (
            RadarMessageAutoDecisionSynchronization()
        )
        for i in range(0, len(self.message_package), 1):
            cmd_id = int.from_bytes(self.message_package[i : i + 2], byteorder="big")
            if cmd_id == radar_markerprocess.cmd_id:
                radar_markerprocess = RadarMarkProcess(
                    IsOpponentHeroDebuffed=bool(self.message_package[0] & 0x01),
                    IsOpponentEngineerDebuffed=bool(self.message_package[0] & 0x02),
                    IsOpponentInfantry3Debuffed=bool(self.message_package[0] & 0x04),
                    IsOpponentInfantry4Debuffed=bool(self.message_package[0] & 0x08),
                    IsOpponentAerialMarked=bool(self.message_package[0] & 0x10),
                    IsOpponentSentryDebuffed=bool(self.message_package[0] & 0x20),
                    IsAllyHeroMarked=bool(self.message_package[1] & 0x01),
                    IsAllyEngineerMarked=bool(self.message_package[1] & 0x02),
                    IsAllyInfantry3Marked=bool(self.message_package[1] & 0x04),
                    IsAllyInfantry4Marked=bool(self.message_package[1] & 0x08),
                    IsAllyAerialMarked=bool(self.message_package[1] & 0x10),
                    IsAllySentryMarked=bool(self.message_package[1] & 0x20),
                )
            elif cmd_id == radar_message_autodecision_synchronization.cmd_id:
                radar_message_autodecision_synchronization = (
                    RadarMessageAutoDecisionSynchronization(
                        EncryptionRank=self.message_package[0],
                        IsModifierKeyAble=bool(self.message_package[1] & 0x01),
                    )
                )
            else:
                return None
        return RadarInfo(
            radar_mark_process=radar_markerprocess,
            radar_message_auto_decision_synchronization=radar_message_autodecision_synchronization,
        )
