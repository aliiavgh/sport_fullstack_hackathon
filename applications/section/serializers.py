from django.db.models import Avg
from rest_framework import serializers

from applications.section.models import Category, Section, Image, Poster, ParsingGym


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'


class SectionSerializer(serializers.ModelSerializer):
    trainer = serializers.EmailField(required=False)

    class Meta:
        model = Section
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        section = Section.objects.create(**validated_data)

        files = request.FILES
        list_images = []
        for image in files.getlist('images'):
            list_images.append(Image(section=section, image=image))
        Image.objects.bulk_create(list_images)

        return section

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['likes'] = instance.likes.filter(like=True).count()
        rep['rating'] = instance.ratings.all().aggregate(Avg('rating'))['rating__avg']
        return rep


class PosterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poster
        fields = '__all__'


class ParsingGymSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParsingGym
        fields = '__all__'
