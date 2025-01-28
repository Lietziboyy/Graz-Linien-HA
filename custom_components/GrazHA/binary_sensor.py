from homeassistant.components.binary_sensor import BinarySensorEntity

class GrazHABinarySensor(BinarySensorEntity):
    """GrazHA binary_sensor class."""

    def __init__(
        self,
        coordinator: BlueprintDataUpdateCoordinator,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary_sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def is_on(self) -> bool:
        """Return true if the binary_sensor is on."""
        return self.coordinator.data.get("title", "") == "foo"

    async def update_state_from_website(self):
        """Check the status of the website and update the binary sensor."""
        try:
            import requests
        except ImportError:
            raise RuntimeError(
                "This platform requires python-requests to be installed."
            )

        url = "https://verkehrsauskunft.verbundlinie.at"
        response = requests.get(url)

        if response.status_code == 200:
            self.coordinator.data["title"] = "foo"  # Assuming this is the expected title when the website is online
            self.async_schedule_update_ha_state(True)
        else:
            try:
                response.raise_for_status()
            except requests.HTTPError as e:
                # Handle HTTP errors here, for example, print the error message
                print(f"HTTP Error: {e}")
            else:
                # Handle other non-200 status codes here
                self.coordinator.data["title"] = ""  # Or some other value to indicate the website is offline
                self.async_schedule_update_ha_state(False)

    async def async_will_remove_from_hass(self):
        """Clean up when removing from hass."""
        await super().async_will_remove_from_hass()
        self.coordinator.data["title"] = ""  # Reset title