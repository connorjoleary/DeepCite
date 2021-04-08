async function grab_ip() {
	const response = await fetch('http://api.ipify.org/?format=json');
	const data = await response.json();
	return data.ip;
}

