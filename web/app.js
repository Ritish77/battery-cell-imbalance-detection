const demo = {
  cells: [4.12, 4.11, 4.09, 4.10],
  imbalance: 0.03,
  temperature: 30.8,
  status: "NORMAL",
  actuators: { relay: "ON", fan: "OFF", buzzer: "OFF", led: "GREEN" }
};

function render(data) {
  data.cells.forEach((value, index) => {
    document.getElementById(`cell${index + 1}`).textContent = `${value.toFixed(3)} V`;
  });
  document.getElementById("imbalance").textContent = `${data.imbalance.toFixed(3)} V`;
  document.getElementById("temperature").textContent = `${data.temperature.toFixed(1)} C`;
  const status = document.getElementById("status");
  status.textContent = data.status;
  status.className = `badge ${data.status.toLowerCase()}`;
  Object.entries(data.actuators).forEach(([key, value]) => {
    document.getElementById(key).textContent = value;
  });
}

render(demo);
