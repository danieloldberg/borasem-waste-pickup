"""Config flow for Borås Energi och Miljö Waste Pickup integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
from borasem_waste import auth, borasem
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema({vol.Required("address"): str})


class BorasEMConfigFlow:
    """Class to validate Borås EM Config Flow."""

    def __init__(self, address: str) -> None:
        """Initialize."""
        self.address = address

    async def validateAddress(self) -> Any:
        """Test if the address exist in BorasEM API."""

        async with aiohttp.ClientSession() as session:
            authObj = auth.Auth(session)
            api = borasem.BorasEM(authObj)

            _LOGGER.debug("Input: ")
            _LOGGER.debug(self.address)

            # Check address
            addressList = await api.async_get_address(self.address)

            _LOGGER.debug("Retrieved")
            for addressItem in addressList:
                _LOGGER.debug(addressItem)

            # Only return true if we have one exact match, otherwise return false.
            if len(addressList) == 1:
                # Replace the user input with the matched address.
                self.address = addressList[0]
            else:
                raise InvalidAddress

            # return len(addressList) == 1


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """

    hub = BorasEMConfigFlow(data["address"])

    try:
        await hub.validateAddress()
    except InvalidAddress:
        raise InvalidAddress

    _LOGGER.info(hub.address)
    return {"address": hub.address}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Borås Energi och Miljö Waste Pickup."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAddress:
                errors["base"] = "invalid_address"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["address"], data=info)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAddress(HomeAssistantError):
    """Error to indicate we cannot connect."""
