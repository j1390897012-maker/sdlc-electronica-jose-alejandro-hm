import pytest

from sensor_registry import SensorRegistry, SensorNotFoundError

def test_get_unkown_sensor_raises():
    registry = SensorRegistry()

with pytest.raises(SensorNotFoundError):
    registry.get("GHOST-99")