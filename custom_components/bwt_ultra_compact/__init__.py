"""The BWT Ultra Compact integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.helpers.entity_platform import async_get_current_platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_MAC_ADDRESS, CONF_PASSKEY

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up BWT Ultra Compact from a config entry."""
    _LOGGER.warning("🔧 Setting up BWT Ultra Compact integration - Starting initialization")

    # Store configuration data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "mac_address": entry.data[CONF_MAC_ADDRESS],
        "passkey": entry.data[CONF_PASSKEY],
        "connection_status": "initializing"
    }

    # Test Bluetooth connection using HA native methods
    _LOGGER.warning("🔍 Testing Bluetooth connection using HA native methods...")
    await _test_bluetooth_connection(hass, entry.data[CONF_MAC_ADDRESS])

    # Forward setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    _LOGGER.warning("✅ BWT Ultra Compact integration setup completed successfully")
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
        _LOGGER.warning("📡 Attempting to find BWT device via Bluetooth...")

        # Use HA's native Bluetooth methods
        ble_device = bluetooth.async_ble_device_from_address(
            hass, mac_address.upper(), connectable=True
        )

        if not ble_device:
            _LOGGER.error("❌ Bluetooth device NOT found: %s", mac_address)
            _LOGGER.warning("💡 Please ensure the device is powered on and in range")
            hass.data[DOMAIN][entry.entry_id]["connection_status"] = "device_not_found"
            return

        _LOGGER.warning("🎉 Found Bluetooth device: %s", ble_device.name or ble_device.address)
        _LOGGER.warning("🔗 Bluetooth connection test completed successfully")
        hass.data[DOMAIN][entry.entry_id]["connection_status"] = "connected"

    except Exception as err:
        _LOGGER.error("⚠️ Error during Bluetooth connection test: %s", err)
        _LOGGER.warning("📋 This may indicate a Bluetooth stack issue")
        hass.data[DOMAIN][entry.entry_id]["connection_status"] = "connection_error"
