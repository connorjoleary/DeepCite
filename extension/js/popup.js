let url = "http://localhost:3000"


$(document).ready(() => {
    //data = {claim:"abc", link:"asdf"}; //dummy data
    //$("#btnsubmit").click(data, sendToServer);
    $('#linxerForm').on('submit', (event) => {
        event.preventDefault();
        data = {
                claim:event.target["0"].value, 
                link:event.target["1"].value
                };
        sendToServer(data); //perform some operations
    });
})


function sendToServer(data){
    $.ajax({
        type: "POST",
        url: url,
        success: dataReceived,
        contentType: "application/json",
        data: JSON.stringify(data)
    })
}

function dataReceived(data){
    // update popup with results
    console.log("Received: ", data);
}