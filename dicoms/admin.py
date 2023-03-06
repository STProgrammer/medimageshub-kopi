from django.contrib import admin
from .models import DicomFile, DicomFile_User, Patient, Comment

# Register your models here.


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class DicomFileAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]

    list_display_links = None

    list_display = ('file_title', 'owner', 'patient', 'upload_date')

    def has_change_permission(self, request, obj=None):
        return False
    
    def has_view_permission(self, request, obj=None):
        if obj==None:
            return True
        else:
            return False
    
    def has_add_permission(self, request, obj=None):
        return False
    

    list_display_links = None


 
@admin.register(Comment)
class PostAdmin(admin.ModelAdmin):

    list_display = ('author', 'comment_time')
    list_display_links = None
 
    class Meta:
       model = Comment
    
    def has_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        if obj==None:
            return True
        else:
            return False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Patient)
class PostAdmin(admin.ModelAdmin):

    list_display = ('first_name', 'last_name', 'main_doctor')
    readonly_fields = ('first_name', 'birth_date')
    
    def has_add_permission(self, request, obj=None):
        return False
 
    class Meta:
       model = Patient



@admin.register(DicomFile_User)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'dicomfile', 'added_time')
    list_display_links = None

    def has_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        if obj==None:
            return True
        else:
            return False
    
    def has_add_permission(self, request, obj=None):
        return False


    class Meta:
       model = DicomFile_User


admin.site.register(DicomFile, DicomFileAdmin)
