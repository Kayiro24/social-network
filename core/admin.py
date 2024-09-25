from django.contrib import admin


class CreationModificationBaseAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    ordering = ['-created']

    def get_list_display(self, request):
        """Add created, modified to list_display"""
        return list(self.list_display) + ["created", "modified"]
