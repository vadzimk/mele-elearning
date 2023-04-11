from rest_framework import serializers

from courses.models import Subject


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        # specifies fields to be included in json, if not specified, all are included
        fields = ['id', 'title', 'slug']

