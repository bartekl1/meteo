function loadCurrentReadings() {
    fetch("/api/current_reading")
        .then((response) => {
            return response.json();
        })
        .then((json) => {
            if (json.status === "ok") {
                document.querySelector("#bme280-temperature").innerHTML =
                    json.bme280.temperature.toFixed(2);
                document.querySelector("#bme280-humidity").innerHTML =
                    json.bme280.humidity.toFixed(2);
                document.querySelector("#bme280-pressure").innerHTML =
                    json.bme280.pressure.toFixed(2);
                document.querySelector("#ds18b20-temperature").innerHTML =
                    json.ds18b20.temperature.toFixed(2);
                document.querySelector("#pms5003-pm-1-0").innerHTML =
                    json.pms5003["pm1.0"];
                document.querySelector("#pms5003-pm-2-5").innerHTML =
                    json.pms5003["pm2.5"];
                document.querySelector("#pms5003-pm-10").innerHTML =
                    json.pms5003["pm10"];

                document.querySelector("#sensor-error").classList.add("d-none");
                document
                    .querySelector("#current-readings")
                    .classList.remove("d-none");
            } else if (
                json.status === "error" &&
                json.error === "sensor_error"
            ) {
                document
                    .querySelector("#current-readings")
                    .classList.add("d-none");
                document
                    .querySelector("#sensor-error")
                    .classList.remove("d-none");
            }

            document
                .querySelector("#loading-current-readings")
                .classList.add("d-none");
            document
                .querySelector("#refresh-current-readings-div")
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
            if (json.status === "ok") {
                document.querySelector("#bme280-temperature").innerHTML =
                    json.bme280.temperature.toFixed(2);
                document.querySelector("#bme280-humidity").innerHTML =
                    json.bme280.humidity.toFixed(2);
                document.querySelector("#bme280-pressure").innerHTML =
                    json.bme280.pressure.toFixed(2);
                document.querySelector("#ds18b20-temperature").innerHTML =
                    json.ds18b20.temperature.toFixed(2);
                document.querySelector("#pms5003-pm-1-0").innerHTML =
                    json.pms5003["pm1.0"];
                document.querySelector("#pms5003-pm-2-5").innerHTML =
                    json.pms5003["pm2.5"];
                document.querySelector("#pms5003-pm-10").innerHTML =
                    json.pms5003["pm10"];

                document.querySelector("#sensor-error").classList.add("d-none");
                document
                    .querySelector("#current-readings")
                    .classList.remove("d-none");
            } else if (
                json.status === "error" &&
                json.error === "sensor_error"
            ) {
                document
                    .querySelector("#current-readings")
                    .classList.add("d-none");
                document
                    .querySelector("#sensor-error")
                    .classList.remove("d-none");
            }

            document
                .querySelector("#refresh-current-readings-loading")
                .classList.add("d-none");
            document
                .querySelector("#refresh-current-readings")
                .classList.remove("d-none");
        });
}

function loadArchiveReadings(options) {
    document
        .querySelector("#archive-readings")
        .querySelector(".table-responsive")
        .classList.add("d-none");
    document
        .querySelector("#loading-archive-readings2")
        .classList.remove("d-none");

    const searchParams = new URLSearchParams(options);
    fetch(`/api/archive_readings?${searchParams.toString()}`)
        .then((response) => {
            return response.json();
        })
        .then((json) => {
            var tBody = document
                .querySelector("#archive-readings")
                .querySelector("tbody");

            tBody.innerHTML = "";

            json.forEach((e) => {
                var rowElement = document.createElement("tr");

                rowElement.setAttribute("id", e.id);
                rowElement.setAttribute("date", e.read_date);

                var idColumn = document.createElement("th");
                idColumn.scope = "row";
                idColumn.innerHTML = e.id;
                rowElement.append(idColumn);

                var dateColumn = document.createElement("td");
                dateColumn.innerHTML = new Date(e.read_time).toLocaleString();
                rowElement.append(dateColumn);

                var ds18b20Temperature = document.createElement("td");
                ds18b20Temperature.innerHTML = (e.ds18b20_temperature !== null) ? `${e.ds18b20_temperature.toFixed(
                    2
                )} ℃` : "-";
                rowElement.append(ds18b20Temperature);

                var bme280Temperature = document.createElement("td");
                bme280Temperature.innerHTML = (e.bme280_temperature !== null) ? `${e.bme280_temperature.toFixed(
                    2
                )} ℃` : "-";
                rowElement.append(bme280Temperature);

                var bme280Humidity = document.createElement("td");
                bme280Humidity.innerHTML = (e.bme280_humidity !== null) ? `${e.bme280_humidity.toFixed(2)} %` : "-";
                rowElement.append(bme280Humidity);

                var bme280Pressure = document.createElement("td");
                bme280Pressure.innerHTML = (e.bme280_pressure !== null) ? `${e.bme280_pressure.toFixed(
                    2
                )} hPa` : "-";
                rowElement.append(bme280Pressure);

                var pm1_0 = document.createElement("td");
                pm1_0.innerHTML = (e.pms5003_pm_1_0 !== null) ? `${e.pms5003_pm_1_0} μg/m³` : "-";
                rowElement.append(pm1_0);

                var pm2_5 = document.createElement("td");
                pm2_5.innerHTML = (e.pms5003_pm_2_5 !== null) ? `${e.pms5003_pm_2_5} μg/m³` : "-";
                rowElement.append(pm2_5);

                var pm10 = document.createElement("td");
                pm10.innerHTML = (e.pms5003_pm_10 !== null) ? `${e.pms5003_pm_10} μg/m³` : "-";
                rowElement.append(pm10);

                tBody.append(rowElement);
            });

            fetch(`/api/archive_readings/count`)
                .then((response) => {
                    return response.json();
                })
                .then((json) => {
                    document.querySelector(
                        "#total-pages"
                    ).innerHTML = `/ ${Math.ceil(
                        json.rows_count /
                            document.querySelector("#rows-number").value
                    )}`;
                    document
                        .querySelector("#loading-archive-readings")
                        .classList.add("d-none");
                    document
                        .querySelector("#archive-readings")
                        .classList.remove("d-none");

                    document
                        .querySelector("#loading-archive-readings2")
                        .classList.add("d-none");
                    document
                        .querySelector("#archive-readings")
                        .querySelector(".table-responsive")
                        .classList.remove("d-none");
                });
        });
}

