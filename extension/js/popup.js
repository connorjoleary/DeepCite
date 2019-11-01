let url = "http://localhost:3000"


$(document).ready(() => {

    //populate claim and link from storage

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
    $("body").html(`<div id="results" class="container-fluid main">
                    <h1 id="title">Data Recieved!</h1>
                    </div>`);
    //for each item in data returned:
    data.results.forEach(result => {
        $("#results").append(`
        <div class="result">
            <p class="result-text">"${result.source}"</p>
            <a href="${result.link}" class="card-link"><b>${result.link}</b></a>
        </div>
        `);
    });

    //makes anchor tags open in new tab
    $('body').on('click', 'a', function(){
        chrome.tabs.create({url: $(this).attr('href')});
        return false;
    });

    // window.location.href="test.html";
    // chrome.browserAction.setPopup({popup: "test.html"});
}