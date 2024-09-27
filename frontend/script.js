document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("file-input");
    const preview = document.getElementById("preview");
    const predictBtn = document.getElementById("predict-btn");
    const predictionsDiv = document.getElementById("predictions");
    const highestProbabilitySpan = document.getElementById("highest-probability");
    const modal = document.getElementById("modal");
    const closeModal = document.querySelector(".close");
    const modalImage = document.getElementById("modal-image");
    const predictedClass = document.getElementById("predicted-class");
    const descriptionElem = document.getElementById("description");
    const modalProbability = document.getElementById("modal-probability");

    let selectedImage = null;
    let predictions = [];

    const diseaseDescriptions = {
        Catarata: "La Catarata es una opacidad del cristalino del ojo...",
        "Retinopatía Diabética": "La Retinopatía Diabética es una complicación...",
        Glaucoma: "El Glaucoma es un grupo de enfermedades oculares...",
        "Ojo Normal": "No muestra signos de enfermedades oculares...",
    };

    const getProgressColor = (percentage) => {
        if (percentage > 70) return "#73D13D"; // Verde
        if (percentage > 20) return "#FFEC3D"; // Amarillo
        return "#FF4D4F"; // Rojo
    };

    fileInput.addEventListener("change", (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                selectedImage = e.target.result;
                preview.src = selectedImage;
                predictBtn.disabled = false;
            };
            reader.readAsDataURL(file);
        }
    });

    predictBtn.addEventListener("click", function () {
        if (!selectedImage) return;

        predictionsDiv.innerHTML = "";
        modalImage.src = selectedImage;

        // Simular predicciones
        predictions = [
            { class: "Catarata", probability: 0.85 },
            { class: "Retinopatía Diabética", probability: 0.6 },
            { class: "Glaucoma", probability: 0.25 },
        ];

        let highestProbability = predictions[0];

        predictions.forEach((prediction) => {
            const bar = document.createElement("div");
            bar.classList.add("progress-bar");
            const fill = document.createElement("div");
            fill.classList.add("progress-fill");
            fill.style.width = prediction.probability * 100 + "%";
            fill.style.backgroundColor = getProgressColor(
                prediction.probability * 100
            );
            bar.appendChild(fill);
            predictionsDiv.appendChild(bar);

            const label = document.createElement("span");
            label.innerText = `${prediction.class}: ${(
                prediction.probability * 100
            ).toFixed(2)}%`;
            predictionsDiv.appendChild(label);

            if (prediction.probability > highestProbability.probability) {
                highestProbability = prediction;
            }
        });

        highestProbabilitySpan.textContent = `${highestProbability.class} (${(
            highestProbability.probability * 100
        ).toFixed(2)}%)`;

        predictedClass.textContent = highestProbability.class;
        descriptionElem.textContent = diseaseDescriptions[highestProbability.class];
        modalProbability.textContent =
            (highestProbability.probability * 100).toFixed(2) + "%";

        modal.style.display = "block";
    });

    closeModal.onclick = function () {
        modal.style.display = "none";
    };

    window.onclick = function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    };
});
