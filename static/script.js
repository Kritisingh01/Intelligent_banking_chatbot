document.getElementById("send-btn").onclick = function() {
    let input = document.getElementById("user-input").value;

    fetch("/get", {
        method: "POST",
        body: JSON.stringify({message: input}),
        headers: {"Content-Type": "application/json"}
    })
    .then(res => res.json())
    .then(data => {
        let chatBox = document.getElementById("chat-box");

        chatBox.innerHTML += `<div><b>You:</b> ${input}</div>`;
        chatBox.innerHTML += `<div><b>Bot:</b> ${data.response}</div>`;
    });

    document.getElementById("user-input").value = "";
}
