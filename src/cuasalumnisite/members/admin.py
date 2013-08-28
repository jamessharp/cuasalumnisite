from models import *
from django.contrib import admin

class MemberAdmin(admin.ModelAdmin):
    form = MemberForm

class MemberInline(admin.StackedInline):
    model = Member

class UserAdmin(admin.ModelAdmin):
    form = UserForm
    inlines = [MemberInline]

#admin.site.register(Member, MemberAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)