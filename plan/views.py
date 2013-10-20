from django import http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template.response import TemplateResponse

from account.forms import StripeTokenForm

from .models import Plan
from .forms import ChangePlanForm

@login_required
def my_plan(request):

    plans = Plan.objects.filter(selectable=True).order_by('rate')

    if request.method == "POST":
        if "stripeToken" in request.POST:
            stripeForm = StripeTokenForm(request.POST, user=request.user)
            if stripeForm.is_valid():
                stripeForm.save()
            else:
                import ipdb; ipdb.set_trace()

        planForm = ChangePlanForm(request.POST, user=request.user)
        if planForm.is_valid():
            planForm.save()

        messages.success(request, "Plan changed successfully")
        return redirect('my-account')

    context = {
        "plans": plans,
        "publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
    }

    return TemplateResponse(request, 'account/my_plan.html', context)