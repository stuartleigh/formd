from functools import wraps

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

def plan_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            request.user.plan
        except ObjectDoesNotExist as e:
            messages.warning(request, 'You must sign up to a plan before getting started.')
            return redirect('my-plan')
        return func(request, *args, **kwargs)
    return wrapper