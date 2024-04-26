$(function () {
    setInterval(() => {
        fetch("http://localhost:8000/api/email").then((response) => {
            response.json().then((data) => {
                let emails = data.map(obj => obj.email);

                updateEmailDisplay(emails);
            });
        });
    }, 1000);
});

function addEmail() {
    const csrftoken = Cookies.get("csrftoken");
    const form = document.getElementById("email_form"); // use js instead of jquery here to give FormData constructor a valid argument
    const form_data = new FormData(form);
    // this is a quick, simple one-liner to convert an ES6 FormData object to JSON. **THIS WILL DISCARD DUPLICATE KEYS**
    const form_data_json = JSON.stringify(Object.fromEntries(form_data));

    fetch("http://localhost:8000/api/email/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: form_data_json
    }).then(r => r.json().then(j => console.log(j)));

    form.reset();
}

function rmEmail() {
    const csrftoken = Cookies.get("csrftoken");
    const form = document.getElementById("email_form"); // use js instead of jquery here to give FormData constructor a valid argument
    const form_data = new FormData(form);
    // this will discard duplicate keys, it's okay here because the email field is unique in the db
    const form_data_json = Object.fromEntries(form_data);

    // get id of object in database from email
    getRecipientByEmail(form_data_json["email"]).then(data => {
        const id = data["id"];

        fetch(`http://localhost:8000/api/email/${id}`, {
            method: "DELETE",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            }
        }).then(r => console.log(r));
    });

    form.reset();
}

function sendEmail() {
    fetch("http://localhost:8000/api/email/send/", {
        method: "GET",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json"
        }
    }).then(r => console.log(`Email sent`));
}

function updateEmailDisplay(list) {
    const emailsSpan = $("#emails");

    // If there is no <ul> tag in the span, set it to be an empty <ul>
    if (!emailsSpan.find("ul").length) {
        emailsSpan.html("<ul></ul>");
    }

    // Select the <ul> tag within the span
    const ul = emailsSpan.find("ul");

    // Clear any previous list items
    ul.empty();

    // For each email in the list
    list.forEach(email => {
        // Create a list element
        const li = $("<li>").text(email);

        // Append list element to the <ul>
        ul.append(li);
    });
}


async function getRecipientByEmail(email) {
    try {
        const response = await fetch(`http://localhost:8000/api/email?email=${email}`);
        if (!response.ok) throw new Error(await response.json());
        return await response.json();
    } catch (error) {
        console.error("Error fetching data:", error);
        return null;
    }
}