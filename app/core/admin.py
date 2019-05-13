from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		(_('Personal Info'), {'fields': ('name',)}),
		(_('Permissions'), {
			'fields': (
				'is_staff',
				'is_active',
				'is_superuser'
			)}),
		(_('Important dates'), {'fields': ('last_login',)})
	)

	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'password1', 'password2'),
		}),
	)

	ordering = ['id']
	list_display = ['email', 'name']
	search_fields = ['email', 'name']


admin.site.register(models.User, UserAdmin)
