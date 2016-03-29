from django.utils.text import slugify
from rest_framework.serializers import ModelSerializer

from core.serializers import DetailSerializer, FieldSelectorSerializer
from accounts.serializers import UserSerializer
from accounts.models import User
from .models import Organization, Project


class OrganizationSerializer(DetailSerializer, FieldSelectorSerializer,
                             ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = ('id', 'slug', 'name', 'description', 'archived', 'urls',
                  'contacts', 'users')
        read_only_fields = ('id',)
        detail_only_fields = ('users',)

    def to_internal_value(self, data):
        if not data.get('slug'):
            data['slug'] = slugify(data.get('name'))

        return super(OrganizationSerializer, self).to_internal_value(data)


class ProjectSerializer(DetailSerializer, ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'organization', 'country', 'name', 'description',
                  'archived', 'urls', 'contacts', 'users')
        read_only_fields = ('id', 'country',)
        detail_only_fields = ('users',)

    def create(self, validated_data):
        organization = self.context['organization']
        return Project.objects.create(
            organization_id=organization.id,
            **validated_data
        )


class UserAdminSerializer(UserSerializer):
    organizations = OrganizationSerializer(
        many=True, read_only=True, fields=('id', 'name'))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'organizations', 'last_login', 'is_active')