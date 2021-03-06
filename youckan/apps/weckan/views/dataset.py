# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import DetailView

from youckan.apps.youckan.models import Dataset


class DatasetView(DetailView):
    template_name = 'dataset.html'
    context_object_name = 'dataset'
    model = Dataset
    slug_field = 'name'
