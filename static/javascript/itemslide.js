var slideIndex = 1;
showSlides(slideIndex);
var pages = document.getElementsByClassName("card-holder")

function prevSlide() {
  for (i = 0; i < pages.length; i++) {
    document.getElementById(pages[i].id).className = "card-holder animation-left";
  }
}

function nextSlide() {
  for (i = 0; i < pages.length; i++) {
    document.getElementById(pages[i].id).className = "card-holder animation-right";
  }
}

function plusSlides(n) {
  showSlides(slideIndex += n);
}

function toPage(elem) {
  var tempString = elem.id;
  var extractedNumber = tempString.match(/(\d+)/);
	var convertedInt = parseInt(extractedNumber[0]);

  if (convertedInt > slideIndex) {
    nextSlide();
  } else if (convertedInt < slideIndex) {
    prevSlide();
  }

  showSlides(slideIndex = convertedInt);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("card-holder");

  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }

  slides[slideIndex-1].style.display = "grid";
  setActivePage(slideIndex);
}

function setActivePage(activeSlide) {
  var pageButtons = document.getElementsByClassName("catalog-pages");
  for (i = 0; i < pageButtons.length; i++) {
    if ((i+1) == activeSlide) {
      pageButtons[i].className = "catalog-pages catalog-pages-active";
    } else {
      pageButtons[i].className = "catalog-pages";
    }
  }
}
