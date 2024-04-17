window.onload = function () {
    const gaugeElement = document.getElementById("demoGauge");
    const tableElement = document.getElementById("recentData");

    setInterval(() => {
        fetch("http://localhost:8000/api/model/latest").then((response) => {
            response.json().then((data) => {
                updateGauge(gaugeElement, data);
            });
        });
    }, 1000);

    setInterval(() => {
        fetch("http://localhost:8000/api/data/latest").then((response) => {
            response.json().then((data) => {
                updateTable(tableElement, data);
            });
        });
    }, 1000);
};

function updateRisk(risk) {
    const element = document.getElementById("riskYN");

    if (risk) {
        element.innerText = "YES";
        element.style.color = "red";
    } else if (!risk) {
        element.innerText = "NO";
        element.style.color = "green";
    } else {
        element.innerText = "ERROR";
        element.style.removeProperty("color");
    }
}

function updateGauge(gauge, data) {
    let risk = data["wpvRisk"];
    let probability = parseFloat(data["wpvProbability"]).toFixed(2);

    if (probability < 0 || probability > 1) return;

    gauge.querySelector(".gauge_fill").style.transform = `rotate(${probability / 2}turn)`;
    gauge.querySelector(".gauge_percentage").innerText = Math.round(probability * 100);
    updateRisk(risk);

    // console.log(`Prediction ${data["id"]}: ${probability}`);
}

function updateTable(table, data) {
    let top_row = table.querySelector("tbody tr:first-child");
    // assuming "id" is first column
    let top_id = top_row.querySelector("td:first-child").innerText;
    let new_id = data["id"];

    let top_id_int = Number(top_id);
    let new_id_int = Number(new_id);

    if (new_id_int > top_id_int) {
        const tbody = table.querySelector("tbody");
        let row = tbody.insertRow(0);

        let i = 0; // enumerated for-in loop
        for (let [key, value] of Object.entries(data)) {
            let cell = row.insertCell(i);
            cell.innerHTML = value;
            i++;
        }

        console.log(`Updating table -- OLD: ${top_id_int} -- NEW: ${new_id_int}`);
    } else {
        console.log(`Not updating table -- OLD: ${top_id_int} -- NEW: ${new_id_int}`);
    }
}