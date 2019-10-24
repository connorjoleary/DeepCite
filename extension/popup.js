let url = "127.0.0.1"


$(document).ready(() => {
    $("submit").click(data, sendToServer);
})


function sendToServer(data){
    $.ajax({
        type: "POST",
        url: url,
        success: dataReceived,
        dataType: "json",
        data: data
    })
}

function dataReceived(data){
    console.log(data);
}