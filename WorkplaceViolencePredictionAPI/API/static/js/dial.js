window.onload = function () {
    const gaugeElement = document.getElementById("demoGauge");

    setInterval(() => {
        fetch("http://localhost:8000/api/model/latest").then((response) => {
            response.json().then((data) => {
                let probability = data["wpvProbability"];
                setGaugeValue(gaugeElement, probability.toFixed(2));
                console.log(data);
            });
        });
    }, 5000);
};

function setGaugeValue(gauge, value) {
    if (value < 0 || value > 1) return;

    gauge.querySelector(".gauge_fill").style.transform = `rotate(${value / 2}turn)`;
    gauge.querySelector(".gauge_percentage").innerText = Math.round(value * 100);
}

function changeNum() {
    const randomNum = Math.random().toFixed(2);
    const degrees = Math.round((randomNum / 100) * 180);
    const root = document.querySelector(":root");
    let title = document.querySelector(".loader__title");

    let currentNumber = title.innerText;

    setInterval(() => {
        if (currentNumber < randomNum) {
            currentNumber++;
            title.innerText = currentNumber;
        } else if (currentNumber > randomNum) {
            currentNumber--;
            title.innerText = currentNumber;
        }
    }, 3);

    root.style.setProperty("--rotation", `${degrees}deg`);
}

