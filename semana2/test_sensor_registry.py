import pytest
from sensor_registry import SensorNotFoundError, SensorRegistry


def test_get_unkown_sensor_raises() -> None:
    registry = SensorRegistry()

    with pytest.raises(SensorNotFoundError):
        registry.get("GHOST-99")