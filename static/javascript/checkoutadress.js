var speedy = document.getElementById("shippingmethod-0");
var econt = document.getElementById("shippingmethod-1");
var home = document.getElementById("shippingmethod-2");
var adresslabel = document.getElementById("forjs")

speedy.addEventListener('change', function(event) {
	if (speedy.checked == true) {
		adresslabel.innerHTML = "Адрес на офис*";
	}
});

econt.addEventListener('change', function(event) {
	if (econt.checked == true) {
		adresslabel.innerHTML = "Адрес на офис*";
	}
});

home.addEventListener('change', function(event) {
	if (home.checked == true) {
		adresslabel.innerHTML = "Адрес*";
	}
});
