"""Support for Adax temperature sensors."""
import logging

from adax import Adax
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import CONF_PASSWORD, UnitOfTemperature
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import ACCOUNT_ID

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Adax temperature sensor with config flow."""
    await _setup(
        hass, entry.data[ACCOUNT_ID], entry.data[CONF_PASSWORD], async_add_entities
    )


async def _setup(hass, account_id, password, async_add_entities):
    adax_data_handler = Adax(
        account_id, password, websession=async_get_clientsession(hass)
    )

    sensors = []
    for room in await adax_data_handler.get_rooms():
        sensors.append(AdaxTemperatureSensor(room, adax_data_handler))
    async_add_entities(sensors)


class AdaxTemperatureSensor(SensorEntity):
    """Representation of an Adax temperature sensor."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, room_data, adax_data_handler):
        """Initialize the temperature sensor."""
        self._room_data = room_data
        self._adax_data_handler = adax_data_handler

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self._room_data['homeId']}_{self._room_data['id']}_temperature"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._room_data['name']} Temperature"

    @property
    def native_value(self):
        """Return the current temperature."""
        return self._room_data.get("temperature")

    @property
    def available(self):
        """Return if entity is available."""
        return self._room_data.get("temperature") is not None

    async def async_update(self):
        """Get the latest data."""
        for room in await self._adax_data_handler.get_rooms():
            if room["id"] == self._room_data["id"]:
                self._room_data = room
                return
