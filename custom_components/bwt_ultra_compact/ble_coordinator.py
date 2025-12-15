"""Bluetooth coordinator for BWT Ultra Compact."""
from __future__ import annotations

import logging
import asyncio
from typing import Optional

from bleak import BleakClient, BleakError
from bleak.backends.device import BLEDevice

from .const import (
    BLE_SERVICE_UUID,
    BLE_BROADCAST_CHARACTERISTIC_UUID,
    CONF_MAC_ADDRESS,
    CONF_PASSKEY,
)

_LOGGER = logging.getLogger(__name__)

class BWTCoordinator:
    """Class to manage the BWT Bluetooth connection."""

    def __init__(self, hass, mac_address: str, passkey: str):
        """Initialize the coordinator."""
        self.hass = hass
        self.mac_address = mac_address
        self.passkey = passkey
        self._client: Optional[BleakClient] = None
        self._device: Optional[BLEDevice] = None
        self._is_connected = False

    async def connect(self) -> bool:
        """Connect to the BWT device using HA Bluetooth stack."""
        _LOGGER.info("Attempting to connect to BWT device: %s", self.mac_address)

        try:
            # Use HA's Bluetooth manager to get the device
            from homeassistant.components import bluetooth
            ble_device = bluetooth.async_ble_device_from_address(
                self.hass, self.mac_address.upper(), connectable=True
            )

            if not ble_device:
                _LOGGER.error("Bluetooth device not found: %s", self.mac_address)
                return False

            _LOGGER.debug("Found Bluetooth device: %s", ble_device.name or ble_device.address)

            # Create client using HA's Bluetooth stack
            self._client = BleakClient(
                ble_device,
                timeout=30.0,
                disconnected_callback=self._handle_disconnect
            )

            _LOGGER.debug("Connecting to device...")
            await self._client.connect()

            # Note: HA's BleakClientWrapper doesn't support discover_services()
            # Services are automatically discovered by HA's Bluetooth stack
            _LOGGER.debug("Connection established successfully")

            self._is_connected = True
            _LOGGER.info("Successfully connected to BWT device: %s", self.mac_address)

            return True

        except BleakError as err:
            _LOGGER.error("Failed to connect to BWT device: %s", err)
            await self.disconnect()
            return False

        except Exception as err:
            _LOGGER.exception("Unexpected error during connection: %s", err)
            await self.disconnect()
            return False

    async def disconnect(self) -> None:
        """Disconnect from the BWT device."""
        if self._client and self._is_connected:
            _LOGGER.info("Disconnecting from BWT device: %s", self.mac_address)
            try:
                await self._client.disconnect()
                self._is_connected = False
                _LOGGER.debug("Successfully disconnected")
            except Exception as err:
                _LOGGER.error("Error during disconnection: %s", err)
        self._client = None

    def _handle_disconnect(self, client: BleakClient) -> None:
        """Handle unexpected disconnections."""
        _LOGGER.warning("Unexpected disconnection from BWT device: %s", self.mac_address)
        self._is_connected = False
        self._client = None

    @property
    def is_connected(self) -> bool:
        """Return connection status."""
        return self._is_connected

    async def test_connection(self) -> bool:
        """Test the connection by reading a characteristic."""
        if not self._client or not self._is_connected:
            _LOGGER.error("Cannot test connection: not connected")
            return False

        try:
            _LOGGER.debug("Testing connection by reading broadcast characteristic...")
            # Try to read the broadcast characteristic
            data = await self._client.read_gatt_char(BLE_BROADCAST_CHARACTERISTIC_UUID)
            _LOGGER.info("Connection test successful, received data: %s", data.hex())
            return True

        except BleakError as err:
            _LOGGER.error("Connection test failed: %s", err)
            return False

        except Exception as err:
            _LOGGER.exception("Unexpected error during connection test: %s", err)
            return False
