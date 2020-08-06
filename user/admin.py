from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'nickname', 'avatar', 'email', 'is_staff', 'is_active', 'is_superuser')

    def nickname(self, obj):
        return obj.profile.nickname

    def avatar(self, obj):
        return obj.profile.avatar

    nickname.short_description = '昵称'
    avatar.short_description = '头像'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname')
