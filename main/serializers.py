from rest_framework import serializers

from .models import (Problem, Picture, Reply, Comment)


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ('image', )


class ProblemSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    class Meta:
        model = Problem
        fields = ('id', 'title', 'description', 'author')

    def create(self, validated_data):
        request = self.context.get('request')
        pictures_files = request.FILES
        problem = Problem.objects.create(
            author=request.user,
            **validated_data
        )
        for picture in pictures_files.getlist('pictures'):
            Picture.objects.create(
                image=picture,
                problem=problem
            )
        return problem

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        images_data = request.FILES
        instance.pictures.all().delete()
        for image in images_data.getlist('images'):
            Picture.objects.create(
                image=image,
                problem=instance
            )
        return instance


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['pictures'] = PictureSerializer(
            instance.pictures.all(), many=True
        ).data
        action = self.context.get('action')
        print('------------------------------')
        print(instance.replies.all())
        print('------------------------------')
        if action == 'retrieve':
            representation['replies'] = ReplySerializer(
                instance.replies.all(),
                many=True
            ).data
        elif action == 'list':
            representation['replies'] = instance.replies.count()
        return representation


class ReplySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    class Meta:
        model = Reply
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        reply = Reply.objects.create(
            author=request.user,
            **validated_data
        )
        return reply

    def to_representation(self, instance):
        represenatation = super().to_representation(instance)
        action = self.context.get('action')
        if action == 'list':
            represenatation['comments'] = instance.comments.count()
        elif action == 'retrieve':
            represenatation['comments'] = CommentSerializer(
                instance.comments.all(), many=True
            ).data
        return represenatation

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        comment = Comment.objects.create(
            author=request.user,
            **validated_data
        )
        return comment


