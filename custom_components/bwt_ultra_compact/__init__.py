"""The BWT Ultra Compact integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_MAC_ADDRESS, CONF_PASSKEY

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = []

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up BWT Ultra Compact from a config entry."""
    _LOGGER.info("Setting up BWT Ultra Compact integration")

    # Store configuration data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "mac_address": entry.data[CONF_MAC_ADDRESS],
        "passkey": entry.data[CONF_PASSKEY]
    }

    # Test Bluetooth connection using HA native methods
    _LOGGER.info("Testing Bluetooth connection using HA native methods...")
    await _test_bluetooth_connection(hass, entry.data[CONF_MAC_ADDRESS])

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN].pop(entry.entry_id)
    return True

async def _test_bluetooth_connection(hass, mac_address: str) -> None:
    """Test Bluetooth connection using HA native methods."""
    try:
        from homeassistant.components import bluetooth
        _LOGGER.debug("Using HA Bluetooth stack to find device...")

        # Use HA's native Bluetooth methods
        ble_device = bluetooth.async_ble_device_from_address(
            hass, mac_address.upper(), connectable=True
        )

        if not ble_device:
            _LOGGER.error("Bluetooth device not found: %s", mac_address)
            return

        _LOGGER.info("Found Bluetooth device: %s", ble_device.name or ble_device.address)
        _LOGGER.info("Bluetooth connection test completed successfully")

    except Exception as err:
        _LOGGER.exception("Error during Bluetooth connection test: %s", err)
