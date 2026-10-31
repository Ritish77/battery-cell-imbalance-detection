# Battery Cell Imbalance Detection

Software-only battery monitoring project for four-cell telemetry, imbalance detection, actuator decision logic, InfluxDB storage, and a Vercel-ready dashboard.

## Architecture

```text
Python simulator or sensors -> Mosquitto MQTT -> Python receiver -> InfluxDB -> Grafana
                                                         |
                                                         +-> Vercel dashboard API contract
```

The default local MQTT topic is `battery/device01/raw`. The receiver expects JSON containing four cell voltages, pack current, and four cell temperatures. The Vercel frontend is a static dashboard shell that can display demo data now and can be connected to a hosted read-only API later.

## Repository contents

- `backend/battery_analysis.py` - pure analysis and actuator rules.
- `backend/mqtt_receiver.py` - MQTT subscription and InfluxDB persistence.
- `backend/battery_simulator.py` - safe software telemetry generator.
- `backend/requirements.txt` - Python dependencies.
- `grafana/battery-dashboard.json` - starter Grafana dashboard definition.
- `web/` - static Vercel dashboard frontend.
- `docs/PROJECT_REPORT.md` - project methodology, requirements, testing and limitations.

## Local backend setup

1. Install Python 3.11 or newer and Mosquitto.
2. Create a virtual environment and install `backend/requirements.txt`.
3. Copy `.env.example` to `.env` and set the local InfluxDB token.
4. Start InfluxDB and Mosquitto.
5. Run `python backend/mqtt_receiver.py`.
6. In a second terminal run `python backend/battery_simulator.py`.

The project uses environment variables for credentials. Do not commit `.env`.

## Vercel deployment

Import this repository into Vercel and set the project root to `web`. The static frontend does not contain credentials and does not run an MQTT loop. To show live data, deploy a separate authenticated read-only API that queries InfluxDB and set `VITE_BATTERY_API_URL` to that endpoint.

## Scope

This repository models a software prototype. It does not claim physical ESP32 hardware, a real battery pack, safety certification, or a production cloud deployment.

## License

MIT License. Add the project owner name and year before publishing if required by your institution.
