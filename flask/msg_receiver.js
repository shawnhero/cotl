var eventOutputContainer = document.getElementById("event");
var evtSrc = new EventSource("/subscribe");
evtSrc.onmessage = function(e) {
	console.log(e.data);
	eventOutputContainer.innerHTML = e.data;
};
