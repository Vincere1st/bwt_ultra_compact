"""Bluetooth access to the softener (uses Home Assistant's Bluetooth stack)."""
from __future__ import annotations

import contextlib

from bleak import BleakError
from bleak_retry_connector import BleakClientWithServiceCache, establish_connection

from homeassistant.components import bluetooth
from homeassistant.core import HomeAssistant

from .client import BwtDecodeError, BwtState, parse_state
from .const import CHAR_STATE


class BwtConnectionError(Exception):
    """The softener could not be reached or read."""


async def async_read_state(hass: HomeAssistant, address: str) -> BwtState:
    """Connect, read the state characteristic, disconnect."""

    def _device():
        return bluetooth.async_ble_device_from_address(hass, address, connectable=True)

    ble_device = _device()
    if ble_device is None:
        raise BwtConnectionError("device not in range of any Bluetooth adapter/proxy")
    try:
        client = await establish_connection(
            BleakClientWithServiceCache,
            ble_device,
            ble_device.name or address,
            max_attempts=3,
            ble_device_callback=_device,
        )
    except (BleakError, TimeoutError) as err:
        raise BwtConnectionError(f"connection failed: {err}") from err
    try:
        data = await client.read_gatt_char(CHAR_STATE)
    except (BleakError, TimeoutError) as err:
        raise BwtConnectionError(f"read failed: {err}") from err
    finally:
        with contextlib.suppress(BleakError, TimeoutError):
            await client.disconnect()
    try:
        return parse_state(bytes(data))
    except BwtDecodeError as err:
        raise BwtConnectionError(str(err)) from err
