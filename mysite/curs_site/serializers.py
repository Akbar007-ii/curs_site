from .models import (User,Course,Lesson,Assignment,Question,Answer,Exam,ExamQuestion,
                     Variants,ExamAnswer,Certificate,Review,Cart,CartItem,Favorite)
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name'
                  ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']



class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class CourseListSerializers(serializers.ModelSerializer):
    user = UserSerializers()
    get_avg_rating = serializers.SerializerMethodField
    get_count_rating = serializers.SerializerMethodField

    class Meta:
        model = Course
        fields = ['id','user','course_image','get_avg_rating','get_count_rating','course_name','category','level','price']

    def get_avg_rating(self,obj):
        return obj.get_avg_rating()

    def get_count_rating(self,obj):
        return obj.get_count_rating()

class CourseDetailSerializers(serializers.ModelSerializer):
    user = UserSerializers()
    get_avg_rating = serializers.SerializerMethodField
    get_count_rating = serializers.SerializerMethodField
    class Meta:
        model = Course
        fields = ['id','video','course_name','user','category','level','price','description',
                  'get_avg_rating','get_count_rating','created_at','updated_at']

    def get_avg_rating(self,obj):
        return obj.get_avg_rating()

    def get_count_rating(self,obj):
        return obj.get_count_rating()

class LessonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class AssignmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

class QuestionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class AnswerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class ExamSerializers(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'

class ExamQuestionSerializers(serializers.ModelSerializer):
    class Meta:
        model = ExamQuestion
        fields = '__all__'

class VariantsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Variants
        fields = '__all__'

class ExamAnswerSerializers(serializers.ModelSerializer):
    class Meta:
        model = ExamAnswer
        fields = '__all__'

class CertificateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'

class CartItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['cart','course','added_at']

class CartItemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['cart','course','added_at']


class CartDetailSerializer(serializers.ModelSerializer):
    cart = CartItemListSerializer(read_only=True, many=True)
    class Meta:
        model = Cart
        fields = ['user','created_at','cart']

class FavoriteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id','user']

class FavoriteDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id','user','course','added_at']
