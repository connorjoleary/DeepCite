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

    chrome.contextMenus.create({
        title: "Cite this text",
        contexts:["selection"],  // ContextType
        onclick: newCitationFromSelection // A callback function
       });
});

function newCitationFromSelection(info) {
    claim = info.selectionText;
    link = info.pageUrl;

    chrome.storage.local.set({ 'claimField': claim }, function () {
        console.log('Rightclick claim set to:', claim);
    });
    chrome.storage.local.set({ 'linkField': link }, function () {
        console.log('Rightclick link set to:', link);
    });
    chrome.storage.local.set({ 'state': 0 }, function () {
        console.log('Initialized extention state');
    });
    
    // submitClaim(claim, link)
}
