# Leagueofnobles Website

## Project description
[League of Nobles](https://www.leagueofnobles.com/) is an [E-Commerce](https://en.wikipedia.org/wiki/E-commerce) website created from scratch as a side project using Python, Flask, HTML5, CSS3 and JavaScript. The deployment in production mode is done using an Ubuntu virtual machine on Azure Cloud Services in order to increase stability, server uptime and security and at the same time decrease costs.

## Main features of the website

- Completely responsive (works on all types of devices and screen sizes).
- A database created with SQLAlchemy containing information about the product assortment. Automatically updates when changes are made (ex. updates available product quantity when a sale is made).
- Multipage catalogue containing all the products offered for sale.
- Shopping cart with a fully operational checkout system.
- Functional "Contact us" page and a newsletter feature.

## Project deployment

1. Create a virtual machine on a cloud service provider (in this particular case Azure). Alternative to that would be to use an own device for the purpose of being a server. **Note that ports 443 (HTTPS) and 80 (HTTP) must be opened in order to allow incoming traffic**.
2. Clone the repository `git clone https://github.com/KristofarStavrev/leagueofnobles-website.git` and create a `config.json` file inside of it with the following structure.

```
{
 "SECRET_KEY" : "YOUR_SECRET_KEY",
 "RECAPTCHA_PUBLIC_KEY" : "YOUR_PUBLIC_KEY",
 "RECAPTCHA_PRIVATE_KEY" : "YOUR_PRIVATE_KEY",
 "MAIL_SERVER" : "MAIL_SERVER_OF_CHOICE",
 "MAIL_PORT" : MAIL_PORT_OF_CHOICE,
 "MAIL_USE_SSL" : TRUE_FALSE,
 "MAIL_USE_TLS" : TRUE_FALSE,
 "MAIL_USERNAME" : "YOUR_EMAIL_USERNAME",
 "MAIL_PASSWORD" : "YOUR_EMAIL_PASSWORD",
 "MAIL_DEFAULT_SENDER" : "YOUR_DEFAULT_SENDER",
 "SQLALCHEMY_DATABASE_URI" : "sqlite:///site.db"
}
```

3. Create a virtual environment and install the dependencies found in `requirments.txt`.
4. Setting up Nginx:
  - `sudo apt install nginx`
  - `sudo rm /etc/nginx/sites-enabled/default`
  - `sudo nano /etc/nginx/sites-enabled/leagueofnobles`
  - Place the following code in the newly created file:

```
server {
    listen 80;
    server_name PUBLIC_IP_OR_DOMAIN_NAME;

    location /static {
        alias /home/USER/PROJECT_DIR/static;
    }

    location / {
        proxy_pass http://localhost:8000;
        include /etc/nginx/proxy_params;
        proxy_redirect off;
    }
}
```
  - `sudo systemctl restart nginx`

5. Setting up Gunicorn:
  - `pip install gunicorn`
  - Execute the following command in the project folder: `gunicorn -w 3 main:app` (gunicorn -w (2 x num_cores) + 1 main:app).
  - The number of cores on the machine can be checked with the command `nproc --all`.
  - After following the above steps the website should be now up and running.

6. (BONUS) Choosing a DNS provider is necessary for obtaining a custom domain name.
  - **If a custom domain name is used the `server_name` in the nginx configuration file created in the above steps needs to be updated.**

7. (BONUS) For an SSL encryption it is recommended to use [Let's encrypt](https://letsencrypt.org/). Using the "Certbot" follow the steps for creating an SSL certificate.

## Known issue with using Gmail SMTP for sending automatic emails

This issue can arise if the script has not accessed the Gmail API necessary for sending automatic emails for a prolonged period of time. It occurs in the following scenarios:
- When signing up for the newsletter.
- When sending a message using the 'Contact us' form.
- When completing an order.

The error thrown in the log usually resembles something along the lines of `smtp authentication error 534`.

Fix for the error can be found on the following [link](https://support.google.com/mail/answer/7126229?hl=en&authuser=1#zippy=%2Cstep-check-that-imap-is-turned-on%2Cstep-change-smtp-other-settings-in-your-email-client%2Ci-cant-sign-in-to-my-email-client).

Usually, the issue is resolved by allowing less secure apps to access your account and/or following the steps for the DisplayUnlockCaptcha section.

## Visual examples of the website

### Image 1: Home Page

![alt text](docs/img/image1.png)

### Image 2: Assortment Catalogue First Row

![alt text](docs/img/image2.png)

### Image 3: Assortment Catalogue Second Row and Footer

![alt text](docs/img/image3.png)

### Image 4: FAQ Page

![alt text](docs/img/image4.png)

### Image 5: Shopping Cart 1

![alt text](docs/img/image5.png)

### Image 6: Shopping Cart 2

![alt text](docs/img/image6.png)

### Image 7: Checkout 1

![alt text](docs/img/image7.png)

### Image 8: Checkout 2

![alt text](docs/img/image8.png)

### Image 9: Empty Shopping Cart

![alt text](docs/img/image9.png)

### Image 10: Contact Us Page

![alt text](docs/img/image10.png)
