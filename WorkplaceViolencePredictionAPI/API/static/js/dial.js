window.onload = function () {
    const gaugeElement = document.getElementById("demoGauge");

    /*
    Skeleton code for a HTTP GET request to the PredictionModelViewset.

    fetch(http://127.0.0.1:8000/api/model/, {
      method: "GET" // default, so we can ignore
    })

    Next, I will need to figure out how to store this inside a variable and replace Math.random().toFixed(2)
        with the prediction value made by the API call.
    */

    setInterval(() => {
        setGaugeValue(gaugeElement, Math.random().toFixed(2));
    }, 2000);
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

