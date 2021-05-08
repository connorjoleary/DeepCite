async function grab_ip() {
	const response = await fetch('http://api.ipify.org/?format=json');
	const data = await response.json();
	return data.ip;
}

function useTextFragment(url, text) {
	return url.split('#')[0]+'#:~:text='+escape(text.toLowerCase().trim())
}

