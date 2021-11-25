# The Accounts app

This Django app forms part of the MUYA Workspace for Collaborative Editing. It is used for account management.

The account creation process is initiated by a staff user in the Django admin interface using the email address of the
new user which also acts as the username. The new user is then emailed a link to complete the account set up. Once a
user has created their account they can edit their details and reset their password using the account management
interface provided in the app. Permissions and group membership are managed by staff users in the Django admin
interface. User documentation for creating and managing users is included in the code for the main Django project.

## Configuration/Dependencies

This app has been tested with Django 3.2.

The following configurations are required in the Django settings file:

```python
LOGIN_URL = '/accounts/login/'
AUTH_USER_MODEL = 'accounts.User'
```

If the api app is also being used, there is an optional configuration which determines which of the user fields will be
used for the 'created_by' and 'last_modified_by' fields in any model which inherits the api BaseModel class. This
should be set to the field in the accounts user model which you want to be used for this purpose, for example:

```python
USER_IDENTIFIER_FIELD = 'full_name'
```

For testing the password reset and other email based functions locally, a file based system can be configured as
follows:

```python
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")
```

In production, a working email backend must be configured following the django documentation here:
https://docs.djangoproject.com/en/3.2/topics/email/#email-backends

The default setup expects a privacy statement named `privacy.html` to be available in the templates directory of the
main Django project. If this is not available or required the account app templates will need to be edited to remove
all links and references to the privacy statement.

## License

This app is licensed under the GNU General Public License v3.0.


## Acknowledgments

This application was released as part of the Multimedia Yasna Project funded by the European Union Horizon 2020
Research and Innovation Programme (grant agreement 694612).

The software was created by Catherine Smith and Liam Carrington at the Institute for Textual Scholarship and Electronic
Editing (ITSEE) in the University of Birmingham. It is based on a suite of tools developed for and supported by the
following research projects:

- The Workspace for Collaborative Editing (AHRC/DFG collaborative project 2010-2013)
- COMPAUL (funded by the European Union 7th Framework Programme under grant agreement 283302, 2011-2016)
- CATENA (funded by the European Union Horizon 2020 Research and Innovation Programme under grant agreement 770816,
  2018-2023)
