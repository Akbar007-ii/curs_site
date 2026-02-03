from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator,MinValueValidator
from django.core.exceptions import ValidationError

class User(AbstractUser):
    USER_ROLE = (
    ('Студент','Студент'),
    ('Предподаватель','Предподаватель')
    )
    user_role = models.CharField(max_length=15, choices=USER_ROLE, default='Студент')
    user_image = models.ImageField(upload_to='user_image/')
    bio = models.TextField(blank=True)

class Course(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='course_user')
    course_name = models.CharField(max_length=32)
    course_image = models.ImageField(upload_to='course_image/')
    video = models.FileField(null=True,blank=True)
    description = models.TextField()
    CATEGORY = (
    ('A','A'),
    ('A1','A1'),
    ('B','B'),
    ('B1','B1'),
    ('C','C'),
    ('C1','C1'),
    ('D','D'),
    ('D1','D1'),
    ('BE','BE'),
    ('CE','CE'),
    ('C1E','C1E'),
    ('DE','DE'),
    ('D1E','D1E')
    )
    category = models.CharField(max_length=10, choices=CATEGORY)
    LEVEL =(
    ('Новичок','Новичок'),
    ('Средний','Средний'),
    ('Профиессионал','Профиессионал')
    )
    level = models.CharField(max_length=15,choices=LEVEL,default='Новичок')
    price = models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def get_avg_rating(self):
        reviews = self.review_course.all()
        if reviews.exists():
            return sum([i.comment for i in reviews]) / reviews.count()

        return 0

    def get_count_rating(self):
        reviews =self.review_course.all()
        if reviews.exists():
            return  reviews.count()
        return 0

    def __str__(self):
        return self.course_name

class Lesson(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='lesson_course')
    title = models.CharField(max_length=70)
    video_url = models.FileField(upload_to='videos/')
    content = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Assignment(models.Model):
    courses = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='assignment_courses')
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    assignment_name = models.CharField(max_length=70)

    def __str__(self):
        return self.assignment_name

class Question(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='question_course')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='question_user')
    assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE,related_name='question_assignment')
    question = models.TextField(blank=True)
    files = models.FileField(upload_to='question_file/',null=True,blank=True)

    def __str__(self):
        return self.question

class Answer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='answer_user')
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='answer_question')
    answer = models.TextField()
    file = models.FileField(blank=True)
    answer_at = models.DateTimeField(auto_now_add=True)


class Exam(models.Model):
    course_exam = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='exam_course')
    TYPES_OF_EXAMS = (
    ('Тренировочный','Тренировочный'),
    ('Проверочный','Проверочный'),
    ('Итоговый','Итоговый')
    )
    types_of_exams = models.CharField(max_length=15,choices=TYPES_OF_EXAMS)

    def __str__(self):
        return f'{self.course_exam}:{self.types_of_exams}'

class ExamQuestion(models.Model):
    teacher = models.ForeignKey(User,on_delete=models.CASCADE,related_name='exam_teacher')
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE,related_name='exam_questions')
    title = models.CharField(max_length=100)

class Variants(models.Model):
    teacher = models.ForeignKey(User,on_delete=models.CASCADE,related_name='teacher_variants')
    exam = models.ForeignKey(ExamQuestion,on_delete=models.CASCADE,related_name='variants_exam')
    VARIANTS = (
    ('A','A'),
    ('B','B'),
    ('C','C')
    )
    variants = models.CharField(max_length=5,choices=VARIANTS)
    variants_text = models.TextField()
    variants_true = models.BooleanField(blank=False)


    def clean(self):
        if self.variants_true:
            exists = Variants.objects.filter(
                exam=self.exam,
                variants_true=True
            ).exclude(id=self.id).exists()

            if exists:
                raise ValidationError(
                    'Бул суроодо бир гана туура жооп болушу керек!'
                )

    def __str__(self):
        return f"{self.exam.title} - {self.variants}"

class ExamAnswer(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE,related_name='answer_student')
    question = models.ForeignKey(ExamQuestion,on_delete=models.CASCADE,related_name='answers')
    variants = models.ForeignKey(Variants,on_delete=models.CASCADE,related_name='exam_variants')



class Certificate(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE,related_name='certificate_student')
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='courses_certificate')
    issued_at = models.DateTimeField(auto_now_add=True)



class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='review_user')
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='review_course')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment = models.TextField(null=True,blank=True)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'{self.user}:{self.created_at}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    added_at =models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'{self.cart}:{self.course}'



class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_favorite')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'{self.user}:{self.course}'



