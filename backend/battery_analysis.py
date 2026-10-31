from dataclasses import dataclass


MIN_CELL_VOLTAGE = 2.8
MAX_CELL_VOLTAGE = 4.2
WARNING_IMBALANCE = 0.10
CRITICAL_IMBALANCE = 0.20
MIN_CELL_TEMPERATURE = 22.0
MAX_CELL_TEMPERATURE = 38.0
CRITICAL_TEMPERATURE = 85.0


@dataclass(frozen=True)
class BatteryAnalysis:
    maximum_voltage: float
    minimum_voltage: float
    average_voltage: float
    voltage_imbalance: float
    maximum_temperature: float
    minimum_temperature: float
    average_temperature: float
    voltage_anomalies: tuple[str, ...]
    temperature_anomalies: tuple[str, ...]
    imbalance_status: str
    temperature_status: str
    battery_status: str


def analyze_battery(voltages: list[float], current: float, temperatures: list[float]) -> BatteryAnalysis:
    if len(voltages) != 4 or len(temperatures) != 4:
        raise ValueError("Exactly four cell voltages and four temperatures are required")
    if not all(map(float, voltages + temperatures + [current])):
        raise ValueError("Telemetry values must be numeric")

    maximum_voltage = max(voltages)
    minimum_voltage = min(voltages)
    average_voltage = sum(voltages) / len(voltages)
    voltage_imbalance = maximum_voltage - minimum_voltage
    maximum_temperature = max(temperatures)
    minimum_temperature = min(temperatures)
    average_temperature = sum(temperatures) / len(temperatures)

    voltage_anomalies = tuple(
        f"Cell {index} LOW VOLTAGE" if value < MIN_CELL_VOLTAGE else f"Cell {index} HIGH VOLTAGE"
        for index, value in enumerate(voltages, start=1)
        if value < MIN_CELL_VOLTAGE or value > MAX_CELL_VOLTAGE
    )
    temperature_anomalies = tuple(
        f"Cell {index} CRITICAL TEMPERATURE" if value > CRITICAL_TEMPERATURE
        else f"Cell {index} HIGH TEMPERATURE" if value > MAX_CELL_TEMPERATURE
        else f"Cell {index} LOW TEMPERATURE"
        for index, value in enumerate(temperatures, start=1)
        if value > CRITICAL_TEMPERATURE or value > MAX_CELL_TEMPERATURE or value < MIN_CELL_TEMPERATURE
    )

    imbalance_status = (
        "CRITICAL" if voltage_imbalance > CRITICAL_IMBALANCE
        else "WARNING" if voltage_imbalance > WARNING_IMBALANCE
        else "NORMAL"
    )
    temperature_status = (
        "CRITICAL" if maximum_temperature > CRITICAL_TEMPERATURE
        else "WARNING" if maximum_temperature > MAX_CELL_TEMPERATURE
        else "NORMAL"
    )
    battery_status = (
        "CRITICAL" if voltage_anomalies or temperature_status == "CRITICAL" or imbalance_status == "CRITICAL"
        else "WARNING" if temperature_status == "WARNING" or imbalance_status == "WARNING" or temperature_anomalies
        else "NORMAL"
    )
    return BatteryAnalysis(
        maximum_voltage, minimum_voltage, average_voltage, voltage_imbalance,
        maximum_temperature, minimum_temperature, average_temperature,
        voltage_anomalies, temperature_anomalies, imbalance_status,
        temperature_status, battery_status,
    )


def control_actuators(analysis: BatteryAnalysis) -> dict[str, str]:
    fan = "ON" if analysis.temperature_status in {"WARNING", "CRITICAL"} else "OFF"
    if analysis.battery_status == "CRITICAL":
        return {"fan": fan, "relay": "OFF", "buzzer": "ON", "led": "RED"}
    if analysis.battery_status == "WARNING":
        return {"fan": fan, "relay": "ON", "buzzer": "ON", "led": "YELLOW"}
    return {"fan": fan, "relay": "ON", "buzzer": "OFF", "led": "GREEN"}
