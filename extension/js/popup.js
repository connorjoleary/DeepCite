const url = "https://us-central1-deepcite-306405.cloudfunctions.net/deepcite";
//const url = "http://localhost:5000/api/v1/deep_cite";
//const url = "http://localhost:5000/";
var ajax = null;
const stageValue = 'dev'
const num_results_displayed = 5
var timeout = null;

if (!deepCite) {
	var deepCite = {};
}
deepCite.citationWindow = document.getElementById("citation-list-modal");
deepCite.deepCiteWindow = document.getElementById("deep-cite-modal");
deepCite.errorWindow = document.getElementById("error-modal");

deepCite.errorMessageTextTag = document.getElementById("error-message-text");
deepCite.submitButton = document.getElementById("btnsubmit");
deepCite.formClaimInput = document.getElementById("formClaimInput");
deepCite.formLinkInput = document.getElementById("formLinkInput");
deepCite.citationResults = document.getElementById("results");

function hideAllWindows() {
	deepCite.citationWindow.style = "display: none;";
	deepCite.deepCiteWindow.style = "display: none;";
	deepCite.errorWindow.style = "display: none;";
	deepCite.errorMessageTextTag.value = null;
}

function showCitationWindow() {
	hideAllWindows();
	// clear previous citation results (remove innerHTML in the future)
	deepCite.citationResults.innerHTML = "";
	deepCite.citationWindow.style = null;
}
function showDeepCiteWindow() {
	hideAllWindows();
	enableCiteActions();
	deepCite.deepCiteWindow.style = null;
}
function showErrorWindowWithMessage(errorMessage) {
	hideAllWindows();
	// response error message is HTML, and should be changed to strictly text.
	// innerHTML needs to be removed to avoid cross-site scripting.
	deepCite.errorMessageTextTag.innerHTML = errorMessage;
	deepCite.errorWindow.style = null;
}

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
	deepCite.formClaimInput.addEventListener('change', handleClaimChange);
	deepCite.formLinkInput.addEventListener('change', handleLinkChange);
	deepCite.formClaimInput.addEventListener('paste', handleClaimChange);
	deepCite.formLinkInput.addEventListener('paste', handleLinkChange);
});

$(document).ready(() => {
	chrome.storage.local.get(['state'], function (result) {
		let state = result.state;
		console.log(state);

		if (state == 0) {
			chrome.storage.local.get(['claimField'], function (result) {
				console.log('Value currently is ' + result.claimField);
				deepCite.formClaimInput.value = result.claimField;
			});
			chrome.storage.local.get(['linkField'], function (result) {
				console.log('Value currently is ' + result.linkField);
				deepCite.formLinkInput.value = result.linkField;
			});
		} else if (state == 1) {
			chrome.storage.local.get(['lastData'], function (result) {
				dataReceived(result.lastData);
			})
		}
	});

	//makes anchor tags open in new tab
	$('body').on('click', 'a', function () {
		chrome.tabs.create({ url: $(this).attr('href') });
		return false;
	});
	// we cannot strictly call functions with an onclick attribute from an html tag, so we must create ids for each button separately
	$('#btnback-citation').on('click', function () {
		newCitationButtonClicked();
	});
	$('#btnback-error').on('click', function () {
		newCitationButtonClicked();
	});

	//populate claim and link from storage
	$('#linxerForm').on('submit', (event) => {

		var claimValue = event.target["0"].value;
		var linkValue = event.target["1"].value;

		// wait for both fields to be filled out
		if (!claimValue || !linkValue) {
			return;
		}

		disableCiteActions();

		event.preventDefault();
		sendToServer(claimValue, linkValue); //perform some operations

		var delay = 1440000; //180000 is a 3 minute timeout
		timeout = this.setTimeout(function () {
			ajax.abort();
			chrome.storage.local.set({ 'state': 0 }, function () {
				console.log('Initialized extention state');
			});
		}, delay);
	});
})

