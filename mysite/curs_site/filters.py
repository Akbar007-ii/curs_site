from .models import Course,Review
from django_filters.rest_framework import FilterSet

class CourseFilter(FilterSet):
    class Meta:
        model = Course
        fields = {
            'category': ['exact'],
            'level': ['exact'],
            'price': ['gt','lt']
        }

class ReviewFilter(FilterSet):
    class Meta:
        model = Review
        fields = {
            'rating': ['exact'],
        }