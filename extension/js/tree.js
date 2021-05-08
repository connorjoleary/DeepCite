/*
 *	DeepCite Source Tree page 
*/

var timeout = null;
var baseId = null;

if (!deepCite) {
	var deepCite = {};
}
// DOM elements
deepCite.citeComponent = document.getElementsByClassName("generated-cite-box")[0];
deepCite.claimComponent = document.getElementsByClassName("generated-claim-box")[0];
deepCite.treeContainer = document.getElementById("tree-container");
deepCite.canvasElement = document.getElementById("canvas-element");
deepCite.donateButton = document.getElementsByClassName('button-donate')[0];

// Unable to use onclick in HTML: https://stackoverflow.com/questions/36324333/refused-to-execute-inline-event-handler-because-it-violates-csp-sandbox
deepCite.donateButton.addEventListener("click", donateButtonClicked);

// initialization function
function init() {
	// var data = generateTestData();
	var data = gatherData();
	// populateDataIntoTree(data);
}

function gatherData() {
	chrome.storage.local.get(['state'], function (result) {
		let state = result.state;
		console.log(state);

		if (state == 1) {
			chrome.storage.local.get(['lastData'], function (result) {
				populateDataIntoTree(result.lastData.results);
			})
		} else {
			// TODO make this actually do something different
			console.log("WARN: State not accepted");
			chrome.storage.local.get(['lastData'], function (result) {
				populateDataIntoTree(result.lastData.results);
			})
		}
	});

}

function generateTestData() {
	var record, parentRecordID, randomTextCount, enforcedMaximumChildrenBool, maximumChildrenCount;
	var text = "";
	var runningRecordID = 1;
	var randomText = "lorem ipsum dolor ";
	var testData = [];
	// random number 3-15
	var randomCount = (Math.floor(Math.random() * 13) + 3);

	while (randomCount > 0) {
		// a random cite with a lower id.  if citeID = 1, parentCiteID = 0
		if (runningRecordID === 1) {
			parentRecordID = 0;
		}
		// enforce maximum children limit (currently 3)
		else {
			var enforcedMaximumChildrenBool = false;
			while (!enforcedMaximumChildrenBool) {
				parentRecordID = Math.floor(Math.random() * (runningRecordID - 1) + 1);
				maximumChildrenCount = testData.filter(function (createdCite) {
					return createdCite.parentCiteID === parentRecordID;
				}).length;
				// if we're trying to create a fourth children to a parent cite, we need to pick a different parent
				if (maximumChildrenCount < 3) {
					enforcedMaximumChildrenBool = true;
				}
			}
		}
		text = "";
		// get a random amount of text
		randomTextCount = (Math.floor(Math.random() * 10) + 1);
		while (randomTextCount > 0) {
			text = text + "" + randomText;
			randomTextCount--;
		}
		record = {
			citeID: runningRecordID,
			parentCiteID: parentRecordID,
			link: "https://www.google.com/search?rlz=1C1CHBF_enUS897US897&sxsrf=ALeKk00tGtiAE0FRqCZBEMQggSU9STLJBA%3A1593977105987&ei=ESkCX8ntO8e6tAaZy5ugCg&q=deepCite&oq=deepCite&gs_lcp=CgZwc3ktYWIQAzoECCMQJzoFCAAQkQI6BAgAEEM6BQgAELEDOgIIADoHCAAQsQMQQzoECAAQClC0EljjG2DLHGgAcAB4AYAB9wKIAcwHkgEHNi4xLjAuMZgBAKABAaoBB2d3cy13aXo&sclient=psy-ab&ved=0ahUKEwiJurq567bqAhVHHc0KHZnlBqQQ4dUDCAw&uact=5",
			score: Math.floor(Math.random() * 100) + 1, // 1-100
			source: text
		}
		testData.push(record);
		runningRecordID++;
		randomCount--;
	}
	return testData;
}

function donateButtonClicked() {
	console.log("donate clicked");
	chrome.tabs.create({ url: "https://github.com/connorjoleary/DeepCite#donate" });
}

async function grab_ip() {
	const response = await fetch('http://api.ipify.org/?format=json');
	const data = await response.json();
	return data.ip;
}

async function upvoteButtonClicked(event) {
	var ipValue = await grab_ip();

	var element = event.srcElement
	var citeID = findClosestCiteID(element);

	data = {
		type: "source",
		ip: ipValue,
		sourceId: citeID,
		baseId: baseId,
		stage: stageValue
	}
	console.log("upvote clicked on citeID " + citeID);

	// disable button
	element.classList.add("btn-disabled");
	element.innerText = "Sending...";

	// Submit feedback

	// Code used to run locally
	data['test'] = true

	ajax = $.ajax({
		type: "POST",
		url: url, // where the post request gets sent to (backend server address)
		crossDomain: true,
		success: dataReceived(element), // callback function on success
		error: serverOffline, // function if failed to connect to server
		contentType: "application/json",
		timeout: 60000, //1 minute timeout
		data: JSON.stringify(data) // send the data json as a string
	});
}

