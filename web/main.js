function nextButtonClick() { //executed when user clicks "Next"-Button
	eel.nextButtonClick(document.getElementById("exampleInputUrl1").value, //sends form data to python backend
						[document.getElementById("inlineCheckbox1").checked,
						 document.getElementById("inlineCheckbox2").checked,
						 document.getElementById("inlineCheckbox3").checked,
						 document.getElementById("inlineCheckbox4").checked,
						 document.getElementById("inlineCheckbox5").checked,
						 document.getElementById("inlineCheckbox6").checked],
						{"download_dir": false, 
						 "headless": !document.getElementById("inlineCheckbox7").checked, 
						 "screenshot": document.getElementById("inlineCheckbox8").checked});

	//hides current page and shows next
	document.getElementById("optionspage").style.display = "none"; 
	document.getElementById("loginpage").style.display = "block";
}

function startButtonClick() { //executed when user clicks "Start Download"-Button
	eel.startButtonClick(document.getElementById("exampleInputUsername1").value, //sends form data to python backend
						 document.getElementById("exampleInputPassword1").value);

	//hides current page and shows next
	document.getElementById("loginpage").style.display = "none"; 
	document.getElementById("loadingpage").style.display = "block";
}

function quitButtonClick() { //executed when user clicks "Quit"-Button
	window.close()
}

function backButtonClick() { //executed when user clicks "Back"-Button

	//hides all possible current pages and shows startpage
	document.getElementById("successpage").style.display = "none";
	document.getElementById("errorpage").style.display = "none";
	document.getElementById("optionspage").style.display = "block";
}

eel.expose(wrongLogin);
function wrongLogin() {
	window.alert("wrong login") //make better later

	//reshows login page
	document.getElementById("loginpage").style.display = "block"; 
	document.getElementById("loadingpage").style.display = "none";
}

eel.expose(updateProgressbar); 
function updateProgressbar(len, text) { //updates progressbar, called from python backend
	$(".progress-bar").css("width", len + "%") //changes progressbar width
	document.getElementById("progresstext").innerHTML = text //changes text below progressbar to currnet file being downloaded
}

eel.expose(showEndScreen);
function showEndScreen(n, filepath) { //shows EndScreen, called from python backend
	document.getElementById("num_files").innerHTML = n; //adds number of downloaded files -label
	document.getElementById("filepath").innerHTML = filepath; //adds file destination -label

	//hides current page and shows endscreen
	document.getElementById("loadingpage").style.display = "none";
	document.getElementById("successpage").style.display = "block"
}

eel.expose(showErrorScreen);
function showErrorScreen(text) { //shows ErrorScreen, called from python backend
	document.getElementById("errorDescription").innerHTML = text; //adds error description

	//hides all possible current pages and shows error-page
	document.getElementById("loginpage").style.display = "none";
	document.getElementById("loadingpage").style.display = "none";
	document.getElementById("successpage").style.display = "none";
	document.getElementById("errorpage").style.display = "block"
}