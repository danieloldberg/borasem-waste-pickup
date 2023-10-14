"""Exceptions to the co2signal integration."""
from homeassistant.exceptions import HomeAssistantError


class BorasEMError(HomeAssistantError):
    """Base error."""


class UnknownError(BorasEMError):
    """Raised when an unknown error occurs."""
