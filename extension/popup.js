const url = "127.0.0.1:3000"
const bkg = chrome.extension.getBackgroundPage();
bkg.console.log("sdassdgsafdff");
document.getElementById("title").innerHTML = "TESTTE";
$(document).ready(() => {
    $("submit").click(data, sendToServer);
    console.log("sdf");
    bkg.console.log("sdasdff");
})


function sendToServer(data){
	bkg.console.log("data sent to server");
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