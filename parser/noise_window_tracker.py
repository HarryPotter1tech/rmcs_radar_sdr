from dataclasses import dataclass


@dataclass
class NoiseTrackResult:
    real_key: tuple[int, int, int, int, int, int] | None
    updated: bool
    has_three_keys: bool


class NoiseKeyWindowTracker:
    def __init__(self, window_size: int = 20):
        self.window_size = window_size
        self.values: list[tuple[int, int, int, int, int, int]] = []
        self.counts: list[int] = []
        self.sample_count = 0
        self.real_key: tuple[int, int, int, int, int, int] | None = None
        self.real_key_history: list[tuple[int, int, int, int, int, int]] = []

    def track(self, value: tuple[int, int, int, int, int, int]) -> NoiseTrackResult:
        self._add_to_window(value)
        if self.sample_count < self.window_size:
            return NoiseTrackResult(None, False, self._has_three_keys())

        real_key = self._pick_real_key()
        updated = False
        if real_key is not None:
            updated = self._update_real_key(real_key)
        return NoiseTrackResult(real_key, updated, self._has_three_keys())

    def _add_to_window(self, value: tuple[int, int, int, int, int, int]) -> None:
        self.sample_count += 1
        try:
            index = self.values.index(value)
        except ValueError:
            self.values.append(value)
            self.counts.append(1)
        else:
            self.counts[index] += 1

    def _pick_real_key(self) -> tuple[int, int, int, int, int, int] | None:
        if not self.values:
            self._reset_window()
            return None
        max_index = max(range(len(self.counts)), key=self.counts.__getitem__)
        result = self.values[max_index]
        self._reset_window()
        return result

    def _update_real_key(self, real_key: tuple[int, int, int, int, int, int]) -> bool:
        if self.real_key == real_key:
            return False
        self.real_key = real_key
        if real_key not in self.real_key_history:
            self.real_key_history.append(real_key)
        return True

    def _has_three_keys(self) -> bool:
        return len(self.real_key_history) >= 3

    def _reset_window(self) -> None:
        self.values = []
        self.counts = []
        self.sample_count = 0
