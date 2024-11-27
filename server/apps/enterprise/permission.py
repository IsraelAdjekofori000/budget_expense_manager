from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Grants permission when the user is an organization admin
    
    
    Models that use this permission class should provide a get_org method()
    that returns the associated organization
    """

    def has_object_permission(self, request, view, obj):
        return request.user.has_perm('enterprise.AD', obj.get_org())


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.associate.pk == request.user.pk
