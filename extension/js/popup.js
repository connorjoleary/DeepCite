const url = "http://18.223.108.40:5000/api/v1/deep_cite";

/*const url = "http://localhost:5000/api/v1/deep_cite";
const host = "localhost";
const port = 5000;
const path = "/api/v1/deep_cite";*/



function handleClaimChange(e) {
    const fieldVal = document.getElementById(e.srcElement.id).value;
    // console.log(fieldVal);
    chrome.storage.local.set({ 'claimField': fieldVal }, function () {
        console.log('claimField is set to ' + fieldVal);
    });

}

function handleLinkChange(e) {
    const fieldVal = document.getElementById(e.srcElement.id).value;
    // console.log(fieldVal);
    chrome.storage.local.set({ 'linkField': fieldVal }, function () {
        console.log('linkField is set to ' + fieldVal);
    });
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#formClaimInput').addEventListener('change', handleClaimChange);
    document.querySelector('#formLinkInput').addEventListener('change', handleLinkChange);
});


$(document).ready(() => {

    chrome.storage.local.get(['claimField'], function (result) {
        console.log('Value currently is ' + result.claimField);
        document.getElementById("formClaimInput").value = result.claimField;
    });
    chrome.storage.local.get(['linkField'], function (result) {
        console.log('Value currently is ' + result.linkField);
        document.getElementById("formLinkInput").value = result.linkField;
    });

    //populate claim and link from storage
    // console.log("Persist store: " + );
    var delay = 1000;
    $("button").click(function() {
        var $btn = $(this);
        $btn.button('loading');
        // simulating a timeout
        setTimeout(function () {
            $btn.button('reset');
        }, delay);
    });

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
    });

    /*http.get({
        host: host, 
        port: port,
        path: path 
      }, function(res) {
        $.ajax({
            type: "POST",
            url: url, // where the post request gets sent to (backend server address)
            success: dataReceived, // callback function on success
            contentType: "application/json", // exprected data type of the returned data
            data: JSON.stringify(data) // send the data json as a string
        })

      }).on("error", function(e) {
        $("body").html(`<div id="results" class="container-fluid main">
                        <h2 id="title" style="font-family: Book Antiqua">Error</h1>
                        </div>`);

        $('#results').append(`
            <div class="error">
                <p class="result-text" style="color:#8b0000">${"Error 503: Unable to contect to server"}</p>
            </div>
        `);
      });*/
}

function dataReceived(data) {

    //prints errors:
    if(data.error) {
        console.log("Received: ", data);
        $("body").html(`<div id="results" class="container-fluid main">
                        <h2 id="title" style="font-family: Book Antiqua">Error</h1>
                        </div>`);

        $('#results').append(`
            <div class="error">
                <p class="result-text" style="color:#8b0000">${data.error}</p>
            </div>
        `);
    }
    else{ 

        // update popup with results
        console.log("Received: ", data);
        $("body").html(`<div id="results" class="container-fluid main">
                        <h2 id="title" style="font-family: Book Antiqua">Citation List</h1>
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

    }


    //makes anchor tags open in new tab
    $('body').on('click', 'a', function () {
        chrome.tabs.create({ url: $(this).attr('href') });
        return false;
    });

    // window.location.href="test.html";
    // chrome.browserAction.setPopup({popup: "test.html"});
}
