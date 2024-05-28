from rest_framework import permissions


class IsAdmin(permissions.IsAdminUser):
    def has_permission(self, request, view):
        return (
            (request.user.is_authenticated and request.user.admin_role)
            or super().has_permission(request, view)
        )


class IsModerator(IsAdmin):
    def has_permission(self, request, view):
        return (
            (request.user.is_authenticated and request.user.moderator_role)
            or super().has_permission(request, view)
        )


class IsAdminOrReadOnly(IsAdmin):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or super().has_permission(request, view)
        )


class AuthorAdminModerOrReadOnly(IsModerator):
    """Разрешение доступа для чтения всем, а для небезопасных запросов
    админу, модератору, автору"""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.method in permissions.SAFE_METHODS
            or super().has_permission(request, view)
        )


class IsAdminOrSelf(IsAdmin):
    def has_permission(self, request, view):
        return (
            (view.detail
             and request.user.is_authenticated
             and view.action in ('retrieve', 'partial_update', 'destroy'))
            or super().has_permission(request, view)
        )

    def has_object_permission(self, request, view, obj):
        return (
            (request.user == obj and view.me)
            or super().has_permission(request, view)
        )
