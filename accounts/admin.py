from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from accounts.models import User, UserProfile

class UserProfileInline(admin.TabularInline):
    model = UserProfile
    fk_name = 'user'

# @admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'is_staff')
    search_fields = ('email',)
    ordering = ('email',)
    inlines = (UserProfileInline,)


class UserProfileAdmin(admin.ModelAdmin):
    fields = ('desc', )
    search_fields = ('first_name', 'last_name', 'user__email')
    readonly_fields = ['thumb', 'get_name']
    list_display = ('get_name', 'thumb', 'online' )


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

