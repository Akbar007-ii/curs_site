from .models import Course,Lesson,Assignment
from modeltranslation.translator import TranslationOptions,register

@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('course_name',)

@register(Lesson)
class LessonTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Assignment)
class AssignmentTranslationOptions(TranslationOptions):
    fields = ('assignment_name',)