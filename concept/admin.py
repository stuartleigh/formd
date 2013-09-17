from django.contrib import admin

from concept.models import Concept, Message


class ConceptAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'user', 'active',)
    list_editable = ('active',)
    search_fields = ('code', 'user__email',)
    list_filter = ('active', )
    readonly_fields = ('code',)
admin.site.register(Concept, ConceptAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'message_id', 'concept', 'sent', 'created_at',)
    search_fields = ('message_id', 'concept__code', 'concept__user__email')
    list_filter = ('sent', )
    readonly_fields = ('message_id', 'concept', 'created_at', 'sent')

    def has_add_permission(self, request):
    	return False
admin.site.register(Message, MessageAdmin)