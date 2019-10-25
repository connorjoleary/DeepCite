const url = "127.0.0.1:3000"
// $(document).ready(() => {
//     $("submit").click(data, sendToServer);
//     console.log("sdf");
// })


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



// function dataReceived(data){
//     console.log(data);
// }

function main() {
	document.getElementById("title").innerHTML = "TESTTE";
}

// Add event listeners once the DOM has fully loaded by listening for the
// `DOMContentLoaded` event on the document, and adding your listeners to
// specific elements when it triggers.
document.addEventListener('DOMContentLoaded', function () {
  // document.querySelector('button').addEventListener('click', clickHandler);
  console.log("js is linked");
  main();
});

// document.addEventListener('DOMContentLoaded', function () {
//   document.querySelector('button').addEventListener('click', clickHandler);
//   main();
// });