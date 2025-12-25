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
        _LOGGER.debug("🔍 TRACE: Starting async_update")
        try:
            from homeassistant.components import bluetooth

            mac_address = self._entry.data[CONF_MAC_ADDRESS]
            _LOGGER.debug(f"🔍 TRACE: mac_address = {mac_address}")
            _LOGGER.warning(f"🔄 Updating salt level for device {mac_address}")

            # Get Bluetooth device
            _LOGGER.debug("🔍 TRACE: Getting Bluetooth device")
            ble_device = bluetooth.async_ble_device_from_address(
                self.hass, mac_address.upper(), connectable=True
            )

            if not ble_device:
                _LOGGER.error("❌ Bluetooth device not available for salt level reading")
                self._attr_native_value = None
                self._attr_icon = "mdi:salt-off"
                return

            # Read salt level from BLE characteristic
            _LOGGER.debug("🔍 TRACE: Reading salt level from BLE characteristic")
            _LOGGER.warning("📖 Reading salt level from BLE characteristic...")

            # Read salt level from BLE characteristic
            _LOGGER.warning("📖 Reading salt level from BLE characteristic...")

            # Try using bleak with retry connector for reliable connection
            try:
                import bleak
                from bleak import BleakClient
                from bleak_retry_connector import establish_connection

                # Use bleak-retry-connector for reliable connection
                _LOGGER.debug("🔍 TRACE: Establishing reliable BLE connection")
                _LOGGER.warning("🔄 Establishing reliable BLE connection...")

                # Establish connection with retry
                _LOGGER.debug("🔍 TRACE: Establishing connection with retry")
                client = await establish_connection(
                    BleakClient,
                    ble_device.address,
                    ble_device.name,
                    max_attempts=3,
                    timeout=10.0
                )

                if client and client.is_connected:
                    try:
                        # Read the characteristic
                        _LOGGER.debug("🔍 TRACE: Reading characteristic")
                        salt_data = await client.read_gatt_char(BLE_MAIN_CHARACTERISTIC_UUID)
                        _LOGGER.debug(f"🔍 TRACE: salt_data = {salt_data.hex()}")
                        _LOGGER.warning(f"📊 Raw BLE data received: {salt_data.hex()}")

                        # Parse the salt level from BLE data
                        _LOGGER.debug("🔍 TRACE: Parsing salt level")
                        salt_level = self._parse_salt_level(salt_data)

                        # Update sensor state (convert to string for ENUM device class)
                        _LOGGER.debug(f"🔍 TRACE: salt_level = {salt_level}")
                        self._attr_native_value = str(salt_level)
                        self._update_salt_icon(salt_level)

                        _LOGGER.warning(f"🧂 Salt level updated: {salt_level}/5")

                    except Exception as read_err:
                        # Handle exception safely with detailed logging
                        _LOGGER.debug(f"🔍 TRACE: Exception in read_err = {read_err}")
                        error_msg = str(read_err)
                        _LOGGER.error("⚠️ Error reading BLE characteristic (raw): %s", read_err)
                        _LOGGER.error("⚠️ Error type: %s", type(read_err))
                        # Check if read_err is an object (not a string) before checking for details
                        if not isinstance(read_err, str) and hasattr(read_err, 'details'):
                            error_msg = f"{error_msg} - Details: {read_err.details}"
                        else:
                            _LOGGER.error("⚠️ Error has no details attribute")
                        _LOGGER.error("⚠️ Error reading BLE characteristic: %s", error_msg)
                        self._attr_native_value = None
                        self._attr_icon = "mdi:salt-alert"

                    finally:
                        # Disconnect from the device
                        _LOGGER.debug("🔍 TRACE: Disconnecting from device")
                        await client.disconnect()

                else:
                    _LOGGER.error("❌ Failed to connect to BLE device using bleak-retry-connector")
                    self._attr_native_value = None
                    self._attr_icon = "mdi:salt-alert"

            except ImportError as import_err:
                _LOGGER.debug(f"🔍 TRACE: ImportError = {import_err}")
                _LOGGER.error("❌ bleak or bleak-retry-connector not available: %s", import_err)
                _LOGGER.warning("💡 Please install bleak and bleak-retry-connector")
                self._attr_native_value = None
                self._attr_icon = "mdi:salt-alert"

            except Exception as err:
                # Handle exception safely with detailed logging
                _LOGGER.debug(f"🔍 TRACE: Exception in err = {err}")
                error_msg = str(err)
                _LOGGER.error("⚠️ Error reading salt level (raw): %s", err)
                _LOGGER.error("⚠️ Error type: %s", type(err))
                # Check if err is an object (not a string) before checking for details
                if not isinstance(err, str) and hasattr(err, 'details'):
                    error_msg = f"{error_msg} - Details: {err.details}"
                else:
                    _LOGGER.error("⚠️ Error has no details attribute")
                _LOGGER.error("⚠️ Error reading salt level: %s", error_msg)
                self._attr_native_value = None
                self._attr_icon = "mdi:salt-alert"

        except Exception as err:
            # Handle exception safely with detailed logging
            _LOGGER.debug(f"🔍 TRACE: Exception in outer err = {err}")
            error_msg = str(err)
            _LOGGER.error("⚠️ Error reading salt level (raw): %s", err)
            _LOGGER.error("⚠️ Error type: %s", type(err))
            # Check if err is an object (not a string) before checking for details
            if not isinstance(err, str) and hasattr(err, 'details'):
                error_msg = f"{error_msg} - Details: {err.details}"
            else:
                _LOGGER.error("⚠️ Error has no details attribute")
            _LOGGER.error("⚠️ Error reading salt level: %s", error_msg)
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
