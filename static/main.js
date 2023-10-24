document.addEventListener('DOMContentLoaded', () => {
	/* Connect the client to the server with web sockets. */
	socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

	/* When the socket is connected, display it on the browser console. */
	socket.on('connect', () => {
		console.log('Client connected to the server through web sockets');
	});
});