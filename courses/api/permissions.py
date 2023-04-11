from rest_framework.permissions import BasePermission


class IsEnrolled(BasePermission):
    # permission text is IsEnrolled

    def has_object_permission(self, request, view, obj):
        # check that user is present in the Course object
        return obj.students.filter(id=request.user.id).exists()