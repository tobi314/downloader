async function submitButton() {
	eel.submitButton_click(document.getElementById("exampleInputUsername1").value, 
						   document.getElementById("exampleInputPassword1").value,
						   document.getElementById("exampleInputUrl1").value);
	document.getElementById("startpage").style.display = "none";
	document.getElementById("loadingpage").style.display = "block";
	await new Promise(r => setTimeout(r, 2000));
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
function updateProgressbar(i) {
	document.getElementById("progressbar1").setAttribute("aria-valuenow", i)
}

eel.expose(setupProgressbar);
function setupProgressbar(min, max) {
	document.getElementById("progressbar1").setAttribute("aria-valuemin", min);
	document.getElementById("progressbar1").setAttribute("aria-valuemax", max)
}

eel.expose(showEndScreen);
function showEndScreen(n, filepath) {
	document.getElementById("num_files").innerHTML = n;
	document.getElementById("filepath").innerHTML = filepath;
	document.getElementById("loadingpage").style.display = "none";
	document.getElementById("successpage").style.display = "block"
}