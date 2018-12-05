from django import forms

from django.contrib.auth import authenticate
from app.models import xss,ccpa
from django.contrib.auth.forms import AuthenticationForm

from django.utils.translation import ugettext_lazy, ugettext as _

from django.contrib.auth import get_user_model

ERROR_MESSAGE = ugettext_lazy("Please enter the correct username and password "
                              "for a staff account. Note that both fields are case-sensitive.")


class AdminAuthenticationForm(AuthenticationForm):
    """
    A custom authentication form used in the admin app.

    """
    this_is_the_login_form = forms.BooleanField(
        widget=forms.HiddenInput, initial=1,
        error_messages={'required': ugettext_lazy("Please log in again, because your session has expired.")})

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        message = ERROR_MESSAGE

        if username and password:
            self.user_cache = authenticate(
                username=username, password=password)
            if self.user_cache is None:
                if u'@' in username:
                    User = get_user_model()
                    # Mistakenly entered e-mail address instead of username? Look it up.
                    try:
                        user = User.objects.get(email=username)
                    except (User.DoesNotExist, User.MultipleObjectsReturned):
                        # Nothing to do here, moving along.
                        pass
                    else:
                        if user.check_password(password):
                            message = _("Your e-mail address is not your username."
                                        " Try '%s' instead.") % user.username
                raise forms.ValidationError(message)
            elif not self.user_cache.is_active or not self.user_cache.is_staff:
                raise forms.ValidationError(message)
        return self.cleaned_data


class StuAuthenticationForm(AuthenticationForm):
    """
    A custom authentication form used in the admin app.

    """
    this_is_the_login_form = forms.BooleanField(
        widget=forms.HiddenInput, initial=1,
        error_messages={'required': ugettext_lazy("Please log in again, because your session has expired.")})

    def clean(self):
        name = self.cleaned_data.get('name')
        icc = self.cleaned_data.get('icc')
        card_no = self.cleaned_data.get('card_no')
        message = ERROR_MESSAGE

        if name and icc and card_no:
            self.user_cache = None
            if self.user_cache is None:
                # User = xss()
                # Mistakenly entered e-mail address instead of username? Look it up.
                try:
                    xssuser = xss.objects.filter(name=name,icc=icc,card_no=card_no)
                    ccpauser = ccpa.objects.filter(name=name,icc=icc,card_no=card_no)
                except (xss.DoesNotExist, xss.MultipleObjectsReturned):
                    # Nothing to do here, moving along.
                    pass
                raise forms.ValidationError(message)
            elif not self.user_cache.is_active or not self.user_cache.is_staff:
                raise forms.ValidationError(message)
        return self.cleaned_data