function serverOffline() {
	var serverOfflineErrorMessage = "Error 503: Cannot Connect to Server.";
	console.log(serverOfflineErrorMessage)

	element.innerText = "error";
}

function dataReceived(element, data) {
	response = data

	console.log("Returned data:", data)

	element.innerText = "Recorded!";
	element.style.color = "#45ff45";
}

function findClosestCiteID(element) {
	var citeBox = element.closest(".generated-cite-box");
	if (!!citeBox) {
		return citeBox.id;
	}
	// return null if nothing is found
}

function populateDataIntoTree(data) {
	var clonedCiteBox, populatedCiteBox, groupedData, sortedGroupedData;
	var rowCiteCount = 1;
	// first, we need to group our citations by parentCiteID
	groupedData = groupCiteData(data);
	// next, we want to sort our data so the flow chart is clean after drawing lines
	sortedGroupedData = sortCiteData(groupedData);
	// then, we need to create cite/claim boxes for each item and put them in the correct row
	sortedGroupedData.forEach(function (dataGroup) {
		rowCiteCount = dataGroup.length;
		dataGroup.forEach(function (item) {
			if (!item.parentCiteID) {
				// this is our parent node
				clonedCiteBox = deepCite.claimComponent.cloneNode(true);
				populatedCiteBox = populateDataIntoCiteBox(clonedCiteBox, item);
				baseId = item["citeID"];
			}
			else {
				clonedCiteBox = deepCite.citeComponent.cloneNode(true);
				populatedCiteBox = populateDataIntoCiteBox(clonedCiteBox, item);

				// This would be better to do once when the original is created, but idk where that is
				var voteNode = populatedCiteBox.getElementsByClassName("vote-button")[0];
				voteNode.addEventListener("click", upvoteButtonClicked);

				// calculate box width by checking the rowCiteCount value. 4em is 2em padding on left and right of all cite boxes
				populatedCiteBox.style = "width: calc(" + (100 / rowCiteCount) + "% - 4em);";
			}
			// add the cite/claim box to the DOM
			deepCite.treeContainer.appendChild(populatedCiteBox);
		});
	});
	// we need to make sure we are scrolled all the way up so the lines draw correctly
	forceScrollToTop();
	// lastly, we need to draw lines between elements and their parent.
	drawLines(data);
}

function forceScrollToTop() {
	$(this).scrollTop(0);
}

function groupCiteData(data) {
	var citeData = data;
	var groupedData = [];
	var citeCount;
	var parentIDs = [];
	var childIDs = [];
	// if item does not have a parentCiteID, it is the parent node.
	groupedData.push(citeData.filter(function (citeItem) {
		return !citeItem.parentCiteID;
	}));
	// remove parent from the array
	citeData = citeData.filter(function (citeItem) {
		return !!citeItem.parentCiteID;
	});
	// citeCount functions as a 'while' loop validator
	citeCount = citeData.length;
	// our goal is to always put child cites on the row below their parent.
	// this 'while' loop will iterate until all citeData is empty, or until it doesn't find any child cites
	while (!!citeData.length) {
		parentIDs = [];
		childIDs = [];
		// get the citeID of all bottom row cites.  
		// on first iteration, this just the original claim citeID as an array of one item.
		groupedData[groupedData.length - 1].forEach(function (lastGroupedItems) {
			parentIDs.push(lastGroupedItems.citeID);
		});
		// find every cite that has a parent in parentIDs
		citeData.forEach(function (citeItem) {
			if (parentIDs.indexOf(citeItem.parentCiteID) > -1) {
				childIDs.push(citeItem.citeID);
			}
		});
		// push the array to grouped data
		groupedData.push(citeData.filter(function (citeItem) {
			return childIDs.indexOf(citeItem.citeID) > -1;
		}));
		// remove used cites from citeData
		citeData = citeData.filter(function (citeItem) {
			return childIDs.indexOf(citeItem.citeID) === -1;
		});
		// check for errors
		if (citeCount === citeData.length) {
			// nothing happened this iteration, so the data is bad
			console.log("data is malformed - orphaned cite exists");
			break;
		}
	}
	return groupedData;
}

