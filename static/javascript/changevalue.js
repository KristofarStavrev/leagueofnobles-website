var product = document.getElementsByClassName('qnumber');
var decbtn = document.getElementsByClassName('decrease');
var incbtn = document.getElementsByClassName('increase');

function increaseValue(passedval) {
  	var value = parseInt(product[passedval].value, 10);
  	value = isNaN(value) ? 0 : value;
  	value++;
	product[passedval].value = value;
}

function decreaseValue(passedval) {
  	var value = parseInt(product[passedval].value, 10);
  	value = isNaN(value) ? 1 : value;
	if (value > 1) {
  		value--;
	}
	product[passedval].value = value;
}

for (var i = 0; i < product.length; i++) {
	decbtn[i].addEventListener('click', decreaseValue.bind(this, i));
	incbtn[i].addEventListener('click', increaseValue.bind(this, i));
}
