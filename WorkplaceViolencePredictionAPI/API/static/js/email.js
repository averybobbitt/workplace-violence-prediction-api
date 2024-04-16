window.onload = function () {
    setInterval(() => {
        fetch("http://localhost:8000/api/email").then((response) => {
            response.json().then((data) => {
                let list = data["emails"];
                if (data["emails"] == ""){
                    let list = data["emails"];
                }
                else{
                    let list = "No emails in alert mailing list."
                }
                updateEmailDisplay(list)
            });
        });
    }, 1000);
};

function addEmail(){
    let input = document.getElementById("inputBox").value
    let header = new Headers();
    header.append("email", input);
    fetch("http://localhost:8000/api/email/append/", {
        method: "POST",
        headers: header
    }).then(r => console.log(`Email added: ${input}`));
    document.getElementById("inputBox").value = "";
}

function rmEmail(){
    let input = document.getElementById("inputBox").value
    let header = new Headers();
    header.append("email", input);
    fetch("http://localhost:8000/api/email/remove/", {
        method: "POST",
        headers: header
    }).then(r => console.log(`Email removed: ${input}`));
    document.getElementById("inputBox").value = "";
}
function updateEmailDisplay(risk){
    document.getElementById("emails").innerText = risk;
}