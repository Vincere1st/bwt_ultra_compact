"""Data update coordinator."""
from __future__ import annotations

import logging

from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ADDRESS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .ble import BwtConnectionError, async_read_state
from .client import BwtState
from .const import DOMAIN, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

type BwtConfigEntry = ConfigEntry[BwtCoordinator]


class BwtCoordinator(DataUpdateCoordinator[BwtState]):
    """Poll the softener. No default value: a failure makes entities unavailable."""

    config_entry: BwtConfigEntry

    def __init__(self, hass: HomeAssistant, entry: BwtConfigEntry) -> None:
        super().__init__(
            hass, _LOGGER, name=DOMAIN, config_entry=entry, update_interval=SCAN_INTERVAL
        )
        self.address: str = entry.data[CONF_ADDRESS]
        self.rssi: int | None = None

    async def _async_update_data(self) -> BwtState:
        info = bluetooth.async_last_service_info(
            self.hass, self.address, connectable=True
        )
        self.rssi = info.rssi if info else None
        try:
            return await async_read_state(self.hass, self.address)
        except BwtConnectionError as err:
            raise UpdateFailed(str(err)) from err
