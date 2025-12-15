"""Config flow for BWT Ultra Compact integration."""
from __future__ import annotations

from typing import Any
import logging
import re

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, CONF_MAC_ADDRESS, CONF_PASSKEY, DEFAULT_PASSKEY, DEFAULT_NAME

_LOGGER = logging.getLogger(__name__)

class BWTConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for BWT Ultra Compact."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required(CONF_MAC_ADDRESS): str,
                    vol.Required(CONF_PASSKEY, default=DEFAULT_PASSKEY): str,
                }),
            )

        # Basic validation
        errors = {}

        # Validate MAC address format
        if not user_input[CONF_MAC_ADDRESS]:
            errors["base"] = "invalid_mac_address"
        else:
            mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
            if not re.match(mac_pattern, user_input[CONF_MAC_ADDRESS]):
                errors["base"] = "invalid_mac_address"

        # Validate passkey
        if not user_input[CONF_PASSKEY].isdigit() or len(user_input[CONF_PASSKEY]) != 6:
            errors["base"] = "invalid_passkey"

        if errors:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required(CONF_MAC_ADDRESS): str,
                    vol.Required(CONF_PASSKEY, default=DEFAULT_PASSKEY): str,
                }),
                errors=errors,
            )

        return self.async_create_entry(
            title=f"{DEFAULT_NAME} ({user_input[CONF_MAC_ADDRESS]})",
            data=user_input
        )

class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""

class InvalidMacAddress(HomeAssistantError):
    """Error to indicate there is an invalid MAC address."""

class InvalidPasskey(HomeAssistantError):
    """Error to indicate there is an invalid passkey."""
