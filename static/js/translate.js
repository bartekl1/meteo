const textTranslations = [
    "Stacja meteo",
    "Bieżące odczyty",
    "Temperatura",
    "Wilgotność",
    "Ciśnienie",
    "Odśwież",
    "Odczyty archiwalne",
    "Data"
];

const titleTranslations = {
    "Meteo station": "Stacja meteo",
};

const placeholdersTranslations = {};

const alternativeTextTranslations = {
    "Icon": "Ikona"
};

const elementsTitlesTranslations = {};

if (window.navigator.language.split("-")[0] == "pl") {
    document.querySelector("html").lang = "pl";

    document.querySelector("title").innerHTML =
        titleTranslations[document.querySelector("title").innerHTML];

    document.querySelectorAll("[text-id]").forEach((e) => {
        e.innerHTML = textTranslations[e.getAttribute("text-id")];
    });

    document.querySelectorAll("[placeholder]").forEach((e) => {
        e.placeholder = placeholdersTranslations[e.placeholder];
    });

    document.querySelectorAll("[alt]").forEach((e) => {
        e.alt = alternativeTextTranslations[e.alt];
    });

    document.querySelectorAll("[title]").forEach((e) => {
        e.title = elementsTitlesTranslations[e.title];
    });
}
