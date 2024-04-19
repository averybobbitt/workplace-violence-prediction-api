$(function () {
    const gaugeElement = document.getElementById("demoGauge");
    const tableElement = new DataTable("#recentData", {
        responsive: true,
        order: [[0, "desc"]]
    });

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
                updateTable(tableElement, formatHospitalData(data));
            });
        });
    }, 1000);
});

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
    // assuming "id" is first column and latest data is first row
    let top_id = Number(table.rows(0).data()[0][0]);
    let new_id = Number(data["id"]);
    let exists = false;

    // Iterate through each row in the table to check if new_id already exists
    table.rows().every(function () {
        let rowData = this.data();
        if (rowData[0] === new_id) {
            exists = true;
            return false; // Exit the loop early since we found a match
        }
    });

    if (!exists && new_id > top_id) {
        table.row.add(Object.values(data)).draw();
        table.columns.adjust().draw();
        console.log(`Updating table -- OLD: ${top_id} -- NEW: ${new_id}`);
    } else {
        console.log(`Not updating table -- OLD: ${top_id} -- NEW: ${new_id}`);
    }
}

function formatHospitalData(data) {
    let formatted;

    if (Array.isArray(data)) {
        formatted = {
            "ID": data[0],
            "Created Time": dayjs(data[1].replaceAll(".", ""), ["MMMM D, YYYY, h a", "MMMM D, YYYY, h:mm a"]).format("MM/DD/YYYY HH:mm"),
            "Average Nurses": parseFloat(data[2]).toFixed(2),
            "Average Patients": parseFloat(data[3]).toFixed(2),
            "% Beds Full": (parseFloat(data[4]) * 100).toFixed(2),
            "Time of Day": dayjs(data[5].replaceAll(".", ""), ["h a", "h:mm a"]).format("h:mm a")
        };
    } else {
        formatted = {
            "ID": data.id,
            "Created Time": dayjs(data.createdTime).format("MM/DD/YYYY HH:mm"),
            "Average Nurses": parseFloat(data.avgNurses).toFixed(2),
            "Average Patients": parseFloat(data.avgPatients).toFixed(2),
            "% Beds Full": (parseFloat(data.percentBedsFull) * 100).toFixed(2),
            "Time of Day": dayjs(data.timeOfDay, "HH:mm:ss").format("h:mm a")
        };
    }

    return formatted;
}