from __future__ import annotations

from pathlib import Path

from HAL.FileAccess import FileAccess
from TLC import TlcNormalOperationState, TlcSafeState, TrafficLightController
from TLCConfigProvider import TLCConfigProvider
from TrafficLight import (
    AmberState,
    GreenState,
    ITrafficLightState,
    LightColor,
    OffState,
    RedAmberState,
    RedState,
    TrafficLight,
)
from HAL.TrafficLightAbstraction import ITrafficLightDriver, TrafficLightConsoleDriver

CONFIG_DIR = Path(__file__).parent / "config"


class TLCFactory:
    @staticmethod
    def createTrafficLightStates(trafficLightDriver: ITrafficLightDriver) -> dict[LightColor, ITrafficLightState]:
        return {
            LightColor.RED: RedState(trafficLightDriver),
            LightColor.RED_AMBER: RedAmberState(trafficLightDriver),
            LightColor.GREEN: GreenState(trafficLightDriver),
            LightColor.AMBER: AmberState(trafficLightDriver),
            LightColor.OFF: OffState(trafficLightDriver),
        }

    @staticmethod
    def createConsoleTLC() -> TrafficLightController:
        sequence = TLCConfigProvider(FileAccess(CONFIG_DIR / "TLCConfig.txt")).load_sequence()
        traffic_lights = {
            name: TrafficLight(TLCFactory.createTrafficLightStates(TrafficLightConsoleDriver()))
            for name in ("car_main", "ped_main", "car_cross", "ped_cross")
        }
        return TrafficLightController(TlcNormalOperationState(sequence, traffic_lights), TlcSafeState(traffic_lights))

    @staticmethod
    def createGuiTLC(trafficLightDrivers: dict[str, ITrafficLightDriver]) -> TrafficLightController:
        sequence = TLCConfigProvider(FileAccess(CONFIG_DIR / "TLCConfig.txt")).load_sequence()
        traffic_lights = {
            name: TrafficLight(TLCFactory.createTrafficLightStates(driver)) for name, driver in trafficLightDrivers.items()
        }
        return TrafficLightController(TlcNormalOperationState(sequence, traffic_lights), TlcSafeState(traffic_lights))

    @staticmethod
    def createGuiLeftTurnTLC(trafficLightDrivers: dict[str, ITrafficLightDriver]) -> TrafficLightController:
        sequence = TLCConfigProvider(FileAccess(CONFIG_DIR / "TLCLeftConfig.txt")).load_sequenceLeftTurn()
        traffic_lights = {
            name: TrafficLight(TLCFactory.createTrafficLightStates(driver)) for name, driver in trafficLightDrivers.items()
        }
        return TrafficLightController(TlcNormalOperationState(sequence, traffic_lights), TlcSafeState(traffic_lights))

    @staticmethod
    def createHackedGuiLeftTurnTLC(trafficLightDrivers: dict[str, ITrafficLightDriver]) -> TrafficLightController:
        sequence = TLCConfigProvider(FileAccess(CONFIG_DIR / "TLCLeftConfig_hacked.txt")).load_sequenceLeftTurn()
        traffic_lights = {
            name: TrafficLight(TLCFactory.createTrafficLightStates(driver)) for name, driver in trafficLightDrivers.items()
        }
        return TrafficLightController(TlcNormalOperationState(sequence, traffic_lights), TlcSafeState(traffic_lights))
