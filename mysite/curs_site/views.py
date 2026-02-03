from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets,generics,permissions,status
from .models import (User,Course,Lesson,Assignment,Question,Answer,Exam,ExamQuestion,
                     Variants,ExamAnswer,Certificate,Review,Cart,CartItem,Favorite)
from .serializers import (UserSerializers,CourseListSerializers,UserProfileSerializer,LoginSerializer,CourseDetailSerializers,LessonSerializers,
                          AssignmentSerializers,QuestionSerializers,AnswerSerializers,
                          ExamSerializers,ExamQuestionSerializers,VariantsSerializers,
                          ExamAnswerSerializers,CertificateSerializers,ReviewSerializers,CartDetailSerializer,
                          CartItemDetailSerializer,CartItemListSerializer,FavoriteListSerializer,FavoriteDetailSerializer)
from .pagination import CoursePagination
from .filters import CourseFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .perimission import CheckCourseStatus,CheckTeacher
from .services import calculate_exam_score
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def finish_exam(request, exam_id):
    exam = Exam.objects.get(id=exam_id)
    student = request.user

    score = calculate_exam_score(student, exam)

    total_questions = exam.exam_questions.count()

    return Response({
        "score": score,
        "total": total_questions,
        "result": "PASS" if score >= total_questions * 0.6 else "FAIL"
    })

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers

class CourseListViewSet(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializers
    pagination_class = CoursePagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['course_name', 'category', 'level']
    ordering_fields = ['price', 'create_at']
    filterset_class = CourseFilter
    permission_classes = [IsAuthenticatedOrReadOnly, CheckCourseStatus, CheckTeacher]



class CourseDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializers
    pagination_class = CoursePagination
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    search_fields = ['course_name','category','level']
    ordering_fields = ['price','create_at']
    filterset_class = CourseFilter
    permission_classes = [IsAuthenticatedOrReadOnly,CheckCourseStatus,CheckTeacher]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializers

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializers

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializers

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializers

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializers

class ExamQuestionViewSet(viewsets.ModelViewSet):
    queryset = ExamQuestion.objects.all()
    serializer_class = ExamQuestionSerializers

class VariantsViewSet(viewsets.ModelViewSet):
    queryset = Variants.objects.all()
    serializer_class = VariantsSerializers

class ExamAnswerViewSet(viewsets.ModelViewSet):
    queryset = ExamAnswer.objects.all()
    serializer_class = ExamAnswerSerializers

class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializers



class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    filter_backends = [SearchFilter]
    search_filters = ['rating']


class CartViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class CartItemListViewSet(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemListSerializer
    permission_classes = [permissions.IsAuthenticated]

class CartItemDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

class FavoriteListViewSet(generics.ListCreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteListSerializer
    permission_classes = [permissions.AllowAny,CheckCourseStatus,CheckTeacher]

class FavoriteDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

