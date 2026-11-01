# Battery Cell Imbalance Detection

## Submission report

### Project status

This software prototype monitors four-cell battery telemetry, detects voltage imbalance and abnormal temperatures, applies protection-state logic, and provides a dashboard view. The public source repository is [Ritish77/battery-cell-imbalance-detection](https://github.com/Ritish77/battery-cell-imbalance-detection). The static dashboard is deployed at [battery-cell-imbalance-detection-we.vercel.app](https://battery-cell-imbalance-detection-we.vercel.app/).

The implementation is software-only. It does not claim physical ESP32 hardware, a real battery pack, safety certification, or a production cloud data path.

## Objectives

- Receive JSON telemetry on `battery/device01/raw`.
- Analyze four cell voltages, pack current, and four cell temperatures.
- Calculate maximum, minimum, average, and voltage spread.
- Detect voltage, imbalance, and temperature conditions.
- Derive relay, fan, buzzer, and LED protection outputs.
- Store analyzed telemetry in the `battery_monitor` InfluxDB bucket when configured.
- Present verified demo values through the deployed Vercel dashboard.

## Requirements and implementation status

| Requirement | Implementation status |
|---|---|
| Four-cell telemetry model | Implemented in `battery_analysis.py` and `battery_simulator.py` |
| MQTT topic `battery/device01/raw` | Implemented in `mqtt_receiver.py` and simulator configuration |
| Voltage spread analysis | Implemented as maximum cell voltage minus minimum cell voltage |
| Voltage limits 2.8 V to 4.2 V | Implemented |
| Imbalance warning above 0.10 V | Implemented |
| Imbalance critical above 0.20 V | Implemented |
| Temperature warning above 38 C | Implemented |
| Temperature critical above 85 C | Implemented |
| InfluxDB bucket `battery_monitor` | Implemented as an optional persistence path |
| Grafana dashboard definition | Included in `grafana/battery-dashboard.json` |
| Static Vercel dashboard | Deployed and verified |
| Live MQTT/InfluxDB data in Vercel | Not implemented; requires a separate authenticated API |

## Architecture and data flow

```text
Python simulator or sensors -> Mosquitto MQTT: battery/device01/raw
    -> Python receiver and analysis rules
       -> InfluxDB bucket: battery_monitor -> Grafana dashboard

Static demo dashboard: web/ -> Vercel
Future live path: Vercel -> authenticated read-only API -> InfluxDB
```

## Methodology

The receiver decodes a JSON payload and validates the expected four-cell structure. The analysis layer calculates voltage statistics and the maximum cell temperature. Imbalance is defined as `maximum_cell_voltage - minimum_cell_voltage`.

The overall state is `CRITICAL` for a critical imbalance, a critical temperature, or a cell voltage outside the configured limits. It is `WARNING` for warning-level imbalance, warning temperature, or temperature anomalies. Otherwise, the state is `NORMAL`.

## Actuator logic

| State | Relay | Fan | Buzzer | LED |
|---|---|---|---|---|
| NORMAL | ON | OFF unless temperature requires it | OFF | GREEN |
| WARNING | ON | ON for temperature warning | ON | YELLOW |
| CRITICAL | OFF | ON | ON | RED |

These are software decisions represented in telemetry output. They are not connected to physical actuators in the verified implementation.

## Repository and deployment

- GitHub repository: <https://github.com/Ritish77/battery-cell-imbalance-detection>
- Vercel project: `battery-cell-imbalance-detection-web`
- Live URL: <https://battery-cell-imbalance-detection-we.vercel.app/>
- Vercel root directory: `web`
- Vercel preset: Other/static
- Deployment status: deployed to production and opened successfully during verification

The repository also contains `vercel.json` so the deployment configuration is explicit. Vercel hosts the static dashboard only; it does not run the persistent MQTT receiver.

## Testing

The automated analysis test suite covers normal telemetry, warning imbalance, and critical imbalance. The verified run completed successfully with 3 tests passing. Additional submission evidence should include receiver logs, an InfluxDB point, a Grafana screenshot, and any live API evidence if those integrations are enabled later.

## Results

The deployed dashboard currently renders verified demo values: four cell voltages, voltage imbalance, average temperature, and relay/fan/buzzer/LED states. It clearly labels itself as a prototype dashboard and does not imply that the displayed values are live hardware measurements.

## Limitations

- The simulator is not an electrochemical battery model.
- No physical ESP32, sensor, relay, fan, buzzer, or battery pack is claimed as implemented.
- The Vercel page currently uses demo values; live InfluxDB data requires a separate authenticated read-only API.
- No SOC/SOH estimation, trend analytics, hysteresis, balancing control, calibration workflow, or safety certification is included.
- Production monitoring, authentication, alert delivery, and cloud data retention require further engineering.

## Future scope

1. Connect a hardware telemetry source after electrical and safety validation.
2. Add an authenticated API between the dashboard and InfluxDB.
3. Add historical charts, alert acknowledgement, and trend-based detection.
4. Add hysteresis and debounce logic to prevent actuator chatter.
5. Add SOC/SOH estimation and cell balancing recommendations.
6. Add deployment secrets, monitoring, and integration tests for the hosted path.

## Submission checklist

- [x] Public GitHub repository created.
- [x] Source code, simulator, tests, Grafana JSON, and web dashboard included.
- [x] Vercel dashboard deployed and verified.
- [x] Documentation updated with repository and website links.
- [ ] Add institution, team, supervisor, and academic year details if required.
- [ ] Add screenshots of the MQTT receiver, InfluxDB measurement, Grafana dashboard, and deployed site.
- [ ] Add measured test evidence if physical or hosted integrations are later completed.
