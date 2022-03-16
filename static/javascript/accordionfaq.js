var acc = document.getElementsByClassName("accordion");
var i;
var y;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var panel = this.nextElementSibling;
    if (panel.style.maxHeight) {
      this.children[1].children[0].className = 'fas fa-chevron-down';
      panel.style.maxHeight = null;
    } else {
      this.children[1].children[0].className = 'fas fa-chevron-up';
      panel.style.maxHeight = panel.scrollHeight + "px";
      panel.style.marginBottom = "10px";
    }
  });
}

window.addEventListener("resize", deviceResize);

function deviceResize() {
  for (y = 0; y < acc.length; y++) {
    var panelresize = acc[y].nextElementSibling;
    if (panelresize.style.maxHeight) {
      panelresize.style.maxHeight = panelresize.scrollHeight + "px";
    }
  }
}
