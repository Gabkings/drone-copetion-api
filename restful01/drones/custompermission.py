from rest_framework import permissions

class IsCurrentUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self,request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # the method is a safe method
            return True
        else:
            # The method isn't safe method
            # Only user are granted permissions for unsafe methods
            return obj.owner == request.user
            
