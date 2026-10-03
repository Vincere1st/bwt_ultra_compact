"""Binary sensor: salt alarm reported by the softener."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import BwtConfigEntry
from .entity import BwtEntity

ALARM = BinarySensorEntityDescription(
    key="salt_alarm",
    translation_key="salt_alarm",
    device_class=BinarySensorDeviceClass.PROBLEM,
)


async def async_setup_entry(
    hass: HomeAssistant, entry: BwtConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up binary sensors."""
    async_add_entities([BwtAlarm(entry.runtime_data)])


class BwtAlarm(BwtEntity, BinarySensorEntity):
    """Salt alarm ("verif sel")."""

    entity_description = ALARM

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, ALARM.key)

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.alarm
