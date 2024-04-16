window.onload = function () {
    setInterval(() => {
        fetch("http://localhost:8000/api/email").then((response) => {
            response.json().then((data) => {
                let emails = data.toString();

                updateEmailDisplay(emails);
            });
        });
    }, 1000);
};

function addEmail() {
    let input = document.getElementById("inputBox").value;
    console.log(input);
    console.log(JSON.stringify({
        "email": input
    }));

    fetch("http://localhost:8000/api/email/", {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "email": input
        })
    }).then(r => console.log(`Email added: ${input}`));
    document.getElementById("inputBox").value = "";
}

function rmEmail() {
    let input = document.getElementById("inputBox").value;

    fetch("http://localhost:8000/api/email/", {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json"
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