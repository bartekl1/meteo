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

                var bme280Temperature = document.createElement("td");
                bme280Temperature.innerHTML = `${e.bme280_temperature.toFixed(
                    2
                )} ℃`;
                rowElement.append(bme280Temperature);

                var bme280Humidity = document.createElement("td");
                bme280Humidity.innerHTML = `${e.bme280_humidity.toFixed(2)} %`;
                rowElement.append(bme280Humidity);

                var bme280Pressure = document.createElement("td");
                bme280Pressure.innerHTML = `${e.bme280_pressure.toFixed(
                    2
                )} hPa`;
                rowElement.append(bme280Pressure);

                var ds18b20Temperature = document.createElement("td");
                ds18b20Temperature.innerHTML = `${e.ds18b20_temperature.toFixed(
                    2
                )} ℃`;
                rowElement.append(ds18b20Temperature);

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

function refreshArchiveReadings() {
    loadArchiveReadings({
        startId:
            document.querySelector("#rows-number").value *
                (document.querySelector("#page").value - 1) +
            1,
        limit: document.querySelector("#rows-number").value,
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