function disableCiteActions() {
	deepCite.formClaimInput.readOnly = true;
	deepCite.formLinkInput.readOnly = true;

	deepCite.submitButton.disabled = true;
	deepCite.submitButton.classList.add("btn-disabled");
	deepCite.submitButton.innerText = "loading...";
}

function enableCiteActions() {
	deepCite.formClaimInput.readOnly = false;
	deepCite.formClaimInput.value = "";

	deepCite.formLinkInput.readOnly = false;
	deepCite.formLinkInput.value = "";

	deepCite.submitButton.disabled = false;
	deepCite.submitButton.classList.remove("btn-disabled");
	deepCite.submitButton.innerText = "Cite";
}

function serverOffline() {
	clearTimeout(timeout);
	var serverOfflineErrorMessage = "Error 503: Cannot Connect to Server.";
	showErrorWindowWithMessage(serverOfflineErrorMessage);

	chrome.storage.local.set({ 'state': 0 }, function () {
		console.log('Initialized extention state');
	});
}

async function grab_ip() {
	const response = await fetch('http://api.ipify.org/?format=json');
    const data = await response.json();
    return data.ip;
}

async function sendToServer(claimValue, linkValue) {
	var ipValue = await grab_ip();

	var data = {
		claim: claimValue,
		link: linkValue,
		ip: ipValue,
		stage: stageValue
	};
	console.log(JSON.stringify(data));

	// Code used to run locally
	data['test']=true
	ajax = $.ajax({
		type: "POST",
		url: "http://localhost:8001/test/deepcite", // where the post request gets sent to (backend server address)
		crossDomain: true,
		success: dataReceived, // callback function on success
		error: serverOffline, // function if failed to connect to server
		contentType: "application/json",
		data: JSON.stringify(data) // send the data json as a string
	});

	// ajax = $.ajax({
	// 	type: "POST",
	// 	url: url, // where the post request gets sent to (backend server address)
	// 	crossDomain: true,
	// 	success: dataReceived, // callback function on success
	// 	error: serverOffline, // function if failed to connect to server
	// 	contentType: "application/json",
	// 	data: JSON.stringify(data) // send the data json as a string
	// });
}

function sort_response(results) {
	results.sort(function (a, b) {
		return ((a.score >= b.score) ? -1 : 1);
	})

	return results.slice(0, num_results_displayed);
}


function dataReceived(data) {
	chrome.storage.local.set({ 'lastData': data }, () => {
		console.log('Initialized previous data variable');
	});
	chrome.storage.local.set({ 'state': 1 }, function () {
		console.log('Data received');
		console.log(data)
	});

	// cancel timeout
	clearTimeout(timeout)
	
	response = data

	//prints errors:
	if (!!response.error && response.error !== "none") {
		showErrorWindowWithMessage(response.error);
	}
	else {
		showCitationWindow();
		//for each item in data returned, populate results
		if (!!response.results && !!response.results.length) {
			displayed_response = sort_response(response.results)
			populateCitationResults(displayed_response);
		}
	}
}

function newCitationButtonClicked() {
	chrome.storage.local.set({ 'claimField': "" }, function () {
		console.log('Initialized claimField');
	});
	chrome.storage.local.set({ 'linkField': "" }, function () {
		console.log('Initialized linkField');
	});
	chrome.storage.local.set({ 'state': 0 }, function () {
		console.log('Initialized extention state');
	});
	showDeepCiteWindow();
}

function populateCitationResults(results) {
	results.forEach((result, i) => {
		var resultSectionHtml = `<div class="form-section">`;

		if (i == 0) {
			resultSectionHtml += `<div class="form-group-title">Original Claim</div>`;
		}
		if (i == 1) {
			resultSectionHtml += `<div class="form-group-title">We Found</div>`;
		}
		resultSectionHtml += `
					<div class="form-field">
						<div class="result-text">Score: ${result.score}</div>
						<div class="result-text">"${result.source}"</div>
						<a href="${result.link}" class="result-link">${result.link}</a>
					</div>
				</div>
				`;
		$("#results").append(resultSectionHtml);
	});
}
