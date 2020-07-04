/*
 *	DeepSite Source Tree page 
*/

if (!deepCite) {
	var deepCite = {};
}
// DOM elements
deepCite.citeComponent = document.getElementsByClassName("generated-cite-box")[0];
deepCite.claimComponent = document.getElementsByClassName("generated-claim-box")[0];
deepCite.treeContainer = document.getElementById("tree-container");
deepCite.canvasElement = document.getElementById("canvas-element");

// initialization function
function init() {
	// this function will be replaced by getData, an ajax call that will gather data from the server.
	var testData = generateTestData();
	populateDataIntoTree(testData);
}

function generateTestData() {
	var record, parentRecordID, randomTextCount;
	var text = "";
	var runningRecordID = 1;
	var randomText = "lorem ipsum dolor ";
	var testData = [];
	// random number 3-20
	var randomCount = (Math.floor(Math.random() * 18) + 3);

	while (randomCount > 0) {
		// a random cite with a lower id.  if citeID = 1, parentCiteID = 0
		parentRecordID = runningRecordID !== 1 ? Math.floor(Math.random() * (runningRecordID - 1) + 1) : 0;
		text = "";
		// get a random amount of text
		randomTextCount = (Math.floor(Math.random() * 20) + 1);
		while (randomTextCount > 0) {
			text = text + "" + randomText;
			randomTextCount--;
		}
		record = {
			citeID: runningRecordID,
			parentCiteID: parentRecordID,
			link: "https://www.testData.com",
			score: Math.floor(Math.random() * 100),
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
}

function upvoteButtonClicked(element) {
	var citeID = findClosestCiteID(element);
	console.log("upvote clicked on citeID " + citeID);
}

function downvoteButtonClicked(element) {
	var citeID = findClosestCiteID(element);
	console.log("downvote clicked on citeID " + citeID);
}

function findClosestCiteID(element) {
	var citeBox = element.closest(".generated-cite-box");
	if (!!citeBox) {
		return parseInt(citeBox.id);
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
			}
			else {
				clonedCiteBox = deepCite.citeComponent.cloneNode(true);
				populatedCiteBox = populateDataIntoCiteBox(clonedCiteBox, item);
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
	var sortedData = [], subset, previousSortedRowIDs;
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
				subset.push(...rowSubset.filter(function (cite) {
					return cite.parentCiteID === parentCiteID;
				}));
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
	scoreNode.innerText = "Score: " + data.score + "%";
	return citeBox;
}

function drawLines(citeData) {
	// changing screen resolution will misplace lines.
	var currentCiteBox, parentCiteBox, currentCite, parentCite, currentx, currenty, parentx, parenty, canvasContext;
	// set canvasElement bounds to scrollable screen size.
	deepCite.canvasElement.width = $(document).width();
	deepCite.canvasElement.height = $(document).height();
	canvasContext = deepCite.canvasElement.getContext("2d");
	canvasContext.lineWidth = 2;

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
		// we want to draw a line from the bottom of the parent cite to the top of the child cite
		currentx = currentCite.getBoundingClientRect().x + (currentCite.offsetWidth / 2);
		currenty = currentCite.getBoundingClientRect().y;
		parentx = parentCite.getBoundingClientRect().x + (parentCite.offsetWidth / 2);
		parenty = parentCite.getBoundingClientRect().y + parentCite.offsetHeight;
		// draw the line
		canvasContext.beginPath();
		canvasContext.moveTo(currentx, currenty);
		canvasContext.lineTo(parentx, parenty);
		canvasContext.stroke();
	});
}
// initialize functions on load
init();
