"""DataUpdateCoordinator for the Borås Energi och Miljö integration."""
from __future__ import annotations

import asyncio
from collections.abc import Mapping
from datetime import timedelta
import logging
from typing import Any

import aiohttp
from borasem_waste import auth, borasem

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN
from .exceptions import UnknownError

_LOGGER = logging.getLogger(__name__)


class BorasEMCoordinator(DataUpdateCoordinator):
    """Data update coordinator."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass, _LOGGER, name=DOMAIN, update_interval=timedelta(hours=24)
        )
        self._entry = entry
        self.address = entry.title

    @property
    def entry_id(self) -> str:
        """Return entry ID."""
        return self._entry.entry_id

    async def _async_update_data(self):
        """Fetch the latest data from the source."""
        try:
            # data = await self.hass.async_add_executor_job(
            #     get_data, self.hass, self._entry.data
            # )
            data = data = await asyncio.to_thread(
                get_data, self.hass, self._entry.data, self.address
            )
        except UnknownError as err:
            raise UnknownError(str(err)) from err

        return data


async def get_data(hass: HomeAssistant, config: Mapping[str, Any], address):
    """Get data from the API."""

    try:
        async with aiohttp.ClientSession() as session:
            authObj = auth.Auth(session)
            api = borasem.BorasEM(authObj)

            # # Get Waste Schedule
            data = await api.async_get_schedule(address)

    except ValueError as err:
        str(err)

        _LOGGER.exception("Unexpected exception")
        raise UnknownError from err

    return data
