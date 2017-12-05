from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from exams.models import Choice, Question, Exam, ExamQuestion
from json import loads
from subjects.models import Subject


class UserExamsView(generic.list.ListView):
    template_name = 'exam_list.html'
    model = Exam
    context_object_name = 'exams'
    paginate_by = 6

    def get_queryset(self):
        return Exam.objects.filter(user=self.request.user)


class ExamDeleteView(generic.edit.DeleteView):
    template_name = 'exam_confirm_delete.html'
    model = Exam
    context_object_name = 'exam'
    success_url = reverse_lazy('exams:exam-list')
    pk_url_kwarg = 'id'


class ExamFormView(generic.TemplateView):
    template_name = 'create_exam.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ExamFormView, self).get_context_data(*args, **kwargs)
        context['subjects'] = Subject.objects.filter(active=True)
        context['count'] = Question.objects.filter(active=True).count()
        return context


class ExamDetailView(generic.detail.DetailView):
    """
    Gets exam by id
    Raises permission denied if exam doesnt belong to user
    Returns 404 if exam doesnt exists
    """
    template_name = 'exam_detail.html'
    model = Exam
    context_object_name = 'exam'
    pk_url_kwarg = 'id'

    def dispatch(self, request, *args, **kwargs):
        if request.user == self.get_object().user:
            return super(ExamDetailView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


@login_required
def start_exam(request):
    """
    Creates new exam based on subjects and length parameters
    """
    length = int(request.GET.get('length'))
    subjects = request.GET.getlist('subjects')
    exam = Exam.create(request.user, subjects, length)
    return redirect('exams:exam-detail', id=exam.id)


@login_required
def answer(request):
    """
    Gets users choice and respective exam
    Create the Answer and mark the question as answered
    """
    data = loads(request.body.decode('utf-8'))
    choice = Choice.objects.get(id=data.get('choice'))
    exam = Exam.objects.get(id=data.get('exam'))

    if not request.user == exam.user:
        raise PermissionDenied

    exam_question = ExamQuestion.objects.get(exam=exam, question=choice.question)
    correct = exam_question.answer(choice)

    return JsonResponse({
        'correct': correct,
        'hint': exam_question.question.hint
    })
