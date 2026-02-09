const toggle = document.getElementById("themeToggle");
toggle.addEventListener("change", () => {
    document.body.classList.toggle("dark");
});

function searchVehicle() {
    const regNo = document.getElementById("regNo").value.trim().toUpperCase();
    const result = document.getElementById("result");
    const error = document.getElementById("error");
    const spinner = document.getElementById("spinner");

    result.innerHTML = "";
    error.textContent = "";

    if (!regNo) {
        error.textContent = "Please enter registration number";
        return;
    }

    spinner.style.display = "block";

    fetch("/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ registration_number: regNo })
    })
    .then(res => res.json())
    .then(data => {
        spinner.style.display = "none";

        if (data.error) {
            error.textContent = data.error;
            return;
        }

        for (const key in data) {
            const div = document.createElement("div");
            div.className = "card";
            div.innerHTML = `<span>${key}</span><p>${data[key]}</p>`;
            result.appendChild(div);
        }
    })
    .catch(() => {
        spinner.style.display = "none";
        error.textContent = "Something went wrong";
    });
}
