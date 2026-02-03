from .models import ExamAnswer

def calculate_exam_score(student, exam):
    answers = ExamAnswer.objects.filter(
        student=student,
        variants__exam__exam=exam
    )

    score = 0
    for answer in answers:
        if answer.variants.variants_true:
            score += 1

    return score