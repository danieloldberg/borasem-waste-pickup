"""Sensor platform for Borås Energi och Miljö Waste Pickup information."""

import logging

from dateutil import parser

from homeassistant.components.date import DateEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import BorasEMCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Borås Energi och Miljö container sensors."""
    coordinator: BorasEMCoordinator = hass.data[DOMAIN][entry.entry_id]
    data = await coordinator.data

    dateEntities = [container for container in data if container["waste_type"][:4] == "Kärl"]
    sensorEntities = [container for container in data if container["waste_type"] == "Slam"]
    # for dateEntity in dateEntities:
    #     async_add_entities(ContainerDateEntity(coordinator, dateEntity))
    async_add_entities(ContainerDateEntity(coordinator, dateEntity) for dateEntity in dateEntities )
    async_add_entities(ContainerSensorEntity(coordinator, sensorEntity) for sensorEntity in sensorEntities )


def get_entity_state(obj):
    if obj["waste_type"][:4]=="Kärl":
        return parser.parse(obj["next_waste_pickup"])
    else:
        return str(obj["next_waste_pickup"])

class ContainerDateEntity(CoordinatorEntity, DateEntity):
    """An entity using DateEntity.

    The CoordinatorEntity class provides:
      should_poll
      async_update
      async_added_to_hass
      available

    """

    _attr_has_entity_name = True
    _attr_icon = "mdi:delete"


    def __init__(self, coordinator, idx):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator, context=idx)
        self.idx = idx
        self.address = coordinator.address
        self._attr_native_value = parser.parse(self.idx["next_waste_pickup"])
        self._attr_unique_id = self.generate_unique_id(
            self.address, self.idx["container_id"]
        )
        self._attr_name = self.idx["container_id"]
        self._attr_extra_state_attributes = {
            "Is active": self.idx["is_active"],
            "Waste type": self.idx["waste_type"],
            "Waste pickup frequency": self.idx["waste_pickup_frequency"],
            "Waste pickups per year": self.idx["waste_pickups_per_year"],
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = parser.parse(self.idx["next_waste_pickup"])

        self._attr_name = self.coordinator.data["container_id"]
        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, self.address)},
            manufacturer="Borås Energi och Miljö",
            name=self.address,
        )
        self._attr_extra_state_attributes = {
            "Is active": self.idx["is_active"],
            "Waste type": self.idx["waste_type"],
            "Waste pickup frequency": self.idx["waste_pickup_frequency"],
            "Waste pickups per year": self.idx["waste_pickups_per_year"],
        }
        self.async_write_ha_state()

    def generate_unique_id(self, entry_name: str, entity_name: str) -> str:
        """Generate a unique IDs for each entity."""
        entry_name = entry_name.lower().replace(" ", "_")
        entity_name = entity_name.lower().replace(" ", "_")
        return entry_name + "_" + entity_name


class ContainerSensorEntity(CoordinatorEntity, SensorEntity):
    """An entity using SensorEntity.

    The CoordinatorEntity class provides:
      should_poll
      async_update
      async_added_to_hass
      available

    """

    _attr_has_entity_name = True
    _attr_icon = "mdi:delete"



    def __init__(self, coordinator, idx):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator, context=idx)
        self.idx = idx
        self.address = coordinator.address
        self._attr_native_value = get_entity_state(self.idx)
        self._attr_unique_id = self.generate_unique_id(
            self.address, self.idx["description"]
        )
        self._attr_name = self.idx["description"]
        self._attr_extra_state_attributes = {
            "Is active": self.idx["is_active"],
            "Waste type": self.idx["waste_type"],
            "Waste pickup frequency": self.idx["waste_pickup_frequency"],
            "Waste pickups per year": self.idx["waste_pickups_per_year"],
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = get_entity_state(self.idx)

        self._attr_name = self.coordinator.data["description"]
        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, self.address)},
            manufacturer="Borås Energi och Miljö",
            name=self.address,
        )
        self._attr_extra_state_attributes = {
            "Is active": self.idx["is_active"],
            "Waste type": self.idx["waste_type"],
            "Waste pickup frequency": self.idx["waste_pickup_frequency"],
            "Waste pickups per year": self.idx["waste_pickups_per_year"],
        }
        self.async_write_ha_state()

    def generate_unique_id(self, entry_name: str, entity_name: str) -> str:
        """Generate a unique IDs for each entity."""
        entry_name = entry_name.lower().replace(" ", "_")
        entity_name = entity_name.lower().replace(" ", "_")
        return entry_name + "_" + entity_name
