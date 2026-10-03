"""Sensors: salt remaining (kg) and salt level (%)."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    EntityCategory,
    UnitOfMass,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .client import BwtState
from .coordinator import BwtConfigEntry
from .entity import BwtEntity


@dataclass(frozen=True, kw_only=True)
class BwtSensorDescription(SensorEntityDescription):
    """Sensor description with a value function."""

    value_fn: Callable[[BwtState], float | int]


SENSORS = (
    BwtSensorDescription(
        key="salt_remaining",
        translation_key="salt_remaining",
        device_class=SensorDeviceClass.WEIGHT,
        native_unit_of_measurement=UnitOfMass.KILOGRAMS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        value_fn=lambda s: s.salt_grams / 1000,
    ),
    BwtSensorDescription(
        key="salt_percentage",
        translation_key="salt_percentage",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        value_fn=lambda s: s.salt_percent,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: BwtConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up sensors."""
    coordinator = entry.runtime_data
    async_add_entities(
        [*(BwtSensor(coordinator, d) for d in SENSORS), BwtRssiSensor(coordinator)]
    )


class BwtSensor(BwtEntity, SensorEntity):
    """A softener sensor."""

    entity_description: BwtSensorDescription

    def __init__(self, coordinator, description: BwtSensorDescription) -> None:
        super().__init__(coordinator, description.key)
        self.entity_description = description

    @property
    def native_value(self) -> float | int:
        return self.entity_description.value_fn(self.coordinator.data)


RSSI = SensorEntityDescription(
    key="rssi",
    translation_key="rssi",
    device_class=SensorDeviceClass.SIGNAL_STRENGTH,
    native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    state_class=SensorStateClass.MEASUREMENT,
    entity_category=EntityCategory.DIAGNOSTIC,
)


class BwtRssiSensor(BwtEntity, SensorEntity):
    """Bluetooth signal strength of the last advertisement (refreshed with each poll)."""

    entity_description = RSSI

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, RSSI.key)

    @property
    def native_value(self) -> int | None:
        return self.coordinator.rssi