function loadStats() {
    document.querySelector("#refresh-statistics").classList.add("d-none");
    document
        .querySelector("#refresh-statistics-loading")
        .classList.remove("d-none");

    fetch("/api/stats")
        .then((response) => {
            return response.json();
        })
        .then((json) => {
            document.querySelector("#readings-count").innerHTML =
                json.readings_count;

            document.querySelector(
                "#min-bme280-temperature"
            ).innerHTML = `${json.bme280.temperature.min.value.toFixed(
                2
            )} ℃ <br> ${new Date(
                json.bme280.temperature.min.read_time
            ).toLocaleString()} <br> #${json.bme280.temperature.min.id}`;
            document.querySelector(
                "#min-bme280-humidity"
            ).innerHTML = `${json.bme280.humidity.min.value.toFixed(
                2
            )} % <br> ${new Date(
                json.bme280.humidity.min.read_time
            ).toLocaleString()} <br> #${json.bme280.humidity.min.id}`;
            document.querySelector(
                "#min-bme280-pressure"
            ).innerHTML = `${json.bme280.pressure.min.value.toFixed(
                2
            )} hPa <br> ${new Date(
                json.bme280.pressure.min.read_time
            ).toLocaleString()} <br> #${json.bme280.pressure.min.id}`;
            document.querySelector(
                "#min-ds18b20-temperature"
            ).innerHTML = `${json.ds18b20.temperature.min.value.toFixed(
                2
            )} ℃ <br> ${new Date(
                json.ds18b20.temperature.min.read_time
            ).toLocaleString()} <br> #${json.ds18b20.temperature.min.id}`;
            document.querySelector(
                "#min-pms5003-pm1-0"
            ).innerHTML = `${json.pms5003["pm1.0"].min.value} μg/m³ <br> ${new Date(
                json.pms5003["pm1.0"].min.read_time
            ).toLocaleString()} <br> #${json.pms5003["pm1.0"].min.id}`;
            document.querySelector(
                "#min-pms5003-pm2-5"
            ).innerHTML = `${json.pms5003["pm2.5"].min.value} μg/m³ <br> ${new Date(
                json.pms5003["pm2.5"].min.read_time
            ).toLocaleString()} <br> #${json.pms5003["pm2.5"].min.id}`;
            document.querySelector(
                "#min-pms5003-pm10"
            ).innerHTML = `${json.pms5003["pm10"].min.value} μg/m³ <br> ${new Date(
                json.pms5003["pm10"].min.read_time
            ).toLocaleString()} <br> #${json.pms5003["pm10"].min.id}`;

            document.querySelector(
                "#max-bme280-temperature"
            ).innerHTML = `${json.bme280.temperature.max.value.toFixed(
                2
            )} ℃ <br> ${new Date(
                json.bme280.temperature.max.read_time
            ).toLocaleString()} <br> #${json.bme280.temperature.max.id}`;
            document.querySelector(
                "#max-bme280-humidity"
            ).innerHTML = `${json.bme280.humidity.max.value.toFixed(
                2
            )} % <br> ${new Date(
                json.bme280.humidity.max.read_time
            ).toLocaleString()} <br> #${json.bme280.humidity.max.id}`;
            document.querySelector(
                "#max-bme280-pressure"
            ).innerHTML = `${json.bme280.pressure.max.value.toFixed(
                2
            )} hPa <br> ${new Date(
                json.bme280.pressure.max.read_time
            ).toLocaleString()} <br> #${json.bme280.pressure.max.id}`;
            document.querySelector(
                "#max-ds18b20-temperature"
            ).innerHTML = `${json.ds18b20.temperature.max.value.toFixed(
                2
            )} ℃ <br> ${new Date(
                json.ds18b20.temperature.max.read_time
            ).toLocaleString()} <br> #${json.ds18b20.temperature.max.id}`;
            document.querySelector(
                "#max-pms5003-pm1-0"
            ).innerHTML = `${json.pms5003["pm1.0"].max.value} μg/m³ <br> ${new Date(
                json.pms5003["pm1.0"].max.read_time
            ).toLocaleString()} <br> #${json.pms5003["pm1.0"].max.id}`;
            document.querySelector(
                "#max-pms5003-pm2-5"
            ).innerHTML = `${json.pms5003["pm2.5"].max.value} μg/m³ <br> ${new Date(
                json.pms5003["pm2.5"].max.read_time
            ).toLocaleString()} <br> #${json.pms5003["pm2.5"].max.id}`;
            document.querySelector(
                "#max-pms5003-pm10"
            ).innerHTML = `${json.pms5003["pm10"].max.value} μg/m³ <br> ${new Date(
                json.pms5003["pm10"].max.read_time
            ).toLocaleString()} <br> #${json.pms5003["pm10"].max.id}`;

            document.querySelector(
                "#avg-bme280-temperature"
            ).innerHTML = `${json.bme280.temperature.avg.value.toFixed(2)} ℃`;
            document.querySelector(
                "#avg-bme280-humidity"
            ).innerHTML = `${json.bme280.humidity.avg.value.toFixed(2)} %`;
            document.querySelector(
                "#avg-bme280-pressure"
            ).innerHTML = `${json.bme280.pressure.avg.value.toFixed(2)} hPa`;
            document.querySelector(
                "#avg-ds18b20-temperature"
            ).innerHTML = `${json.ds18b20.temperature.avg.value.toFixed(2)} ℃`;
            document.querySelector(
                "#avg-pms5003-pm1-0"
            ).innerHTML = `${json.pms5003["pm1.0"].avg.value.toFixed(2)} μg/m³`;
            document.querySelector(
                "#avg-pms5003-pm2-5"
            ).innerHTML = `${json.pms5003["pm2.5"].avg.value.toFixed(2)} μg/m³`;
            document.querySelector(
                "#avg-pms5003-pm10"
            ).innerHTML = `${json.pms5003["pm10"].avg.value.toFixed(2)} μg/m³`;

            document.querySelector(
                "#amp-bme280-temperature"
            ).innerHTML = `${json.bme280.temperature.amp.value.toFixed(2)} ℃`;
            document.querySelector(
                "#amp-bme280-humidity"
            ).innerHTML = `${json.bme280.humidity.amp.value.toFixed(2)} %`;
            document.querySelector(
                "#amp-bme280-pressure"
            ).innerHTML = `${json.bme280.pressure.amp.value.toFixed(2)} hPa`;
            document.querySelector(
                "#amp-ds18b20-temperature"
            ).innerHTML = `${json.ds18b20.temperature.amp.value.toFixed(2)} ℃`;
            document.querySelector(
                "#amp-pms5003-pm1-0"
            ).innerHTML = `${json.pms5003["pm1.0"].amp.value} μg/m³`;
            document.querySelector(
                "#amp-pms5003-pm2-5"
            ).innerHTML = `${json.pms5003["pm2.5"].amp.value} μg/m³`;
            document.querySelector(
                "#amp-pms5003-pm10"
            ).innerHTML = `${json.pms5003["pm10"].amp.value} μg/m³`;

            document
                .querySelector("#loading-statistics")
                .classList.add("d-none");
            document.querySelector("#statistics").classList.remove("d-none");
            document
                .querySelector("#refresh-statistics-div")
                .classList.remove("d-none");
            document
                .querySelector("#refresh-statistics")
                .classList.remove("d-none");
            document
                .querySelector("#refresh-statistics-loading")
                .classList.add("d-none");
        });
}

function refreshArchiveReadings() {
    loadArchiveReadings({
        startId:
            document.querySelector("#rows-number").value *
                (document.querySelector("#page").value - 1) +
            1,
        limit: document.querySelector("#rows-number").value,
        // reverseDirection: document.querySelector("#reverse-direction").checked
        //     ? "true"
        //     : "false",
    });
}

function setFooterPadding() {
    document.querySelector("body").style.paddingBottom = `${
        document.querySelector("footer").clientHeight + 10
    }px`;
}

setFooterPadding();

window.addEventListener("resize", setFooterPadding);

loadCurrentReadings();

document
    .querySelector("#refresh-current-readings")
    .addEventListener("click", refreshCurrentReadings);

loadArchiveReadings({ limit: 20 });

document
    .querySelector("#refresh-archive-readings")
    .addEventListener("click", refreshArchiveReadings);

document.querySelectorAll(".archive-readings-settings").forEach((e) => {
    e.addEventListener("change", refreshArchiveReadings);
});

loadStats();

document
    .querySelector("#refresh-statistics")
    .addEventListener("click", loadStats);
