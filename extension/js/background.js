// adds DeepCite to right click context menu
chrome.runtime.onInstalled.addListener(function () {
    chrome.contextMenus.create({
        title: 'DeepCite for "%s"',
        contexts: ['selection'],
        onclick: populateClaim
    });


    chrome.storage.local.set({ 'claimField': "" }, function () {
        console.log('Initialized claimField');
    });
    chrome.storage.local.set({ 'linkField': "" }, function () {
        console.log('Initialized linkField');
    });
});

function populateClaim() {
    //add in iteration 2
}