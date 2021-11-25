# accounts/admin.py
from os.path import join
from django.utils.crypto import get_random_string
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from .forms import AccountCreationByAdminForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form_template = 'accounts/add_user.html'
    add_form = AccountCreationByAdminForm
    add_fieldsets = (
        (None, {
            'fields': ('email',),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['full_name', 'first_name', 'last_name', 'email', 'last_login', 'date_joined']
        return []

    def save_model(self, request, obj, form, change):
        if not change and (not form.cleaned_data['password1'] or not obj.has_usable_password()):
            obj.set_password(get_random_string())
            obj.username = obj.email
            reset_password = True
        else:
            reset_password = False

        super(CustomUserAdmin, self).save_model(request, obj, form, change)

        if reset_password:
            reset_form = PasswordResetForm({'email': obj.email})
            assert reset_form.is_valid()
            reset_form.save(
                request=request,
                use_https=request.is_secure(),
                from_email='itsee@contacts.bham.ac.uk',
                subject_template_name=join(settings.BASE_DIR,
                                           'accounts/templates/accounts/account_creation_subject.txt'),
                email_template_name=join(settings.BASE_DIR,
                                         'accounts/templates/accounts/account_creation_email.html'),
            )


# Defining fieldsets to add unique ones (full_name etc)
CustomUserAdmin.fieldsets = ((('Personal info'), {'fields': ('first_name', 'last_name',
                                                             'email', 'full_name',)}),
                             (('Important dates'), {'fields': ('last_login', 'date_joined',)}),
                             (('Permissions'), {'fields': ('is_active', 'is_staff',
                                                           'is_superuser', 'groups', 'user_permissions',)}),
                             )

admin.site.register(User, CustomUserAdmin)
