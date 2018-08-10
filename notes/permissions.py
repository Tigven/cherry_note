from rest_framework import permissions

class IsAdminOrIsSelf(permissions.BasePermission):
    """
    Object-level permission to only allow owners and admin of an
    object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        if obj.owner == request.user:
            return True

        return request.user.is_superuser()