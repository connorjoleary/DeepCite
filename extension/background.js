chrome.runtime.onInstalled.addListener(function () {
    chrome.contextMenus.create({
        title: 'DeepCite for "%s"',
        contexts: ['selection'],
        onclick: populateClaim
    });
});

function populateClaim() {

}