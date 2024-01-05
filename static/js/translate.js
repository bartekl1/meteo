const textTranslations = [
    "Stacja meteo",
    "Bieżące odczyty",
    "Temperatura",
    "Wilgotność",
    "Ciśnienie",
    "Odśwież",
    "Odczyty archiwalne",
    "Data",
    "Wersja",
    "Autor",
    "Profil GitHub",
    "Repozytorium GitHub",
    "Dokumentacja",
    "Biblioteki",
    "Rejestr zmian",
    "Błąd odczytu czujników",
    "Odwróć kolejność",
    "Statystyki",
    "Ilość odczytów:",
    "Minimalna",
    "Maksymalna",
    "Średnia",
    "Amplituda",
    "Podziękowania",
];

const titleTranslations = {
    "Meteo station": "Stacja meteo",
};

const placeholdersTranslations = {};

const alternativeTextTranslations = {
    Icon: "Ikona",
};

const elementsTitlesTranslations = {};

if (window.navigator.language.split("-")[0] == "pl") {
    document.querySelector("html").lang = "pl";

    document.querySelector("title").innerHTML =
        titleTranslations[document.querySelector("title").innerHTML];

    document.querySelector("link[rel=manifest]").href = "/manifest_pl.json";

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

    document.querySelector("#acknowledgements-link").href = "https://github.com/bartekl1/meteo/blob/main/ACKNOWLEDGEMENTS_PL.md";
    document.querySelector("#changelog-link").href = "https://github.com/bartekl1/meteo/blob/main/CHANGELOG_PL.md";
}
