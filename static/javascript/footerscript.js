var myfooter = document.getElementsByClassName("my-footer")[0];
var mainheader = document.getElementById("main-header");


myfooter.style.height = "312px";
myfooter.style.marginTop = "-312px";
mainheader.style.paddingBottom = "352px";

window.addEventListener("resize", myResize);

window.addEventListener("load", myResize);

function myResize() {
	myfooter.style.height = "312px";
	myfooter.style.marginTop = "-312px";
	mainheader.style.paddingBottom = "352px";

	var correctpadding = myfooter.scrollHeight + 40;
	myfooter.style.height = myfooter.scrollHeight + "px";
	myfooter.style.marginTop = "-" + myfooter.scrollHeight + "px";
	mainheader.style.paddingBottom = correctpadding + "px";
}