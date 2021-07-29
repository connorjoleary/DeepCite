
function getRandomToken() {
    // E.g. 8 * 32 = 256 bits token
    var randomPool = new Uint8Array(32);
    crypto.getRandomValues(randomPool);
    var hex = '';
    for (var i = 0; i < randomPool.length; ++i) {
        hex += randomPool[i].toString(16);
    }
    // E.g. db18458e2782b2b77e36769c569e263a53885a9944dd0a861e5064eac16f1a
    return hex;
}

// example use: Häagen-Dazs
const normalizeString = (str) => {
	return (str || '')
		.normalize('NFKD')
		.replace(/\s+/g, ' ')
		.replace(/[\u0300-\u036f]/g, '')
		.toLowerCase();
  };

function useTextFragment(url, text) {
	return url.split('#')[0]+'#:~:text='+encodeURIComponent(normalizeString(text).trim())
}

