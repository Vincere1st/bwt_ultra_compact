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
        # For ENUM device class, state_class should be None
        self._attr_state_class = None
        self._attr_native_value = None
        self._attr_options = ["1", "2", "3", "4", "5"]
        self._attr_icon = "mdi:salt"

        # Initialize salt level (must be string for ENUM device class)
        self._attr_native_value = "3"  # Default to medium level

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
            _LOGGER.warning("📖 Reading salt level from BLE characteristic...")

            # Try to read the characteristic using available methods
            try:
                # Try using bleak if available
                try:
                    import bleak
                    from bleak import BleakClient

                    # Connect to the device using bleak
                    async with BleakClient(ble_device.address) as client:
                        if client.is_connected:
                            # Read the characteristic
                            salt_data = await client.read_gatt_char(BLE_MAIN_CHARACTERISTIC_UUID)
                            _LOGGER.warning(f"📊 Raw BLE data received: {salt_data.hex()}")

                            # Parse the salt level from BLE data
                            salt_level = self._parse_salt_level(salt_data)

                            # Update sensor state (convert to string for ENUM device class)
                            self._attr_native_value = str(salt_level)
                            self._update_salt_icon(salt_level)

                            _LOGGER.warning(f"🧂 Salt level updated: {salt_level}/5")
                        else:
                            _LOGGER.error("❌ Failed to connect to BLE device using bleak")
                            self._attr_native_value = None
                            self._attr_icon = "mdi:salt-alert"

                except ImportError:
                    _LOGGER.error("❌ bleak library not available, using fallback method")
                    self._attr_native_value = None
                    self._attr_icon = "mdi:salt-alert"

            except Exception as read_err:
                _LOGGER.error("⚠️ Error reading BLE characteristic: %s", read_err)
                self._attr_native_value = None
                self._attr_icon = "mdi:salt-alert"

        except Exception as err:
            _LOGGER.error("⚠️ Error reading salt level: %s", err)
            self._attr_native_value = None
            self._attr_icon = "mdi:salt-alert"

    def _parse_salt_level(self, data: bytes) -> int:
        """Parse salt level from BLE data."""
        # BWT Ultra Compact salt level protocol:
        # The device sends the salt level as a single byte (1-5)
        # If the data is empty or invalid, return default value

        if not data:
            _LOGGER.warning("⚠️ Empty BLE data received, using default value")
            return 3

        try:
            # The salt level is in the first byte
            level = data[0]

            # Validate the level (must be between 1 and 5)
            if 1 <= level <= 5:
                return level

            # If invalid, return default value
            _LOGGER.warning(f"⚠️ Invalid salt level received: {level}, using default value")
            return 3

        except (IndexError, ValueError) as err:
            _LOGGER.error("⚠️ Error parsing BLE data: %s", err)
            return 3

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
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self._attr_native_value

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
