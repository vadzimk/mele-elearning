from rest_framework import serializers

from courses.models import Subject, Course, Module


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        # specifies fields to be included in json, if not specified, all are included
        fields = ['id', 'title', 'slug']


class ModuleSerializer(serializers.ModelSerializer):
    class Meat:
        model = Module
        fields = ['order', 'title', 'description']


class CourseSerializer(serializers.ModelSerializer):
    # nested serializer allows to serialize one-many relationship - include fields from the many side
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug',
                  'overview', 'created', 'owner',
                  'modules']
