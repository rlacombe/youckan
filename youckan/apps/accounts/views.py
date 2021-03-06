# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import futures

from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DetailView, UpdateView, ListView, RedirectView
from django.views.generic.detail import SingleObjectMixin

from braces.views import LoginRequiredMixin

from youckan.apps.accounts.forms import UserForm, ProfileFormset, AvatarForm
from youckan.avatar import get_avatar_url
from youckan.models import User, UserProfile
from youckan.views import FormsetsMixin

from django.utils.module_loading import import_by_path


class UserListView(LoginRequiredMixin, ListView):
    template_name = 'accounts/profiles.html'
    model = User
    context_object_name = 'users'


class ProfileView(DetailView):
    template_name = 'accounts/profile.html'
    model = User
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

        widgets = [import_by_path(classname)(self.object) for classname in settings.PROFILE_WIDGETS]
        context['widgets'] = [widget for widget in widgets if widget.can_display(self.request.user)]

        # Parallelize queries
        with futures.ThreadPoolExecutor(max_workers=4) as executor:
            workers = [executor.submit(widget.fill_context, context) for widget in widgets]
        futures.wait(workers)

        return context


class UserViewMixin(object):
    def get_object(self):
        return self.request.user


class ProfileEditView(LoginRequiredMixin, FormsetsMixin, UserViewMixin, UpdateView):
    template_name = 'accounts/profile_edit.html'
    model = User
    form_class = UserForm

    formsets = {
        'profile': ProfileFormset,
    }


class AvatarEditView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/avatar_edit.html'
    model = UserProfile
    form_class = AvatarForm
    success_url = reverse_lazy('avatar-edit')

    def get_object(self):
        return self.request.user.profile


class AvatarView(SingleObjectMixin, RedirectView):
    model = User

    def get_redirect_url(self, size=None, *args, **kwargs):
        user = self.get_object()
        return get_avatar_url(user, size)
