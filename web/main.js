async function submitButton() {
	eel.submitButton_click(document.getElementById("exampleInputUsername1").value, 
						   document.getElementById("exampleInputPassword1").value,
						   document.getElementById("exampleInputUrl1").value);
	document.getElementById("startpage").style.display = "none";
	document.getElementById("loadingpage").style.display = "block";
	await new Promise(r => setTimeout(r, 2000));
	document.getElementById("loadingpage").style.display = "none";
	document.getElementById("successpage").style.display = "block"
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
