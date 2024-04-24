function submitIncident() {
    let incidentType = document.getElementById("incidentType").value;
    let incidentDate = document.getElementById("incidentDate").value;
    let affectedPeople = document.getElementById("affectedPeople").value;
    let incidentDescription = document.getElementById("incidentDescription").value;

    console.log(JSON.stringify({
        "incidentType": incidentType,
        "incidentDate": incidentDate,
        "affectedPeople": affectedPeople,
        "incidentDescription": incidentDescription
    }));

    fetch("http://localhost:8000/api/log/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "incidentType": incidentType,
            "incidentDate": incidentDate,
            "affectedPeople": affectedPeople,
            "incidentDescription": incidentDescription
        })
    }).then(response => {
        if (response.ok) {
            console.log(`Incident Reported.`);
        } else {
            console.log(response);
            throw new Error(`Error! status: ${response.status}`);
        }
    });
}