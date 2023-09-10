if (
    window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: dark)").matches
) {
    document.querySelector("html").setAttribute("data-bs-theme", "dark");
} else {
    document.querySelector("html").setAttribute("data-bs-theme", "light");
}

window
    .matchMedia("(prefers-color-scheme: dark)")
    .addEventListener("change", (event) => {
        document
            .querySelector("html")
            .setAttribute("data-bs-theme", event.matches ? "dark" : "light");
    });
