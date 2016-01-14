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
   (django-bootstrap3):

        INSTALLED_APPS = (
            # ...
            'drchrono_birthday',
            'bootstrap3',
        )

3. Configure the app in your project's `urls.py`, with the namespace
   `drchrono_birthday`:

        urlpatterns = [
            # ...
            url(r'^birthday/', include('drchrono_birthday.urls',
                                      namespace="drchrono_birthday")),
        ]

4. drchrono Birthday lets the project handle user authentication.  See Django's
   documentation on `login_required()`.
5. Set up your drchrono API key and OAuth client secrets file.  Refer to
   drchrono for information obtaining the API key.  The client secrets file
   format:

        {
            "web": {
                "client_id": "drchrono client ID",
                "client_secret": "drchrono client secret",
                "redirect_uris": ["http://your-site.example.com/birthday/auth_return/"],
                "auth_uri": "https://drchrono.com/o/authorize/",
                "token_uri": "https://drchrono.com/o/token/"
            }
        }

    Put this file somewhere and configure drchrono Birthday with the path in
    your project's `settings.py`:

        DRCHRONO_BIRTHDAY_SECRETS = "/opt/drchrono-birthday/client_secrets.json"

3. Set up SMTP.  Edit the file `management/commands/sendbirthdaymessages.py` and
   define the function `configure_smtp()`.  This function should return a Python
   `smtplib.SMTP` object that is configured and authenticated accordingly.
   Also, edit the constant `_FROM_ADDR` in the same file with the desired
   sending address for birthday emails.
6. Configure SMTP.  An example config is included (`config.ini`).  Edit it and
   save it somewhere to use in the next step.
4. Set up a cron job to run the custom command `python2 manage.py
   sendbirthdaymessages /opt/drchrono-birthday/config.ini` daily.

drchrono Birthday requires the default set of Django installed apps and
middleware and may not work if some of them are missing.

drchrono Birthday relies on Django's native authentication library.  User
authentication and/or registration should be handled by your project.

Sending emails
--------------

drchrono Birthday's custom `sendbirthdaymessages` command will send message for
all birthdays that have happened since the last time the command was run up to
and including the current day.  This "memory" is ignored on the first run (which
only sends messages for the current day) and is limited to one week in the past,
to prevent sending messages for extremely old birthdays.

The server should be up and configured to run this command daily; this "memory"
feature is to ameliorate small bugs in deployment.  It may be undesirable in
extreme edge cases, or when the timezone or system clock is experiencing
fluctuations; in such cases, use the admin interface to edit the database and
delete the `last_sent` key in the `Global` model.

License
-------

Copyright (C) 2015-2016  Allen Li

This file is part of drchrono Birthday.

drchrono Birthday is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

drchrono Birthday is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with drchrono Birthday.  If not, see <http://www.gnu.org/licenses/>.
