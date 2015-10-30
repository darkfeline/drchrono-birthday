drchrono Birthday
=================

drchrono Birthday is a Django app that integrates with
[drchrono][] to send birthday messages to patients.

[drchrono]: (https://www.drchrono.com/) 

Dependencies
------------

- Python 2
- Django 1.8
- oauth2client
- django-bootstrap3

Installation and configuration
------------------------------

Install all of the dependencies.

drchrono Birthday is distributed as a Django app, which is installed as follows:

1. Copy the `drchrono_birthday` directory to your project.
2. Enable the app in your project's `settings.py`, along with `bootstrap3`
   (django-bootstrap3).
3. Configure the app in your project's `urls.py`, with the namespace
   `drchrono_birthday`.  Example:

       url(r'^birthday/', include('drchrono_birthday.urls',
                                  namespace="drchrono_birthday"))

3. Set up SMTP.  Edit the file `management/commands/sendbirthdaymessages.py` and
   define the function `configure_smtp()`.  This function should return a Python
   `smtplib.SMTP` object that is configured and authenticated accordingly.
   Also, edit the constant `_FROM_ADDR` in the same file with the desired
   sending address for birthday emails.
4. Set up a cron job to run the custom command `python2 manage.py
   sendbirthdaymessages` daily.

drchrono Birthday requires the default set of Django installed apps and
middleware and may not work if some of them are missing.

drchrono Birthday relies on Django's native authentication library.  User
authentication and/or registration should be handled by your project.
