function submitIncident() {
    const csrftoken = Cookies.get("csrftoken");
    let incidentType = document.getElementById("incidentType").value;
    let incidentDate = document.getElementById("incidentDate").value;
    let affectedPeople = document.getElementById("affectedPeople").value;
    let incidentDescription = document.getElementById("incidentDescription").value;

    let requestBody = JSON.stringify({
        "incidentType": incidentType,
        "incidentDate": incidentDate,
        "affectedPeople": affectedPeople,
        "incidentDescription": incidentDescription
    });

    console.log(requestBody);

    fetch("http://localhost:8000/api/log/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: requestBody
    }).then(response => {
        if (response.ok) {
            console.log(`Incident Reported.`);
        } else {
            console.error(response);
        }
    });

}

function resetForms(){
    document.getElementById("incidentType").value = '';
    document.getElementById("incidentDate").value = '';
    document.getElementById("affectedPeople").value = '';
    document.getElementById("incidentDescription").value = '';
}