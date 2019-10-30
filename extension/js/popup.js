let url = "http://localhost:3000"


$(document).ready(() => {
    //data = {claim:"abc", link:"asdf"}; //dummy data
    //$("#btnsubmit").click(data, sendToServer);
    $('#linxerForm').on('submit', (event) => {
        event.preventDefault();
        data = {
            claim: event.target["0"].value,
            link: event.target["1"].value
        };
        sendToServer(data); //perform some operations
    });
})


function sendToServer(data) {
    $.ajax({
        type: "POST",
        url: url, // where the post request gets sent to (backend server address)
        success: dataReceived, // callback function on success
        contentType: "application/json", // exprected data type of the returned data
        data: JSON.stringify(data) // send the data json as a string
    })
}

function dataReceived(data) {
    // update popup with results
    console.log("Received: ", data);
    $("body").html(`<div class="container-fluid main">
                    <h2 id="title">Data Recieved!</h2>
                    </div>`);
    //for each item in data returned:
    $("body").append(`<div><p>${data.claim}</p></div>`);
    
    // window.location.href="test.html";
    // chrome.browserAction.setPopup({popup: "test.html"});
}