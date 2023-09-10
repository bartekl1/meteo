function loadCurrentReadings() {
    fetch("/api/current_reading")
        .then((response) => {
            return response.json();
        })
        .then((json) => {
            document.querySelector("#bme280-temperature").innerHTML =
                json.bme280.temperature.toFixed(2);
            document.querySelector("#bme280-humidity").innerHTML =
                json.bme280.humidity.toFixed(2);
            document.querySelector("#bme280-pressure").innerHTML =
                json.bme280.pressure.toFixed(2);
            document.querySelector("#ds18b20-temperature").innerHTML =
                json.ds18b20.temperature.toFixed(2);

            document
                .querySelector("#loading-current-readings")
                .classList.add("d-none");
            document
                .querySelector("#current-readings")
                .classList.remove("d-none");

            setInterval(refreshCurrentReadings, 30_000);
        });
}

function refreshCurrentReadings() {
    document.querySelector("#refresh-current-readings").classList.add("d-none");
    document
        .querySelector("#refresh-current-readings-loading")
        .classList.remove("d-none");
    fetch("/api/current_reading")
        .then((response) => {
            return response.json();
        })
        .then((json) => {
            document.querySelector("#bme280-temperature").innerHTML =
                json.bme280.temperature.toFixed(2);
            document.querySelector("#bme280-humidity").innerHTML =
                json.bme280.humidity.toFixed(2);
            document.querySelector("#bme280-pressure").innerHTML =
                json.bme280.pressure.toFixed(2);
            document.querySelector("#ds18b20-temperature").innerHTML =
                json.ds18b20.temperature.toFixed(2);

            document
                .querySelector("#refresh-current-readings-loading")
                .classList.add("d-none");
            document
                .querySelector("#refresh-current-readings")
                .classList.remove("d-none");
        });
}

loadCurrentReadings();

document
    .querySelector("#refresh-current-readings")
    .addEventListener("click", refreshCurrentReadings);
