/**
 * Submits an incident report to the server.
 */
function submitIncident() {
    // Get CSRF token from cookies
    const csrftoken = Cookies.get("csrftoken");

    // Get values from form inputs
    let incidentType = document.getElementById("incidentType").value;
    let incidentDate = document.getElementById("incidentDate").value;
    let affectedPeople = document.getElementById("affectedPeople").value;
    let incidentDescription = document.getElementById("incidentDescription").value;

    // Create request body as JSON string
    let requestBody = JSON.stringify({
        "incidentType": incidentType,
        "incidentDate": incidentDate,
        "affectedPeople": affectedPeople,
        "incidentDescription": incidentDescription
    });

    // Log request body
    console.log(requestBody);

    // Send POST request to server
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

    // Reset all form inputs to empty strings.
    $("#logForm")[0].reset();
}