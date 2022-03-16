from flask import Flask, render_template, url_for, flash, redirect, request, make_response
from forms import ContactForm, CheckoutForm
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from collections import OrderedDict
import datetime
import time
from jinja2 import Environment
import json

with open('config.json') as config_file:
	config = json.load(config_file)

jinja_env = Environment(extensions=['jinja2.ext.loopcontrols'])

app = Flask(__name__)

app.config['SECRET_KEY'] = config.get('SECRET_KEY')
app.config['RECAPTCHA_PUBLIC_KEY'] = config.get('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = config.get('RECAPTCHA_PRIVATE_KEY')
app.config['TESTING'] = False
app.config['DEBUG'] = False
app.config['ENV'] = 'production'
app.config['MAIL_SERVER'] = config.get('MAIL_SERVER')
app.config['MAIL_PORT'] = config.get('MAIL_PORT')
app.config['MAIL_USE_SSL'] = config.get('MAIL_USE_SSL')
app.config['MAIL_USE_TLS'] = config.get('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = config.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = config.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = config.get('MAIL_DEFAULT_SENDER')
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

mail = Mail(app)
db = SQLAlchemy(app)

class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	product_name = db.Column(db.String(20), unique=True, nullable=False)
	product_price = db.Column(db.Float, nullable=False)
	product_quantity = db.Column(db.Integer, nullable=False)
	product_image = db.Column(db.String(20), nullable=False, default='default.png')

	def __repr__ (self):
		return f"Product('{self.product_name}, {self.product_price}, {self.product_quantity}, {self.product_image}')"

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
	current_date = datetime.datetime.now()
	expire_date_accept_cookies = current_date + datetime.timedelta(days=365)
	expire_date_cookies = current_date + datetime.timedelta(days=14)
	products = Product.query.all()
	cart_counter = 0
	products_names = []
	accepted_cookies = False
	no_quantity = False

	if 'accept_cookies' in request.cookies:
		accepted_cookies = True

	if request.cookies:
		for product in products:
			products_names.append(product.product_name)

	error_resp = make_response(redirect(url_for('home', _anchor='sideline')))
	if request.cookies:
		for item in request.cookies:
			if item in products_names:
				validate_quantity = int(request.cookies.get(item))
				db_item_quantity = Product.query.filter_by(product_name=item).first().product_quantity

				if db_item_quantity < validate_quantity:
					no_quantity = True

					if db_item_quantity == 0:
						error_resp.delete_cookie(str(item))
					else:
						error_resp.set_cookie(str(item), str(db_item_quantity), expires=expire_date_cookies)

	if no_quantity:
		return error_resp

	# User agrees to cookies
	if request.method == 'POST' and 'accept_cookies' in request.form:
		resp = make_response(redirect(url_for('home')))
		resp.set_cookie('accept_cookies', str(True), expires=expire_date_accept_cookies)
		return resp

	if request.method == 'POST':
		if 'newsletteremail' in request.form:

			msg = Message('Newsletter', recipients=['leagueofnobles.store@gmail.com'])
			msg.body = 'Email: {0}'.format(request.form['newsletteremail'])
			mail.send(msg)

			usrmsg = Message('Записване за бюлетин', recipients=[request.form['newsletteremail']])
			usrmsg.html = 'Здравейте, <br><br>Благодарим Ви, че се записахте за нашия информационен бюлетин. Чрез него ще получавате новини и промени относно League of Nobles, лимитирани оферти и кодове за отстъпки.<br><br>Поздрави,<br>Екипът на League of Nobles<br><br><br>'
			usrmsg.html = usrmsg.html + render_template('email_signature.html')
			mail.send(usrmsg)

		elif 'product_name' in request.form:
			product_name = request.form.get('product_name')
			resp = make_response(redirect(url_for('home', _anchor='sideline')))

			if request.cookies:
				if product_name in request.cookies:
					quantity = int(request.cookies.get(product_name))
					current_item_quantity = Product.query.filter_by(product_name=product_name).first()

					if (quantity + 1) > current_item_quantity.product_quantity:
						flash('Желаното количество от ключодържателя \"{0}\" ({1} бр.) не е налично в момента.'.format(product_name, (quantity + 1)), 'home_error')
					else:
						quantity = quantity + 1

					resp.set_cookie(str(product_name), str(quantity), expires=expire_date_cookies)
				else:
					current_item_quantity = Product.query.filter_by(product_name=product_name).first().product_quantity
					if current_item_quantity > 0:
						resp.set_cookie(str(product_name), str(1), expires=expire_date_cookies)
			else:
				current_item_quantity = Product.query.filter_by(product_name=product_name).first().product_quantity
				if current_item_quantity > 0:
					resp.set_cookie(str(product_name), str(1), expires=expire_date_cookies)

			return resp

	if request.cookies:
		for item in request.cookies:
			if item in products_names:
				cart_counter = cart_counter + int(request.cookies.get(item))

	return render_template('index.html', cart_counter=cart_counter, products = products, accepted_cookies=accepted_cookies)

@app.route('/faq', methods=['GET', 'POST'])
def faq():
	accepted_cookies = False
	current_date = datetime.datetime.now()
	expire_date_accept_cookies = current_date + datetime.timedelta(days=365)
	expire_date_cookies = current_date + datetime.timedelta(days=14)
	cart_counter = 0
	products_names = []
	products = Product.query.all()
	no_quantity = False

	if 'accept_cookies' in request.cookies:
		accepted_cookies = True

	if request.cookies:
		for product in products:
			products_names.append(product.product_name)

	error_resp = make_response(redirect(url_for('faq')))
	if request.cookies:
		for item in request.cookies:
			if item in products_names:
				validate_quantity = int(request.cookies.get(item))
				db_item_quantity = Product.query.filter_by(product_name=item).first().product_quantity

				if db_item_quantity < validate_quantity:
					no_quantity = True

					if db_item_quantity == 0:
						error_resp.delete_cookie(str(item))
					else:
						error_resp.set_cookie(str(item), str(db_item_quantity), expires=expire_date_cookies)

	if no_quantity:
		return error_resp

	if request.method == 'POST' and 'newsletteremail' in request.form:

		msg = Message('Newsletter', recipients=['leagueofnobles.store@gmail.com'])
		msg.body = 'Email: {0}'.format(request.form['newsletteremail'])
		mail.send(msg)

		usrmsg = Message('Записване за бюлетин', recipients=[request.form['newsletteremail']])
		usrmsg.html = 'Здравейте, <br><br>Благодарим Ви, че се записахте за нашия информационен бюлетин. Чрез него ще получавате новини и промени относно League of Nobles, лимитирани оферти и кодове за отстъпки.<br><br>Поздрави,<br>Екипът на League of Nobles<br><br><br>'
		usrmsg.html = usrmsg.html + render_template('email_signature.html')
		mail.send(usrmsg)

	# User agrees to cookies
	if request.method == 'POST' and 'accept_cookies' in request.form:
		resp = make_response(redirect(url_for('faq')))
		resp.set_cookie('accept_cookies', str(True), expires=expire_date_accept_cookies)
		return resp

	if request.cookies:
		for item in request.cookies:
			if item in products_names:
				cart_counter = cart_counter + int(request.cookies.get(item))

	return render_template('faq.html', cart_counter=cart_counter, accepted_cookies=accepted_cookies)

@app.route('/contact', methods=['GET', 'POST'])
def contactpage():
	form = ContactForm()
	accepted_cookies = False
	current_date = datetime.datetime.now()
	expire_date_accept_cookies = current_date + datetime.timedelta(days=365)
	expire_date_cookies = current_date + datetime.timedelta(days=14)
	cart_counter = 0
	products_names = []
	products = Product.query.all()
	no_quantity = False

	if 'accept_cookies' in request.cookies:
		accepted_cookies = True

	# User agrees to cookies
	if request.method == 'POST' and 'accept_cookies' in request.form:
		resp = make_response(redirect(url_for('contactpage')))
		resp.set_cookie('accept_cookies', str(True), expires=expire_date_accept_cookies)
		return resp

	if request.cookies:
		for product in products:
			products_names.append(product.product_name)

	error_resp = make_response(redirect(url_for('contactpage')))
	if request.cookies:
		for item in request.cookies:
			if item in products_names:
				validate_quantity = int(request.cookies.get(item))
				db_item_quantity = Product.query.filter_by(product_name=item).first().product_quantity

				if db_item_quantity < validate_quantity:
					no_quantity = True

					if db_item_quantity == 0:
						error_resp.delete_cookie(str(item))
					else:
						error_resp.set_cookie(str(item), str(db_item_quantity), expires=expire_date_cookies)

	if no_quantity:
		return error_resp

	if request.method == 'POST':

		if 'newsletteremail' in request.form:

			msg = Message('Newsletter', recipients=['leagueofnobles.store@gmail.com'])
			msg.body = 'Email: {0}'.format(request.form['newsletteremail'])
			mail.send(msg)

			usrmsg = Message('Записване за бюлетин', recipients=[request.form['newsletteremail']])
			usrmsg.html = 'Здравейте, <br><br>Благодарим Ви, че се записахте за нашия информационен бюлетин. Чрез него ще получавате новини и промени относно League of Nobles, лимитирани оферти и кодове за отстъпки.<br><br>Поздрави,<br>Екипът на League of Nobles<br><br><br>'
			usrmsg.html = usrmsg.html + render_template('email_signature.html')
			mail.send(usrmsg)

		else:

			if form.validate_on_submit():

				flash(f'Съобщението е изпратено! Благодарим ви за обратната връзка!', 'successmessage')
				msg = Message('Contact', recipients=['leagueofnobles.store@gmail.com'])
				msg.body = 'Name: {0} \nEmail: {1} \nPhone: {2} \nMessage: {3}'.format(form.name.data, form.email.data, form.phonenumber.data, form.message.data)
				mail.send(msg)

				usrmsg = Message('Обратна връзка', recipients=[form.email.data])
				usrmsg.html = 'Здравейте {0},<br><br>Благодарим Ви за обратната връзка, ще се свържим с Вас възможно най-скоро. Вашето мнение е важно за нас.<br><br><br>'.format(form.name.data)
				usrmsg.html = usrmsg.html + render_template('email_signature.html')
				mail.send(usrmsg)

	if request.cookies:
		for item in request.cookies:
			if item in products_names:
				cart_counter = cart_counter + int(request.cookies.get(item))

	return render_template('contact.html', cart_counter=cart_counter, form=form, accepted_cookies=accepted_cookies)

@app.route('/shoppingcart', methods=['GET', 'POST'])
def shoppingcart():
	checkoutform = CheckoutForm()
	current_date = datetime.datetime.now()
	expire_date_accept_cookies = current_date + datetime.timedelta(days=365)
	expire_date_cookies = current_date + datetime.timedelta(days=14)

	products = Product.query.all()
	product_data = {}
	products_names = []
	accepted_cookies = False
	current_amount = 0
	discount = 0
	final_amount = 0
	cart_counter = 0
	order_date = ''
	no_quantity = False
	sc_no_quantity = False

	if 'accept_cookies' in request.cookies:
		accepted_cookies = True

	# User agrees to cookies

	if request.method == 'POST' and 'accept_cookies' in request.form:
		resp = make_response(redirect(url_for('shoppingcart')))
		resp.set_cookie('accept_cookies', str(True), expires=expire_date_accept_cookies)
		return resp

	if request.method == 'POST' and 'newsletteremail' in request.form:

		msg = Message('Newsletter', recipients=['leagueofnobles.store@gmail.com'])
		msg.body = 'Email: {0}'.format(request.form['newsletteremail'])
		mail.send(msg)

		usrmsg = Message('Записване за бюлетин', recipients=[request.form['newsletteremail']])
		usrmsg.html = 'Здравейте, <br><br>Благодарим Ви, че се записахте за нашия информационен бюлетин. Чрез него ще получавате новини и промени относно League of Nobles, лимитирани оферти и кодове за отстъпки.<br><br>Поздрави,<br>Екипът на League of Nobles<br><br><br>'
		usrmsg.html = usrmsg.html + render_template('email_signature.html')
		mail.send(usrmsg)

	if request.cookies:
		for product in products:
			products_names.append(product.product_name)

		for item in request.cookies:
			if item in products_names:
				product_data[item] = request.cookies.get(item)

	if not bool(product_data):
		return render_template('empty_cart.html', cart_counter=cart_counter, accepted_cookies=accepted_cookies)

	if request.method == 'POST' and 'checkoutemail' in request.form:
		sc_error_resp = make_response(redirect(url_for('error')))
	else:
		sc_error_resp = make_response(redirect(url_for('shoppingcart')))
	if request.cookies:
		for item in request.cookies:
			if item in products_names:
				validate_quantity = int(request.cookies.get(item))
				db_item_quantity = Product.query.filter_by(product_name=item).first().product_quantity

				if db_item_quantity < validate_quantity:
					sc_no_quantity = True

					if db_item_quantity == 0:
						sc_error_resp.delete_cookie(str(item))
					else:
						sc_error_resp.set_cookie(str(item), str(db_item_quantity), expires=expire_date_cookies)

	if sc_no_quantity:
		return sc_error_resp

	if request.method == "POST" and 'delete-item' in request.form:
		product_name = request.form.get('product_name')
		resp = make_response(redirect(url_for('shoppingcart')))

		if request.cookies:
			for item in request.cookies:
				if item == product_name:
					resp.delete_cookie(str(item))
					return resp

	if request.method == "POST" and 'decrease' in request.form:
		product_name = request.form.get('product_name')
		resp = make_response(redirect(url_for('shoppingcart')))

		if request.cookies:
			for item in request.cookies:
				if item == product_name:
					quantity = int(request.cookies.get(item))
					quantity = quantity - 1

					if quantity == 0:
						resp.delete_cookie(str(item))
						return resp
					else:
						resp.set_cookie(str(product_name), str(quantity), expires=expire_date_cookies)
						return resp

	if request.method == "POST" and 'increase' in request.form:
		product_name = request.form.get('product_name')
		resp = make_response(redirect(url_for('shoppingcart')))

		if request.cookies:
			for item in request.cookies:
				if item == product_name:
					quantity = int(request.cookies.get(item))
					current_item_quantity = Product.query.filter_by(product_name=product_name).first()

					if (quantity + 1 ) > current_item_quantity.product_quantity:
						flash('Желаното количество от ключодържателя \"{0}\" ({1} бр.) не е налично в момента.'.format(product_name, (quantity + 1)), 'cart_error')
					else:
						quantity = quantity + 1

					if quantity == 0:
						resp.delete_cookie(str(item))
						return resp
					else:
						resp.set_cookie(str(product_name), str(quantity), expires=expire_date_cookies)
						return resp

	if request.cookies:
		for item in request.cookies:
			if item in products_names:
				cart_counter = cart_counter + int(request.cookies.get(item))

	if request.method == 'POST' and 'current_amount' in request.form and 'discount' in request.form and 'final_amount' in request.form:
		current_amount = request.form.get('current_amount')
		discount = request.form.get('discount')
		final_amount = request.form.get('final_amount')
		return render_template('checkout.html', currentamount=current_amount, discount=discount, finalamount=final_amount, form=checkoutform, cart_counter=cart_counter, accepted_cookies=accepted_cookies)

	if request.method == "POST" and 'fname' in request.form and 'lname' in request.form and 'checkoutemail' in request.form and 'phone' in request.form and bool(product_data):
		if checkoutform.validate_on_submit():
			error_resp = make_response(redirect(url_for('error')))

			if request.cookies:
				for item in request.cookies:
					if item in products_names:
						validate_quantity = int(request.cookies.get(item))
						db_item_quantity = Product.query.filter_by(product_name=item).first().product_quantity

						if db_item_quantity < validate_quantity:
							no_quantity = True

							if db_item_quantity == 0:
								error_resp.delete_cookie(str(item))
							else:
								error_resp.set_cookie(str(item), str(db_item_quantity), expires=expire_date_cookies)

			if no_quantity:
				return error_resp

			if checkoutform.shippingmethod.data == 1:
				shippingmethod = "Спиди"

			elif checkoutform.shippingmethod.data == 2:
				shippingmethod = "Еконт"

			elif checkoutform.shippingmethod.data == 3:
				shippingmethod = "До адрес"

			temporderid = str(int(time.time()))
			orderid = ''
			for x in range(len(temporderid) - 1, 1, -1):
				orderid = temporderid[x] + orderid

			current_amount = 0
			discount = 0
			final_amount = 0
			product_count = 0

			for orderproduct in product_data:
				current_amount = current_amount + (int(product_data[orderproduct]) * Product.query.filter_by(product_name=orderproduct).first().product_price)
				product_count = product_count + int(product_data[orderproduct])

			if product_count == 2:
				discount = current_amount * 0.1
			elif product_count >= 3:
				discount = current_amount * 0.15
			else:
				discount = 0

			final_amount = current_amount - discount
			current_amount = "%.2f" % current_amount
			discount = "%.2f" % discount
			final_amount = "%.2f" % final_amount

			msg = Message('Order #{0}'.format(orderid), recipients=['leagueofnobles.store@gmail.com'])
			usrmsg = Message('League of Nobles Поръчка №{0}'.format(orderid), recipients=[checkoutform.checkoutemail.data])
			msg.body = 'Order id: {13} \nFirst name: {0} \nLast name: {1} \nEmail: {2} \nPhone: {3} \nShipping method: {4} \nProvince: {5} \nCity: {6} \nAddress: {7} \nOrder date: {12} \nAdditional info: {8} \n\nCurrent amount: {9} \nDiscount: {10} \nFinal amount: {11} \n\nProducts: \n'.format(checkoutform.fname.data, checkoutform.lname.data, checkoutform.checkoutemail.data, checkoutform.phone.data, shippingmethod, checkoutform.province.data, checkoutform.city.data, checkoutform.adress.data, checkoutform.checkoutmessage.data, current_amount, discount, final_amount, datetime.datetime.now().strftime('%d.%m.%Y'), orderid)
			usrmsg.html = '<p style="margin:0px;font-size:17px;">Здравейте {0} {1},<br><br>Благодарим Ви, че пазарувахте от нас. Вашата поръчка ще бъде обработена до 24 часа и ще получите допълнителен E-mail, когато бъде изпратена.<br><br>Информация относно поръчката:</p><b>Номер на поръчка:</b> {11}<br><b>Метод на доставка:</b> {2} <br><b>Община:</b> {3} <br><b>Град/Село:</b> {4} <br><b>Адрес на получаване:</b> {5} <br><b>Дата на поръчка:</b> {10} <br><b>Допълнителна информация:</b> {6} <br><br><b>Междинна сума:</b> {7} лв.<br><b>Отстъпка:</b> {8} лв.<br><b>Крайна сума:</b> {9} лв.<br><br><b>Вашите продукти:</b> <br>'.format(checkoutform.fname.data, checkoutform.lname.data, shippingmethod, checkoutform.province.data, checkoutform.city.data, checkoutform.adress.data, checkoutform.checkoutmessage.data, current_amount, discount, final_amount, datetime.datetime.now().strftime('%d.%m.%Y'), orderid)
			for element in product_data:
				msg.body = msg.body + element + " x " + product_data[element] + "\n"
				usrmsg.html = usrmsg.html + element + " x " + product_data[element] + " бр.<br>"

			usrmsg.html = usrmsg.html + "<br><br>*Плащането се извършва с наложен платеж.<br>**Пратката има право на преглед.<br>***Доставката не е включена в цената.<br><br><p style='margin:0px;font-size:17px;'>Ако имате въпроси, можете директно да отговорите на това съобщение.</p><br><br>"
			usrmsg.html = usrmsg.html + render_template('email_signature.html')
			mail.send(msg)
			mail.send(usrmsg)

			if request.cookies:
				for item in request.cookies:
					if item in products_names:
						update = Product.query.filter_by(product_name=item).first()
						update.product_quantity = update.product_quantity - int(request.cookies.get(item))

				db.session.commit()

			cart_counter = 0
			resp = make_response(render_template('completedorder.html', cart_counter=cart_counter, accepted_cookies=accepted_cookies))

			if request.cookies:
				for item in request.cookies:
					if item in products_names:
						resp.delete_cookie(str(item))

			return resp

		current_amount = 0
		discount = 0
		final_amount = 0
		product_count = 0

		for orderproduct in product_data:
			current_amount = current_amount + (int(product_data[orderproduct]) * Product.query.filter_by(product_name=orderproduct).first().product_price)
			product_count = product_count + int(product_data[orderproduct])

		if product_count == 2:
			discount = current_amount * 0.1
		elif product_count >= 3:
			discount = current_amount * 0.15
		else:
			discount = 0

		final_amount = current_amount - discount

		return render_template('checkout.html', currentamount=current_amount, discount=discount, finalamount=final_amount, form=checkoutform, cart_counter=cart_counter, accepted_cookies=accepted_cookies)

	return render_template('shoppingcart.html', products=products, cart_counter=cart_counter, accepted_cookies=accepted_cookies, product_data=OrderedDict(sorted(product_data.items())))

@app.route('/termsofservice', methods=['GET', 'POST'])
def termsofservice():
	accepted_cookies = False
	current_date = datetime.datetime.now()
	expire_date_accept_cookies = current_date + datetime.timedelta(days=365)
	expire_date_cookies = current_date + datetime.timedelta(days=14)
	cart_counter = 0
	products_names = []
	products = Product.query.all()
	no_quantity = False

	if 'accept_cookies' in request.cookies:
		accepted_cookies = True

	if request.cookies:
		for product in products:
			products_names.append(product.product_name)

	error_resp = make_response(redirect(url_for('termsofservice')))
	if request.cookies:
		for item in request.cookies:
			if item in products_names:
				validate_quantity = int(request.cookies.get(item))
				db_item_quantity = Product.query.filter_by(product_name=item).first().product_quantity

				if db_item_quantity < validate_quantity:
					no_quantity = True

					if db_item_quantity == 0:
						error_resp.delete_cookie(str(item))
					else:
						error_resp.set_cookie(str(item), str(db_item_quantity), expires=expire_date_cookies)

	if no_quantity:
		return error_resp

	if request.method == 'POST' and 'newsletteremail' in request.form:

		msg = Message('Newsletter', recipients=['leagueofnobles.store@gmail.com'])
		msg.body = 'Email: {0}'.format(request.form['newsletteremail'])
		mail.send(msg)

		usrmsg = Message('Записване за бюлетин', recipients=[request.form['newsletteremail']])
		usrmsg.html = 'Здравейте, <br><br>Благодарим Ви, че се записахте за нашия информационен бюлетин. Чрез него ще получавате новини и промени относно League of Nobles, лимитирани оферти и кодове за отстъпки.<br><br>Поздрави,<br>Екипът на League of Nobles<br><br><br>'
		usrmsg.html = usrmsg.html + render_template('email_signature.html')
		mail.send(usrmsg)

	# User agrees to cookies
	if request.method == 'POST' and 'accept_cookies' in request.form:
		resp = make_response(redirect(url_for('termsofservice')))
		resp.set_cookie('accept_cookies', str(True), expires=expire_date_accept_cookies)
		return resp

	if request.cookies:
		for item in request.cookies:
			if item in products_names:
				cart_counter = cart_counter + int(request.cookies.get(item))

	return render_template('termsofservice.html', cart_counter=cart_counter, accepted_cookies=accepted_cookies)

@app.route('/privacypolicy', methods=['GET', 'POST'])
def privacypolicy():
	accepted_cookies = False
	current_date = datetime.datetime.now()
	expire_date_accept_cookies = current_date + datetime.timedelta(days=365)
	expire_date_cookies = current_date + datetime.timedelta(days=14)
	cart_counter = 0
	products_names = []
	products = Product.query.all()
	no_quantity = False

	if 'accept_cookies' in request.cookies:
		accepted_cookies = True

	if request.cookies:
		for product in products:
			products_names.append(product.product_name)

	error_resp = make_response(redirect(url_for('privacypolicy')))
	if request.cookies:
		for item in request.cookies:
			if item in products_names:
				validate_quantity = int(request.cookies.get(item))
				db_item_quantity = Product.query.filter_by(product_name=item).first().product_quantity

				if db_item_quantity < validate_quantity:
					no_quantity = True

					if db_item_quantity == 0:
						error_resp.delete_cookie(str(item))
					else:
						error_resp.set_cookie(str(item), str(db_item_quantity), expires=expire_date_cookies)

	if no_quantity:
		return error_resp

	if request.method == 'POST' and 'newsletteremail' in request.form:

		msg = Message('Newsletter', recipients=['leagueofnobles.store@gmail.com'])
		msg.body = 'Email: {0}'.format(request.form['newsletteremail'])
		mail.send(msg)

		usrmsg = Message('Записване за бюлетин', recipients=[request.form['newsletteremail']])
		usrmsg.html = 'Здравейте, <br><br>Благодарим Ви, че се записахте за нашия информационен бюлетин. Чрез него ще получавате новини и промени относно League of Nobles, лимитирани оферти и кодове за отстъпки.<br><br>Поздрави,<br>Екипът на League of Nobles<br><br><br>'
		usrmsg.html = usrmsg.html + render_template('email_signature.html')
		mail.send(usrmsg)

	# User agrees to cookies
	if request.method == 'POST' and 'accept_cookies' in request.form:
		resp = make_response(redirect(url_for('privacypolicy')))
		resp.set_cookie('accept_cookies', str(True), expires=expire_date_accept_cookies)
		return resp

	if request.cookies:
		for item in request.cookies:
			if item in products_names:
				cart_counter = cart_counter + int(request.cookies.get(item))

	return render_template('privacypolicy.html', cart_counter=cart_counter, accepted_cookies=accepted_cookies)

@app.route('/error', methods=['GET', 'POST'])
def error():
	accepted_cookies = False
	current_date = datetime.datetime.now()
	expire_date_accept_cookies = current_date + datetime.timedelta(days=365)
	expire_date_cookies = current_date + datetime.timedelta(days=14)
	cart_counter = 0
	products_names = []
	products = Product.query.all()
	no_quantity = False

	if 'accept_cookies' in request.cookies:
		accepted_cookies = True

	if request.cookies:
		for product in products:
			products_names.append(product.product_name)

	error_resp = make_response(redirect(url_for('error')))
	if request.cookies:
		for item in request.cookies:
			if item in products_names:
				validate_quantity = int(request.cookies.get(item))
				db_item_quantity = Product.query.filter_by(product_name=item).first().product_quantity

				if db_item_quantity < validate_quantity:
					no_quantity = True

					if db_item_quantity == 0:
						error_resp.delete_cookie(str(item))
					else:
						error_resp.set_cookie(str(item), str(db_item_quantity), expires=expire_date_cookies)

	if no_quantity:
		return error_resp

	if request.method == 'POST' and 'newsletteremail' in request.form:

		msg = Message('Newsletter', recipients=['leagueofnobles.store@gmail.com'])
		msg.body = 'Email: {0}'.format(request.form['newsletteremail'])
		mail.send(msg)

		usrmsg = Message('Записване за бюлетин', recipients=[request.form['newsletteremail']])
		usrmsg.html = 'Здравейте, <br><br>Благодарим Ви, че се записахте за нашия информационен бюлетин. Чрез него ще получавате новини и промени относно League of Nobles, лимитирани оферти и кодове за отстъпки.<br><br>Поздрави,<br>Екипът на League of Nobles<br><br><br>'
		usrmsg.html = usrmsg.html + render_template('email_signature.html')
		mail.send(usrmsg)

	# User agrees to cookies
	if request.method == 'POST' and 'accept_cookies' in request.form:
		resp = make_response(redirect(url_for('error')))
		resp.set_cookie('accept_cookies', str(True), expires=expire_date_accept_cookies)
		return resp

	if request.cookies:
		for item in request.cookies:
			if item in products_names:
				cart_counter = cart_counter + int(request.cookies.get(item))

	return render_template('error.html', cart_counter=cart_counter, accepted_cookies=accepted_cookies)

@app.route('/cancelnewsletter', methods=['GET', 'POST'])
def cancelnewsletter():
	accepted_cookies = False
	current_date = datetime.datetime.now()
	expire_date_accept_cookies = current_date + datetime.timedelta(days=365)
	expire_date_cookies = current_date + datetime.timedelta(days=14)
	cart_counter = 0
	products_names = []
	products = Product.query.all()
	no_quantity = False

	if 'accept_cookies' in request.cookies:
		accepted_cookies = True

	if request.cookies:
		for product in products:
			products_names.append(product.product_name)

	error_resp = make_response(redirect(url_for('cancelnewsletter')))
	if request.cookies:
		for item in request.cookies:
			if item in products_names:
				validate_quantity = int(request.cookies.get(item))
				db_item_quantity = Product.query.filter_by(product_name=item).first().product_quantity

				if db_item_quantity < validate_quantity:
					no_quantity = True

					if db_item_quantity == 0:
						error_resp.delete_cookie(str(item))
					else:
						error_resp.set_cookie(str(item), str(db_item_quantity), expires=expire_date_cookies)

	if no_quantity:
		return error_resp

	if request.method == 'POST' and 'cancelnewslettersub' in request.form:
		msg = Message('Newsletter cancel', recipients=['leagueofnobles.store@gmail.com'])
		msg.body = 'Canceled email: {0}'.format(request.form['cancelnewslettersub'])
		mail.send(msg)

		usrmsg = Message('Oтписване от бюлетин', recipients=[request.form['cancelnewslettersub']])
		usrmsg.html = 'Здравейте,<br><br>Вие успешно се отписахте от нашия бюлетин. Ако имате някакви впечатления, оплаквания или коментари, ще сме благодарни да ги чуем. Можете да се свържите с нас като отговорите директно на това съобщение.<br><br><br>'
		usrmsg.html = usrmsg.html + render_template('email_signature.html')
		mail.send(usrmsg)

		return render_template('successfulnlcancel.html', cart_counter=cart_counter, accepted_cookies=accepted_cookies)

	if request.method == 'POST' and 'newsletteremail' in request.form:

		msg = Message('Newsletter', recipients=['leagueofnobles.store@gmail.com'])
		msg.body = 'Email: {0}'.format(request.form['newsletteremail'])
		mail.send(msg)

		usrmsg = Message('Записване за бюлетин', recipients=[request.form['newsletteremail']])
		usrmsg.html = 'Здравейте, <br><br>Благодарим Ви, че се записахте за нашия информационен бюлетин. Чрез него ще получавате новини и промени относно League of Nobles, лимитирани оферти и кодове за отстъпки.<br><br>Поздрави,<br>Екипът на League of Nobles<br><br><br>'
		usrmsg.html = usrmsg.html + render_template('email_signature.html')
		mail.send(usrmsg)

	# User agrees to cookies
	if request.method == 'POST' and 'accept_cookies' in request.form:
		resp = make_response(redirect(url_for('cancelnewsletter')))
		resp.set_cookie('accept_cookies', str(True), expires=expire_date_accept_cookies)
		return resp

	if request.cookies:
		for item in request.cookies:
			if item in products_names:
				cart_counter = cart_counter + int(request.cookies.get(item))

	return render_template('cancelnewsletter.html', cart_counter=cart_counter, accepted_cookies=accepted_cookies)

@app.errorhandler(404)
def error404(e):

	return render_template('404.html'), 404

@app.errorhandler(500)
def error500(e):

	return render_template('500.html'), 500

if __name__ == '__main__':
	app.run()
