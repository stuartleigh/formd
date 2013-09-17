from django.contrib import admin

from plan.models import Plan, UserPlan

class PlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rate', 'domain_limit', 'form_limit', 'message_limit', 'selectable')
    list_editable = ('selectable',)
    list_filter = ('selectable',)
admin.site.register(Plan, PlanAdmin)

class UserPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'rate', 'domain_limit', 'form_limit', 'message_limit', 'modified_time',)
    readonly_fields = ('modified_time',)
admin.site.register(UserPlan, UserPlanAdmin)