async function grab_ip() {
	const response = await fetch('http://api.ipify.org/?format=json');
	const data = await response.json();
	return data.ip;
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

