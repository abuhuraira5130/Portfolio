from rest_framework import serializers
from .models import Project, Technology, Skill, Testimonial, NewsletterSubscription, ContactMessage

class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ['id', 'name']

class ProjectSerializer(serializers.ModelSerializer):
    technologies = serializers.SerializerMethodField(read_only=True)
    technology_ids = serializers.PrimaryKeyRelatedField(queryset=Technology.objects.all(), many=True, write_only=True, required=False)
    class Meta:
        model = Project
        fields = ['id', 'title', 'slug', 'description', 'link', 'github', 'image', 'featured', 'created_at', 'technologies', 'technology_ids']
    def get_technologies(self, obj):
        return [t.name for t in obj.technologies.all()]
    def create(self, validated_data):
        tech_ids = validated_data.pop('technology_ids', [])
        project = Project.objects.create(**validated_data)
        if tech_ids:
            project.technologies.set(tech_ids)
        return project
    def update(self, instance, validated_data):
        tech_ids = validated_data.pop('technology_ids', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        if tech_ids is not None:
            instance.technologies.set(tech_ids)
        return instance

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'category', 'name']

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'name', 'role', 'company', 'content', 'rating', 'created_at']

class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscription
        fields = ['id', 'email', 'confirmed', 'created_at']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'message', 'created_at', 'handled']