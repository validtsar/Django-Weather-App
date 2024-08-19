from .models import *
from .forms import *




class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        profiles = User.objects.all()
        context['profiles'] = profiles
        if 'profile_selected' not in context:
            context['profile_selected'] = 0
            return context
