"""The Adax heater integration."""


async def async_setup(hass, config):
    """Set up the Adax platform."""
    return True


async def async_setup_entry(hass, entry):
    """Set up the Adax heater."""
    await hass.config_entries.async_forward_entry_setups(entry, ["climate", "sensor"])
    return True


async def async_unload_entry(hass, config_entry):
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(config_entry, ["climate", "sensor"])
