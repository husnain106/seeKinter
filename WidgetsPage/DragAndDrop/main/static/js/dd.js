//Note for any R11 readers: drag_start, drag_over and drop are the key functions of this document. Most of the rest is styling to make it look nicer.
function drag_start(event) {
	var style = window.getComputedStyle(event.target, null);
	var str = (parseInt(style.getPropertyValue("left")) - event.clientX) + ',' + (parseInt(style.getPropertyValue("top")) - event.clientY) + ',' + event.target.id;
	event.dataTransfer.setData("Text", str);
}

function drag_over(event) {
	event.preventDefault();
	return false;
}

function drop(event, divId) {
	var offset = event.dataTransfer.getData("Text").split(',');

	var newBlock = document.createElement('aside');
	newBlock.innerHTML = "This is a <i>created</i> box!";
	newBlock.style.background = document.getElementById(offset[2]).style.backgroundColor;
	newBlock.style.left = (event.clientX + parseInt(offset[0], 10)) + 'px';
	newBlock.style.top = (event.clientY + parseInt(offset[1], 10)) + 'px';

	document.getElementById(divId).appendChild(newBlock);

	event.preventDefault();
	return false;
}