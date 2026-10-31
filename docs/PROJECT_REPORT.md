# Battery Cell Imbalance Detection

## Project summary

This project monitors four cell voltages, pack current, and four cell temperatures. It calculates cell-to-cell voltage spread, classifies the battery state, derives software actuator states, stores telemetry in InfluxDB, and presents the results through Grafana or the Vercel dashboard shell.

## Requirements

- Receive JSON telemetry on `battery/device01/raw`.
- Calculate maximum, minimum, average and imbalance voltage.
- Detect voltage limits outside 2.8 V to 4.2 V.
- Classify imbalance above 0.10 V as warning and above 0.20 V as critical.
- Classify temperature above 38 C as warning and above 85 C as critical.
- Store analyzed telemetry in the `battery_monitor` InfluxDB bucket.
- Keep credentials in environment variables.

## Method

The imbalance is `max(cell voltages) - min(cell voltages)`. Temperature status is based on the maximum cell temperature. Overall status becomes CRITICAL for voltage anomalies, critical temperature, or critical imbalance; WARNING for warning temperature, warning imbalance, or temperature anomalies; otherwise NORMAL.

## Actuator logic

NORMAL keeps the relay on, buzzer off and LED green. WARNING keeps the relay on, turns the buzzer on and LED yellow. CRITICAL turns the relay off, turns the buzzer on and LED red. The fan turns on for warning or critical temperature.

## Testing plan

Run representative NORMAL, WARNING imbalance, CRITICAL imbalance, voltage anomaly, temperature warning, invalid payload, InfluxDB persistence and dashboard display cases. Record input JSON, receiver output, stored point and dashboard screenshot for each required case.

## Limitations

The prototype does not claim physical ESP32 hardware, a real battery pack, safety certification, or production cloud deployment. The simulator is not an electrochemical battery model. Trend analysis, hysteresis, SOC/SOH estimation and balancing hardware are future work.
