$(function () {
    const gaugeElement = document.getElementById("demoGauge");
    const tableElement = new DataTable("#recentData", {
        responsive: true,
        order: [[0, "desc"]]
    });

    // Add title to table
    const firstTableHeaderElement = $("#recentData_wrapper .dt-layout-row:first > .dt-start");
    const titleHTML = "<div class='dt-layout-cell dt-mid' id='tableTitle'><div class='dt-length'><h2>Recent Data</h2></div></div>";
    firstTableHeaderElement.after(titleHTML);

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

function updateRisk(risk, probability) {
    const element = document.getElementById("riskYN");

    if (risk || probability > 0.60) {
        element.innerText = "YES";
        element.style.color = "red";
    } else if (!risk) {
        element.innerText = "NO";
        element.style.color = "rgb(44, 241, 44)";
    } else {
        element.innerText = "ERROR";
        element.style.removeProperty("color");
    }
}

function updateGauge(gauge, data) {
    let risk = data["wpvRisk"];

    let probability = (parseFloat(data["wpvProbability"]) + Math.random()).toFixed(2);

    if (probability < 0 || probability > 1) return;


    gauge.querySelector(".gauge_fill").style.transform = `rotate(${probability / 2}turn)`;
    gauge.querySelector(".gauge_percentage").innerText = Math.round(probability * 100);
    updateRisk(risk, probability);

    console.log(`Prediction ${data["id"]}: ${probability}`);
}

function updateTable(table, data) {
    // assuming "id" is first column and latest data is first row
    let top_id;
    try {
        top_id = Number(table.rows(0).data()[0][0]);
    } catch {
        top_id = 0;
    }

    let new_id = Number(data.id);
    let exists = false;

    // Iterate through each row in the table to check if new_id already exists
    table.rows().every(function () {
        let rowData = this.data();
        if (rowData[0] === new_id) {
            exists = true;
            return false; // Exit the loop early since we found a match
        }
    });

    console.log(data);

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
            "id": data[0],
            "createdTime": dayjs(data[1].replaceAll(".", ""), ["MMMM D, YYYY, h a", "MMMM D, YYYY, h:mm a"]).format("MM/DD/YYYY HH:mm:ss"),
            "avgNurses": parseFloat(data[2]).toFixed(2),
            "avgPatients": parseFloat(data[3]).toFixed(2),
            "percentBedsFull": (parseFloat(data[4]) * 100).toFixed(2),
            "timeOfDay": dayjs(data[5].replaceAll(".", ""), ["h a", "h:mm a"]).format("HH:mm:ss")
        };
    } else {
        formatted = {
            "id": data.id,
            "createdTime": dayjs(data.createdTime).format("MM/DD/YYYY HH:mm:ss"),
            "avgNurses": parseFloat(data.avgNurses).toFixed(2),
            "avgPatients": parseFloat(data.avgPatients).toFixed(2),
            "percentBedsFull": (parseFloat(data.percentBedsFull) * 100).toFixed(2),
            "timeOfDay": data.timeOfDay
        };
    }

    return formatted;
}