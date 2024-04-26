$(function () {
    setInterval(() => {
        fetch("http://localhost:8000/api/email").then((response) => {
            response.json().then((data) => {
                let emails = data.toString();

                updateEmailDisplay(emails);
            });
        });
    }, 1000);
});

function addEmail() {
    const csrftoken = Cookies.get("csrftoken");
    let input = document.getElementById("inputBox").value;

    console.log(input);
    console.log(JSON.stringify({
        "email": input
    }));

    fetch("http://localhost:8000/api/email/", {
        method: "PUT",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            "email": input
        })
    }).then(r => console.log(`Email added: ${input}`));
    document.getElementById("inputBox").value = "";
}

function rmEmail() {
    const csrftoken = Cookies.get("csrftoken");
    let input = document.getElementById("inputBox").value;

    fetch("http://localhost:8000/api/email/", {
        method: "DELETE",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            "email": input
        })
    }).then(r => console.log(`Email removed: ${input}`));
    document.getElementById("inputBox").value = "";
}

function updateEmailDisplay(list) {
    document.getElementById("emails").innerHTML = list.replace(",", "<br>");
}