from rest_framework import serializers
from likes import services as likes_services
# from likes.serializers import FanSerializer

from .models import (Problem, Picture, Reply, Comment, Favorite, Rating)


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ('image', )


class ProblemSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    class Meta:
        model = Problem
        fields = ('id', 'title', 'description', 'author', 'total_likes', 'if_fan')

    def get_is_fan(self, obj) -> bool:
        request = self.context.get('request')
        if request:
            return likes_services.is_fan(obj, request.user)

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


class FavoriteSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    class Meta:
        model = Favorite
        fields = '__all__'

        def create(self, validated_data):
            request = self.context.get('request')
            favorite = Favorite.objects.create(
                author=request.user,
                **validated_data
            )
            return favorite



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

    # def to_representation(self, instance):
    #     represenatation = super().to_representation(instance)
    #     action = self.context.get('action')
    #     if action == 'list':
    #         represenatation['comments'] = instance.comments.count()
    #     elif action == 'retrieve':
    #         represenatation['comments'] = CommentSerializer(
    #             instance.comments.all(), many=True
    #         ).data
    #     rating_list = []
    #     for review in represenatation['reviews']:
    #         rating_list.append(review['rating'])
    #     try:
    #         represenatation['reply_rating'] = round(sum(rating_list) / len(rating_list), 2)
    #     except ZeroDivisionError:
    #         represenatation['reply_rating'] = None
    #     return represenatation

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


class RatingSerializer(serializers.ModelSerializer):
    post_title = serializers.SerializerMethodField("get_post_title")

    class Meta:
        model = Rating
        # fields = 'all'
        exclude = ('author',)

    def get_post_title(self, rating):
        title = rating.problem.title
        return title

    def validate_rating(self, rating):
        if rating not in range(1, 6):
            raise serializers.ValidationError(
                "Рейтинг должен быть от 1 до 5"
            )
        return rating

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        # print(dir(instance) ,'Hellooooooo')
        if not request.user.is_anonymous:
            representation['author'] = request.user.email

        return representation



