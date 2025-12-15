"""Config flow for BWT Minimal Test integration."""
from __future__ import annotations

from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

class BWTMinimalConfigFlow(config_entries.ConfigFlow, domain="bwt_minimal"):
    """Handle a config flow for BWT Minimal Test."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required("test_field"): str,
                }),
            )
        return self.async_create_entry(title="BWT Minimal Test", data=user_input)
