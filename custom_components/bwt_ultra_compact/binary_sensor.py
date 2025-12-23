"""Binary sensor platform for BWT Ultra Compact integration."""
from __future__ import annotations

import logging

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the BWT Ultra Compact binary sensors."""
    _LOGGER.warning("🔄 Setting up BWT Ultra Compact binary sensors")

    # Create connection status sensor
    connection_sensor = BWTConnectionSensor(hass, entry)
    async_add_entities([connection_sensor])

    _LOGGER.warning("✅ BWT Ultra Compact binary sensors setup completed")

class BWTConnectionSensor(BinarySensorEntity):
    """Representation of a BWT Ultra Compact connection status sensor."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the connection sensor."""
        self.hass = hass
        self._entry = entry
        self._attr_name = f"BWT Ultra Compact Connection"
        self._attr_unique_id = f"bwt_ultra_compact_connection_{entry.entry_id}"
        self._attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
        self._attr_is_on = False  # Default to disconnected

        # Get initial connection status from stored data
        if DOMAIN in hass.data:
            entry_data = hass.data[DOMAIN].get(entry.entry_id, {})
            self._update_connection_status(entry_data.get("connection_status", "initializing"))

    def _update_connection_status(self, status: str) -> None:
        """Update the connection status."""
        if status == "connected":
            self._attr_is_on = True
            self._attr_icon = "mdi:bluetooth-connect"
        elif status == "device_not_found":
            self._attr_is_on = False
            self._attr_icon = "mdi:bluetooth-off"
        elif status == "connection_error":
            self._attr_is_on = False
            self._attr_icon = "mdi:bluetooth-alert"
        else:  # initializing or unknown
            self._attr_is_on = False
            self._attr_icon = "mdi:bluetooth-searching"

    async def async_update(self) -> None:
        """Update the connection status."""
        if DOMAIN in self.hass.data:
            entry_data = self.hass.data[DOMAIN].get(self._entry.entry_id, {})
            current_status = entry_data.get("connection_status", "initializing")

            _LOGGER.debug("Updating BWT connection sensor - status: %s", current_status)
            self._update_connection_status(current_status)

            if current_status == "connected":
                _LOGGER.warning("🔵 BWT Connection Sensor: Device CONNECTED")
            elif current_status == "device_not_found":
                _LOGGER.warning("🔴 BWT Connection Sensor: Device NOT FOUND")
            else:
                _LOGGER.warning("🟡 BWT Connection Sensor: Status - %s", current_status)

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return additional state attributes."""
        if DOMAIN in self.hass.data:
            entry_data = self.hass.data[DOMAIN].get(self._entry.entry_id, {})
            return {
                "mac_address": entry_data.get("mac_address", "unknown"),
                "status": entry_data.get("connection_status", "unknown"),
                "friendly_name": self._attr_name
            }
        return {"status": "initializing"}

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return True
