# Happy Days

## Keep track of your mindset

The goal of this project is to help you set up a site on a [Raspberry Pi](https://www.raspberrypi.org) in your own home. The site will let you keep track of how you feel on any given day, and see those days tracked in a graph. Ultimately giving you a better idea of the patterns of your mood and what you can do to stay happy more of the time.

### Software and services used in the project

* [Flask](https://flask.palletsprojects.com)
  - Python based framework, used for the programming back-end.
* [Sqlite](https://www.sqlite.org)
  - Database system to store.. well all of your data.
* [Gunicorn](https://gunicorn.org)
  - Lightweight web server, used to handle our Flask application.
* [Supervisor](http://supervisord.org)
  - Keeps Gunicorn running in case of a crash, or you reboot your Pi.
* [Nginx](https://www.nginx.com)
  - Nginx is a web server that adds speed, security and reliability.
* [Let's Encrypt](https://letsencrypt.org)
  - Free SSL Certificates to keep your site secure with HTTPS.
* [Cloudflare](https://www.cloudflare.com)
  - Free DNS hosting so that you can point your domain name at your Pi, and have the DNS automatically updated if your home's IP address changes.


### Installation

1. Install the newest [Raspberry Pi OS](https://www.raspberrypi.org/software/) on your Pi.
1. Log into your Pi and create a home for your project. I created a Folder called *Sites* in my home directory.
1. `cd` into your new directory and clone this repo.


## To-Do

1. Next/Prev buttons in list view
1. Better HTML Markup
1. Date labels on dashboard graph
1. Custom form errors in HTML
1. Display dynamic slider values 
1. CSS Styling
  1. [Form field styling](https://css-tricks.com/custom-styling-form-inputs-with-modern-css-features/)
  1. Colors and styling on New Entry page
  1. Style list view
1. Fontello icons for nav
1. Account management page
1. Change `created_on` to `created_at` and `modified_on` to `updated_at`
  1. Create migration for this
1. Code cleanup and documentation
1. Project documentation in Git


### Helpful links

* [Flask, nginx, gunicorn, supervisor](https://medium.com/ymedialabs-innovation/deploy-flask-app-with-nginx-using-gunicorn-and-supervisor-d7a93aa07c18)
* [Gunicorn](http://docs.gunicorn.org/en/19.0/settings.html)
* [Flask tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)




