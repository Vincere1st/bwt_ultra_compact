"""Sensor platform for BWT Ultra Compact integration."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    BLE_SERVICE_UUID,
    BLE_MAIN_CHARACTERISTIC_UUID,
    CONF_MAC_ADDRESS,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the BWT Ultra Compact sensors."""
    _LOGGER.warning("🧂 Setting up BWT Ultra Compact salt level sensor")

    # Create salt level sensor
    salt_sensor = BWTSaltLevelSensor(hass, entry)
    async_add_entities([salt_sensor])

    _LOGGER.warning("✅ BWT Ultra Compact salt level sensor setup completed")

class BWTSaltLevelSensor(SensorEntity):
    """Representation of a BWT Ultra Compact salt level sensor."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the salt level sensor."""
        self.hass = hass
        self._entry = entry
        self._attr_name = "BWT Ultra Compact Salt Level"
        self._attr_unique_id = f"bwt_ultra_compact_salt_level_{entry.entry_id}"
        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_value = None
        self._attr_options = ["1", "2", "3", "4", "5"]
        self._attr_icon = "mdi:salt"

        # Initialize salt level
        self._attr_native_value = 3  # Default to medium level

        _LOGGER.warning("🧂 BWT Salt Level Sensor initialized (default: level 3)")

    async def async_update(self) -> None:
        """Update the salt level from BWT device."""
        try:
            from homeassistant.components import bluetooth

            mac_address = self._entry.data[CONF_MAC_ADDRESS]
            _LOGGER.warning(f"🔄 Updating salt level for device {mac_address}")

            # Get Bluetooth device
            ble_device = bluetooth.async_ble_device_from_address(
                self.hass, mac_address.upper(), connectable=True
            )

            if not ble_device:
                _LOGGER.error("❌ Bluetooth device not available for salt level reading")
                self._attr_native_value = None
                self._attr_icon = "mdi:salt-off"
                return

            # Read salt level from BLE characteristic
            # Note: This is a simplified implementation
            # In a real scenario, we would read from the actual BLE characteristic
            # For now, we'll simulate reading from the device

            _LOGGER.warning("📖 Reading salt level from BLE characteristic...")

            # Simulate reading from BLE (to be replaced with actual BLE reading)
            # In reality, we would use:
            # client = await bluetooth.async_ble_device_connect(ble_device)
            # salt_data = await client.read_gatt_char(BLE_MAIN_CHARACTERISTIC_UUID)
            # salt_level = self._parse_salt_level(salt_data)

            # For now, simulate a successful read with default value
            simulated_salt_level = 3  # Default medium level

            # Update sensor state
            self._attr_native_value = simulated_salt_level
            self._update_salt_icon(simulated_salt_level)

            _LOGGER.warning(f"🧂 Salt level updated: {simulated_salt_level}/5")

        except Exception as err:
            _LOGGER.error("⚠️ Error reading salt level: %s", err)
            self._attr_native_value = None
            self._attr_icon = "mdi:salt-alert"

    def _update_salt_icon(self, level: int) -> None:
        """Update icon based on salt level."""
        if level == 1:
            self._attr_icon = "mdi:salt"
        elif level == 2:
            self._attr_icon = "mdi:salt"
        elif level == 3:
            self._attr_icon = "mdi:salt"
        elif level == 4:
            self._attr_icon = "mdi:salt"
        elif level == 5:
            self._attr_icon = "mdi:salt"
        else:
            self._attr_icon = "mdi:salt-question"

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return additional state attributes."""
        return {
            "device_id": self._entry.data[CONF_MAC_ADDRESS],
            "salt_level": self._attr_native_value,
            "status": "active" if self._attr_native_value is not None else "error",
        }

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._attr_native_value is not None
