"""Decoding of the BWT 'Perla Blue' state packet (independent of Home Assistant)."""
from __future__ import annotations

from dataclasses import dataclass


class BwtDecodeError(Exception):
    """The packet is not a valid state packet."""


@dataclass(frozen=True)
class BwtState:
    """Decoded content of characteristic F2E3."""

    salt_grams: int
    capacity_grams: int
    regenerations: int
    quarter_hours_idx: int
    days_idx: int
    alarm: bool

    @property
    def salt_percent(self) -> float:
        """Salt level in %, clamped to 0-100 (the device accepts levels above capacity)."""
        return max(0.0, min(100.0, 100 * self.salt_grams / self.capacity_grams))


def _word(data: bytes, i: int) -> int:
    """Little-endian 16-bit integer."""
    return data[i] | (data[i + 1] << 8)


def parse_state(data: bytes) -> BwtState:
    """Decode the state packet. Raise BwtDecodeError instead of guessing."""
    if len(data) < 15:
        raise BwtDecodeError(f"state packet too short: {len(data)} bytes")
    capacity = _word(data, 10) * 1000
    if capacity <= 0:
        raise BwtDecodeError("invalid capacity in state packet")
    return BwtState(
        salt_grams=_word(data, 0) + _word(data, 2) * 65536,
        capacity_grams=capacity,
        regenerations=_word(data, 8),
        quarter_hours_idx=_word(data, 4),
        days_idx=_word(data, 6),
        alarm=bool(data[12] & 1),
    )
