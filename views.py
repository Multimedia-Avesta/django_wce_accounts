from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
    LoginView, LogoutView
)
from .forms import EditAccountForm, AccountCreationForm
from .models import User


class Update(LoginRequiredMixin, generic.UpdateView):
    form_class = EditAccountForm
    template_name = 'accounts/edit_profile.html'

    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
        context['back_url'] = self.request.GET.get('back')
        context.update(kwargs)
        return super().get_context_data(**context)

    def form_valid(self, form):
        self.object = form.save()
        self.object.save()
        if self.request.POST.get('back_url') != 'None':
            return HttpResponseRedirect('/accounts/profile?back={}'.format(self.request.POST.get('back_url')))
        return HttpResponseRedirect('/accounts/profile')

    def get_object(self):
        return self.request.user


class Profile(LoginRequiredMixin, generic.DetailView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
        context['back_url'] = self.request.GET.get('back')
        context.update(kwargs)
        return super().get_context_data(**context)

    def get_object(self):
        return self.request.user


class AccountLoginView(LoginView):
    template_name = 'accounts/login.html'


class AccountLogoutView(LogoutView):
    template_name = 'accounts/logged_out.html'


class AccountPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        context['back_url'] = self.request.GET.get('back')
        return context

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        if self.request.POST.get('back_url') != 'None':
            return HttpResponseRedirect('done?back={}'.format(self.request.POST.get('back_url')))
        return HttpResponseRedirect('done')


class AccountPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        context['back_url'] = self.request.GET.get('back')
        return context


class AccountPasswordResetView(PasswordResetView):
    email_template_name = 'accounts/password_reset_email.html'
    from_email = 'itsee@contacts.bham.ac.uk'
    subject_template_name = 'accounts/password_reset_subject.txt'
    template_name = 'accounts/password_reset_form.html'


class AccountPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class AccountPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'

    # these functions overwrite the core ones so that if a profile hasn't been created the AccountCeateionView
    # data is used. This closes a loop hole that allowed users to reset passwords before they created a profile.
    def get_form_class(self):
        """Return the form class to use."""
        if self.user.full_name == '':
            return AccountCreateView.form_class
        return self.form_class

    def get_template_names(self):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response() is overridden.
        """
        if self.user.full_name == '':
            self.form_class = AccountCreationForm
            self.success_url = reverse_lazy('account_creation_complete')
            return[AccountCreateView.template_name]
        if self.template_name is None:
            raise ImproperlyConfigured(
                "TemplateResponseMixin requires either a definition of "
                "'template_name' or an implementation of 'get_template_names()'")
        else:
            return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.user.full_name == '':
            context.update({
                'email': self.get_form().get_user_email()
            })
        return context


class AccountPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


class AccountCreateView(PasswordResetConfirmView):
    template_name = 'accounts/register.html'
    form_class = AccountCreationForm
    success_url = reverse_lazy('account_creation_complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'email': self.get_form().get_user_email()
        })
        return context


class AccountCreationCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/account_creation_complete.html'


@login_required(login_url='/accounts/login/')
def view_profile(request):
    user = request.user
    args = {'user': user}
    return render(request, 'accounts/profile.html', args)


def privacy_statement(request):
    return render(request, 'privacy.html')
