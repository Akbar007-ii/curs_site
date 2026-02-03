from django.contrib import admin
from .models import (User,Course,Lesson,Assignment,Question,Answer,Exam,ExamQuestion,
                     Variants,ExamAnswer,Certificate,Review)



from modeltranslation.admin import TranslationAdmin

@admin.register(Course,Assignment,Lesson)
class AllAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

admin.site.register(User)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Exam)
admin.site.register(ExamQuestion)
admin.site.register(Variants)
admin.site.register(ExamAnswer)
admin.site.register(Certificate)
admin.site.register(Review)



