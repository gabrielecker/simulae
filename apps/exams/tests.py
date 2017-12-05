from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory
from django.urls import reverse
from exams.models import Exam, Question, Choice
from exams.views import start_exam, answer, ExamDetailView, ExamDeleteView
from json import dumps
from model_mommy import mommy
from subjects.models import Subject


class MocktestProcess(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = mommy.make(User)
        self.questions = [mommy.make(Question, choices=[mommy.make(Choice)
                          for _ in range(5)], make_m2m=True) for _ in range(10)]
        self.subjects = Subject.objects.all()

    def test_create(self):
        subjects = '&'.join(['subjects=%s' % str(subject.id) for subject in self.subjects])
        query_string = '?{}&length=10'.format(subjects)
        request = self.factory.get('/exams/start/%s' % query_string)
        request.user = self.user
        response = start_exam(request)
        self.assertEqual(response.status_code, 302)

    def test_continue(self):
        self.test_create()
        exam = Exam.objects.first()
        request = self.factory.get(reverse('exams:exam-detail', kwargs={'id': exam.id}))
        request.user = mommy.make(User)
        with self.assertRaises(PermissionDenied):
            ExamDetailView.as_view()(request, id=exam.id)
        request.user = self.user
        response = ExamDetailView.as_view()(request, id=exam.id)
        self.assertEqual(response.status_code, 200)

    def test_answer(self):
        self.test_create()
        exam = Exam.objects.first()
        request = self.factory.post(reverse('exams:answer'), data=dumps({
            'choice': Choice.objects.first().id, 'exam': exam.id
        }), content_type='application/json')
        request.user = mommy.make(User)
        with self.assertRaises(PermissionDenied):
            answer(request)
        request.user = self.user
        response = answer(request)
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        self.test_create()
        exam = Exam.objects.first()
        request = self.factory.get(reverse('exams:delete-exam', kwargs={'id': exam.id}))
        request.user = self.user
        response = ExamDeleteView.as_view()(request, id=exam.id)
        self.assertEqual(response.status_code, 200)
