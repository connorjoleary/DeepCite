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

var testData = [{
	citeID: 1,
	parentCiteID: 0,
	link: "https://en.wikipedia.org/wiki/Video_game",
	score: 0,
	source: "Video games are fun."
}, {
	citeID: 2,
	parentCiteID: 1,
	link: "https://google.com",
	score: 70,
	source: "Video games are enjoyed by many people."
}, {
	citeID: 3,
	parentCiteID: 1,
	link: "https://angrygamer.com",
	score: 20,
	source: "Video games are NOT fun."
}, {
	citeID: 4,
	parentCiteID: 1,
	link: "https://philosophyofvideogames.com",
	score: 10,
	source: "It is unknown whether or not video games are fun."
}, {
	citeID: 5,
	parentCiteID: 2,
	link: "https://reddit.com",
	score: 100,
	source: "I have played video games, and I enjoy them."
}, {
	citeID: 6,
	parentCiteID: 3,
	link: "https://angrygamer.com",
	score: 10,
	source: "I personally hate video games."
}, {
	citeID: 7,
	parentCiteID: 6,
	link: "https://angryoldman.com",
	score: 10,
	source: "I personally hate everything."
}, {
	citeID: 8,
	parentCiteID: 3,
	link: "https://gamerlore.com",
	score: 100,
	source: "Gamers like games more than non-gamers."
}];

// initialization function
function init() {
	populateDataIntoTree(testData);
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
	var clonedCiteBox, populatedCiteBox, groupedData;
	var rowCiteCount = 1;
	// first, we need to group our citations by parentCiteID
	groupedData = groupCiteData(data);
	// next, we need to create cite/claim boxes for each item and put them in the correct row
	groupedData.forEach(function (dataGroup) {
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
	// lastly, we need to draw lines between elements and their parent.
	drawLines(data);
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
	// this function currently only draws lines on the observable page.
	// changing screen resolution will misplace lines, and scrolling down will reveal an absence of lines.
	// this should be modified to fix these two issues.
	var currentCiteBox, parentCiteBox, currentCite, parentCite, currentx, currenty, parentx, parenty, canvasContext;
	// set canvasElement bounds to observable window
	deepCite.canvasElement.width = window.innerWidth;
	deepCite.canvasElement.height = window.innerHeight;
	canvasContext = deepCite.canvasElement.getContext("2d");

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
