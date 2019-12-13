const url = "http://18.223.108.40:5000/api/v1/deep_cite";
//const url = "http://localhost:5000/api/v1/deep_cite";
//const url = "http://localhost:5000/";
var ajax = null;
var timeout = null;

function handleClaimChange(e) {
    const fieldVal = document.getElementById(e.srcElement.id).value;
    chrome.storage.local.set({ 'claimField': fieldVal }, function () {
        console.log('claimField is set to ' + fieldVal);
    });

}

function handleLinkChange(e) {
    const fieldVal = document.getElementById(e.srcElement.id).value;
    chrome.storage.local.set({ 'linkField': fieldVal }, function () {
        console.log('linkField is set to ' + fieldVal);
    });
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#formClaimInput').addEventListener('change', handleClaimChange);
    document.querySelector('#formLinkInput').addEventListener('change', handleLinkChange);
    document.querySelector('#formClaimInput').addEventListener('paste', handleClaimChange);
    document.querySelector('#formLinkInput').addEventListener('paste', handleLinkChange);
});


$(document).ready(() => {
    chrome.storage.local.get(['state'], function(result){
        let state = result.state;
        console.log(state);

        if (state == 0){
            chrome.storage.local.get(['claimField'], function (result) {
                console.log('Value currently is ' + result.claimField);
                document.getElementById("formClaimInput").value = result.claimField;
            });
            chrome.storage.local.get(['linkField'], function (result) {
                console.log('Value currently is ' + result.linkField);
                document.getElementById("formLinkInput").value = result.linkField;
            });
        }else if (state == 1){
            chrome.storage.local.get(['lastData'], function(result){
                dataReceived(result.lastData);
            })
        }
    });


    

    //populate claim and link from storage

    $('#linxerForm').on('submit', (event) => {
        var $btn = $("button");
        $btn.button('loading');

        $('#formClaimInput').attr('readonly', true);
        $('#formLinkInput').attr('readonly', true);

        

        chrome.tabs.query({
            'active': true,
            'lastFocusedWindow': true
        }, function (tabs) {
            chrome.storage.local.set({
                'claimsrc': tabs[0].url
            }, () => {
                console.log('Setting claim source');
            });
            console.log(tabs[0].url);
        });

        event.preventDefault();
        data = {
            claim: event.target["0"].value,
            link: event.target["1"].value
        };
        console.log(JSON.stringify(data));
        sendToServer(data); //perform some operations

        var delay = 180000; // 3 minute timeout
        //var delay = 5000;
        timeout = this.setTimeout(function () {
            $("body").html(`<div id="results" class="container-fluid main">
            <h2 id="title" style="font-family: Book Antiqua">Error</h1>
            </div>`);

            $('#results').append(`
                <div class="error">
                    <p class="result-text" style="color:#8b0000">${"Error 504: Gateway Timeout"}</p>
                </div>
            `);

            ajax.abort();

        }, delay);
    });
})

function serverOffline() {
    clearTimeout(timeout)
    $("body").html(`<div id="results" class="container-fluid main">
                    <h2 id="title" style="font-family: Book Antiqua">Error</h1>
                    </div>`);

    $('#results').append(`
        <div class="error">
            <p class="result-text" style="color:#8b0000">${"Error 503: Cannot Connect to Server"}</p>
        </div>
    `);
}


function sendToServer(data) {
    ajax = $.ajax({
        type: "POST",
        url: url, // where the post request gets sent to (backend server address)
        success: dataReceived, // callback function on success
        error: serverOffline, // function if failed to connect to server
        contentType: "application/json", // exprected data type of the returned data
        data: JSON.stringify(data) // send the data json as a string
    });
}

function dataReceived(data) {

    chrome.storage.local.set({'lastData': data}, ()=>{
        console.log('Initialized previous data variable');
    });
    chrome.storage.local.set({ 'state': 1},  function(){
        console.log('Data received');
    });

    // cancel timeout
    clearTimeout(timeout)

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
                        <h2 id="title" style="font-family: Book Antiqua">Citation List</h2>
                        </div>`);
        
        //for each item in data returned:
        data.results.forEach((result, i) => {

            if(i == 0){
                $("#results").append(`
                <h5 style="font-family: Book Antiqua>You Entered</h5>
                <div class="result">
                    <p class="result-text">"${result.source}"</p>
                    <a href="${result.link}" class="card-link"><b>${result.link}</b></a>
                </div>
                <h5 style="font-family: Book Antiqua>We Found</h5>
                `);
            }else{
                $("#results").append(`
                <div class="result">
                    <p class="result-text">"${result.source}"</p>
                    <a href="${result.link}" class="card-link"><b>${result.link}</b></a>
                </div>
                `);
            }

        });

    }

    $("#results").append(`
    </br>
    <button class="btn btn-info btn-block" id="btnback" style="background-color: #7C77B9; border-color: #7C77B9; color:#EBF5EE">New Citation</button>
    `);


    //makes anchor tags open in new tab
    $('body').on('click', 'a', function () {
        chrome.tabs.create({ url: $(this).attr('href') });
        return false;
    });
    $('#btnback').on('click', function(){
        chrome.storage.local.set({ 'claimField': "" }, function () {
            console.log('Initialized claimField');
        });
        chrome.storage.local.set({ 'linkField': "" }, function () {
            console.log('Initialized linkField');
        });
        chrome.storage.local.set({ 'state': 0},  function(){
            console.log('Initialized extention state');
        });

        chrome.runtime.reload();
    })
}
