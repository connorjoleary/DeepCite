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
    chrome.storage.local.set({ 'state': 0},  function(){
        console.log('Initialized extention state');
    });
    chrome.storage.local.set({'lastData': "0"}, ()=>{
        console.log('Initialized previous data variable');
    });
});

function populateClaim() {
    //add in iteration 2
}