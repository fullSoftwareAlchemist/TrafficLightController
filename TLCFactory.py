from __future__ import annotations

from pathlib import Path

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
from TrafficLightAbstraction import ITrafficLightDriver, TrafficLightConsoleDriver


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
        sequence = TLCConfigProvider(Path(__file__).with_name("TLCConfig.txt")).load_sequence()
        traffic_lights = {
            name: TrafficLight(TLCFactory.createTrafficLightStates(TrafficLightConsoleDriver()))
            for name in ("car_main", "ped_main", "car_cross", "ped_cross")
        }
        return TrafficLightController(TlcNormalOperationState(sequence, traffic_lights), TlcSafeState(traffic_lights))

    @staticmethod
    def createGuiTLC(trafficLightDrivers: dict[str, ITrafficLightDriver]) -> TrafficLightController:
        sequence = TLCConfigProvider(Path(__file__).with_name("TLCConfig.txt")).load_sequence()
        traffic_lights = {
            name: TrafficLight(TLCFactory.createTrafficLightStates(driver)) for name, driver in trafficLightDrivers.items()
        }
        return TrafficLightController(TlcNormalOperationState(sequence, traffic_lights), TlcSafeState(traffic_lights))

    @staticmethod
    def createGuiLeftTurnTLC(trafficLightDrivers: dict[str, ITrafficLightDriver]) -> TrafficLightController:
        sequence = TLCConfigProvider(Path(__file__).with_name("TLCLeftConfig.txt")).load_sequenceLeftTurn()
        traffic_lights = {
            name: TrafficLight(TLCFactory.createTrafficLightStates(driver)) for name, driver in trafficLightDrivers.items()
        }
        return TrafficLightController(TlcNormalOperationState(sequence, traffic_lights), TlcSafeState(traffic_lights))

    @staticmethod
    def createHackedGuiLeftTurnTLC(trafficLightDrivers: dict[str, ITrafficLightDriver]) -> TrafficLightController:
        sequence = TLCConfigProvider(Path(__file__).with_name("TLCLeftConfig_hacked.txt")).load_sequenceLeftTurn()
        traffic_lights = {
            name: TrafficLight(TLCFactory.createTrafficLightStates(driver)) for name, driver in trafficLightDrivers.items()
        }
        return TrafficLightController(TlcNormalOperationState(sequence, traffic_lights), TlcSafeState(traffic_lights))
