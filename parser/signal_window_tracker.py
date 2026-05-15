from dataclasses import dataclass


@dataclass
class SignalTrackResult:
    value: bytes | None


class SignalWindowTracker:
    def __init__(self, window_size: int = 20):
        self.window_size = window_size
        self.values: list[bytes] = []
        self.counts: list[int] = []
        self.sample_count = 0

    def track(self, value: bytes) -> SignalTrackResult:
        self._add_to_window(value)
        if self.sample_count < self.window_size:
            return SignalTrackResult(None)
        result = self._pick_value()
        return SignalTrackResult(result)

    def _add_to_window(self, value: bytes) -> None:
        self.sample_count += 1
        try:
            index = self.values.index(value)
        except ValueError:
            self.values.append(value)
            self.counts.append(1)
        else:
            self.counts[index] += 1

    def _pick_value(self) -> bytes | None:
        if not self.values:
            self._reset_window()
            return None
        max_index = max(range(len(self.counts)), key=self.counts.__getitem__)
        result = self.values[max_index]
        self._reset_window()
        return result

    def _reset_window(self) -> None:
        self.values = []
        self.counts = []
        self.sample_count = 0
