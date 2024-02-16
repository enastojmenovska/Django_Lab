from django.contrib import admin
from .models import Post, Comment, Blogger, BloggerBlockedUser
from rangefilter.filters import DateRangeFilter

# Register your models here.

"""
username1: admin
pass1: admin12345

username2:ana
pass2:ena12345

username3:ena
pass3:ena12345

username4:jana
pass4:ena12345

"""


class CommentAdmin(admin.ModelAdmin):
    list_display = ["content", "date"]
    model = Comment
    exclude = ("blogger",)

    def save_model(self, request, obj, form, change):
        obj.blogger = Blogger.objects.get(user=request.user)
        return super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'post':
            if request.user.is_authenticated:
                blocked_bloggers = BloggerBlockedUser.objects.filter(blocked_user=request.user).values_list("blogger",
                                                                                                            flat=True)
                kwargs['queryset'] = db_field.related_model.objects.exclude(author__user__in=blocked_bloggers)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and (request.user == obj.post.author.user or request.user == obj.blogger.user):
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and (request.user == obj.post.author.user or request.user == obj.blogger.user):
            return True
        return False


admin.site.register(Comment, CommentAdmin)


class CommentInlineAdmin(admin.StackedInline):
    model = Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    search_fields = ("title__contains", "content__contains")
    list_filter = (
        ("date_creation", DateRangeFilter),
    )
    list_display = ["title", "author"]
    model = Post
    exclude = ("author",)
    inlines = [CommentInlineAdmin, ]

    def save_model(self, request, obj, form, change):
        obj.author = Blogger.objects.get(user=request.user)
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # blocked_bloggers = Blogger.objects.filter(blocked_users=request.user)
        blogger = Blogger.objects.get(user=request.user)
        blogger_blocked_by = BloggerBlockedUser.objects.filter(blocked_user=blogger.user).values_list('blogger',
                                                                                                      flat=True)
        return qs.exclude(author__in=blogger_blocked_by)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and request.user == obj.author.user:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and request.user == obj.author.user:
            return True
        return False


admin.site.register(Post, PostAdmin)


class BloggerBlockedUserAdmin(admin.StackedInline):
    model = BloggerBlockedUser
    extra = 0


class BloggerAdmin(admin.ModelAdmin):
    model = Blogger

    inlines = [BloggerBlockedUserAdmin, ]

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and request.user == obj.user:
            return True
        return False


admin.site.register(Blogger, BloggerAdmin)
