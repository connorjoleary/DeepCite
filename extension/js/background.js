// adds DeepCite to right click context menu
chrome.runtime.onInstalled.addListener(function () {

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

    // chrome.contextMenus.create({
    //     title: `Populate claim: "%s"`, 
    //     contexts:["selection"], 
    //     onclick: function(info, tab) {
    //         chrome.storage.local.set({ 'state': 0},  function(){
    //             console.log('Reset extention state');
    //         }); 
    //         chrome.storage.local.set({ 'claimField': info.selectionText }, function () {
    //             console.log('Populated claimField');
    //         });
    //     }
    // });
    // chrome.contextMenus.create({
    //     title: `Populate link`, 
    //     contexts:["link"], 
    //     onclick: function(info, tab) {
    //         chrome.storage.local.set({ 'state': 0},  function(){
    //             console.log('Reset extention state');
    //         }); 
    //         chrome.storage.local.set({ 'linkField': info.linkUrl }, function () {
    //             console.log('Populated claimField');
    //         });
    //     }
    // });
});

function populateClaim() {
    //add in iteration 2
}