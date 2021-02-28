async function submitButton() {
	eel.submitButton_click();
	document.getElementById("startpage").style.display = "none";
	document.getElementById("loadingpage").style.display = "block";
	await new Promise(r => setTimeout(r, 2000));
	document.getElementById("loadingpage").style.display = "none";
	document.getElementById("errorpage").style.display = "block"
}

function quitButton(){
	eel.quitButton_click();
	window.close()
}

function backButton(){
	eel.backButton_click();
	document.getElementById("successpage").style.display = "none";
	document.getElementById("errorpage").style.display = "none";
	document.getElementById("startpage").style.display = "block"
}