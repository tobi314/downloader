function submitButton() {
	eel.submitButton_click(document.getElementById("exampleInputUsername1").value, 
						   document.getElementById("exampleInputPassword1").value,
						   document.getElementById("exampleInputUrl1").value);
	document.getElementById("startpage").style.display = "none";
	document.getElementById("loadingpage").style.display = "block";
}

function quitButton() {
	eel.quitButton_click();
	window.close()
}

function backButton() {
	eel.backButton_click();
	document.getElementById("successpage").style.display = "none";
	document.getElementById("errorpage").style.display = "none";
	document.getElementById("startpage").style.display = "block"
}

eel.expose(updateProgressbar);
function updateProgressbar(len, text) {
	var i = document.getElementById("progressbar1").style.width = len
	document.getElementById("progresstext").innerHTML = text
}

eel.expose(showEndScreen);
function showEndScreen(n, filepath) {
	document.getElementById("num_files").innerHTML = n;
	document.getElementById("filepath").innerHTML = filepath;
	document.getElementById("loadingpage").style.display = "none";
	document.getElementById("successpage").style.display = "block"
}

eel.expose(showErrorScreen);
function showErrorScreen(text) {
	document.getElementById("errorDescription").innerHTML = text;
	document.getElementById("startpage").style.display = "none";
	document.getElementById("loadingpage").style.display = "none";
	document.getElementById("successpage").style.display = "none";
	document.getElementById("errorpage").style.display = "block"
}