function sortCiteData(data) {
	var sortedData = [], subset, unsortedSubset, sortedSubset, previousSortedRowIDs;
	data.forEach(function (rowSubset) {
		// each rowSubset is a row of cites
		subset = [];
		if (rowSubset.length > 1) {
			// if there's multiple cites on this row, we need to sort by parentCiteID to keep lines from crossing
			// problem is, the above row may not be citeID ascending, so we can't order by sort(a - b)
			previousSortedRowIDs = [];
			// grab the parent row's citeIDs.  it's sorted correctly at this point.
			// we can safely assume there will be an array of at least one item here.
			sortedData[sortedData.length - 1].forEach(function (cite) {
				previousSortedRowIDs.push(cite.citeID);
			});
			// for each previousSortedRowID (parentCiteIDs of the current rowSubset), let's populate subset in order
			previousSortedRowIDs.forEach(function (parentCiteID) {
				// find the cites that share a parentCiteID
				unsortedSubset = rowSubset.filter(function (cite) {
					return cite.parentCiteID === parentCiteID;
				});
				// order these cites by score, highest to lowest going from left to right
				sortedSubset = unsortedSubset.sort(function (a, b) {
					return b.score - a.score;
				});
				// add this cite list to the subset (the current row)
				subset.push(...sortedSubset);
			})

		}
		else {
			// this is the original claim
			subset = rowSubset;
		}
		sortedData.push(subset);
	});
	return sortedData;
}

function populateDataIntoCiteBox(citeBox, data) {
	var sourceNode = citeBox.getElementsByClassName("section-content source")[0];
	var linkNode = citeBox.getElementsByClassName("section-content link")[0];
	var scoreNode = citeBox.getElementsByClassName("section-content score")[0];

	citeBox.style = null;
	citeBox.id = data.citeID;

	sourceNode.innerText = `"` + data.source + `"`;
	linkNode.innerText = data.link;
	linkNode.href = data.link;
	// score node changes color depending on the score
	scoreNode.innerText = Math.floor(data.score * 100);
	scoreNode.style.backgroundColor = getBackgroundColorByScore(Math.floor(data.score * 100), 1);
	scoreNode.style.color = getTextColorByScore(Math.floor(data.score * 100));
	scoreNode.style.borderColor = getBackgroundColorByScore(Math.floor(data.score * 100), /* multiplier */ 0.7);

	return citeBox;
}

function getBackgroundColorByScore(score, multiplier) {
	// score of 0 is red background, socre of 100 is green background
	var redVal = 240, greenVal = 240, blueVal = 0;
	var rgbString = "rgb(";

	if (score < 50) {
		greenVal = greenVal - ((50 - score) * 5);
	}
	else {
		redVal = redVal - ((score - 50) * 5);
	}

	// if multiplier has a value, apply it to the colors
	if (!!multiplier) {
		greenVal = greenVal * multiplier;
		redVal = redVal * multiplier;
		blueVal = blueVal * multiplier;
	}

	return rgbString + redVal + "," + greenVal + "," + blueVal + ")";
}

function getTextColorByScore(score) {
	// text color is white < 30, and black >= 30
	var value = 0;
	if (score < 30) {
		value = 255;
	}
	return "rgb(" + value + "," + value + "," + value + ")";
}

function drawLines(citeData) {
	// changing screen resolution will misplace lines.
	var currentCiteBox, parentCiteBox, currentCite, parentCite, currentx, currenty, parentx, parenty, canvasContext;
	// set canvasElement bounds to scrollable screen size.
	deepCite.canvasElement.width = $(document).width();
	deepCite.canvasElement.height = $(document).height();
	canvasContext = deepCite.canvasElement.getContext("2d");
	canvasContext.lineWidth = 2;
	canvasContext.strokeStyle = '#7b7b7b';

	citeData.forEach(function (citeItem) {
		if (!citeItem.parentCiteID) {
			return;
		}
		// currentCiteBox and parentCiteBox are the wrapper elements of the actual cites
		currentCiteBox = document.getElementById(citeItem.citeID);
		parentCiteBox = document.getElementById(citeItem.parentCiteID);
		if (!currentCiteBox || !parentCiteBox) {
			return;
		}
		// currentCite and parentCite are what we want for reference to draw lines
		currentCite = currentCiteBox.children[0];
		parentCite = parentCiteBox.children[0];
		if (!currentCite || !parentCite) {
			return;
		}
		// we want to draw a line from the bottom of the parent cite to the top of the child cite (using three lines and right angles)
		currentx = currentCite.getBoundingClientRect().x + (currentCite.offsetWidth / 2);
		currenty = currentCite.getBoundingClientRect().y;
		parentx = parentCite.getBoundingClientRect().x + (parentCite.offsetWidth / 2);
		parenty = parentCite.getBoundingClientRect().y + parentCite.offsetHeight;
		// draw line from child up
		canvasContext.beginPath();
		canvasContext.moveTo(currentx, currenty);
		canvasContext.lineTo(currentx, currenty - 40);
		canvasContext.stroke();
		// draw line from parent down
		canvasContext.beginPath();
		canvasContext.moveTo(parentx, parenty);
		canvasContext.lineTo(parentx, currenty - 80);
		canvasContext.stroke();
		// draw line to connect the first two lines
		canvasContext.beginPath();
		canvasContext.moveTo(currentx, currenty - 40);
		canvasContext.lineTo(parentx, currenty - 80);
		canvasContext.stroke();
	});
}
// initialize functions on load
init();
