from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group

from .models import User

from django.contrib.auth.forms import UserCreationForm, UserChangeForm



class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'profession_title',
        'country', 'city', 'postal_code','address','workplace', 'phone_nr', 'birth_date')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'groups',
                                       'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    readonly_fields=('last_login', 'date_joined')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'profession_title',
        'country', 'city', 'postal_code','address','workplace', 'phone_nr', 'birth_date'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'profession_title', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email', 'first_name', 'last_name', 'profession_title', 'is_staff')


    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if obj:
                if isinstance(obj, User):
                    if obj.is_staff:
                        return False
        else:
            if obj:
                if isinstance(obj, User):
                    if obj.is_superuser:
                        return False
            else:
                return True
        return True

    
    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if obj:
                if isinstance(obj, User):
                    if obj.is_staff:
                        return False
        else:
            if obj:
                if isinstance(obj, User):
                    if obj.is_superuser:
                        return False
            else:
                return True
        return True

    
    def change_view(self, request, object_id, extra_context=None):
        if request.user.is_superuser:
            self.exclude = ('password', )
        else:
            if object_id:
                self.exclude = ('password', 'user_permissions', 'groups',)
        return super().change_view(request, object_id, extra_context)
    
    
    def get_fieldsets(self, request, obj=None):
        if not request.user.is_superuser:
            if obj:
                if isinstance(obj, User):
                    fieldsets = (
                        (None, {'fields': ('email',)}),
                        (('Personal info'), {'fields': ('first_name', 'last_name', 'profession_title',
                        'country', 'city', 'postal_code','address','workplace', 'phone_nr', 'birth_date')}),
                        (('Permissions'), {'fields': ('is_active',)}),
                        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
                    )
                    return fieldsets
            else:
                return self.add_fieldsets

        else:
            if obj:
                if isinstance(obj, User):
                    return self.fieldsets
            else:
                return self.add_fieldsets
    

    def get_readonly_fields(self, request, obj=None):
            if not request.user.is_superuser:
                if obj:
                    if isinstance(obj, User):
                        return ('email', 'first_name', 'last_login', 'date_joined', 'birth_date')
                else:
                    return self.readonly_fields
            else:
                if obj:
                    if isinstance(obj, User):
                        return ('email', 'first_name', 'last_login', 'date_joined', 'birth_date')
                return self.readonly_fields
            




    
class GroupAdmin(admin.ModelAdmin):
 
    class Meta:
       model = Group
    
    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False

    def has_view_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False



#admin.site.unregister(Group)

admin.site.register(User, UserAdmin)