"""The BWT Ultra Compact integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_MAC_ADDRESS, CONF_PASSKEY
from .ble_coordinator import BWTCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = []

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up BWT Ultra Compact from a config entry."""
    _LOGGER.info("Setting up BWT Ultra Compact integration")

    # Initialize coordinator
    coordinator = BWTCoordinator(
        hass,
        entry.data[CONF_MAC_ADDRESS],
        entry.data[CONF_PASSKEY]
    )

    # Store coordinator in hass.data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "mac_address": entry.data[CONF_MAC_ADDRESS],
        "passkey": entry.data[CONF_PASSKEY]
    }

    # Test connection
    _LOGGER.info("Testing Bluetooth connection...")
    connection_success = await coordinator.connect()

    if connection_success:
        _LOGGER.info("Bluetooth connection established successfully")
        # Test the connection by reading data
        test_success = await coordinator.test_connection()
        if test_success:
            _LOGGER.info("Connection test passed - device is responsive")
        else:
            _LOGGER.warning("Connection test failed - device may not be responsive")
    else:
        _LOGGER.error("Failed to establish Bluetooth connection")

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
        # Disconnect coordinator if connected
        coordinator = hass.data[DOMAIN][entry.entry_id].get("coordinator")
        if coordinator and coordinator.is_connected:
            await coordinator.disconnect()
        hass.data[DOMAIN].pop(entry.entry_id)
    return True
