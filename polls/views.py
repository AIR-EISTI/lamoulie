from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout

from .models import Question, Answer
from .forms import LamouliesForm, AnswerForm
from .utils import getResults, isUserAuthenticatedAndEistiStudent


def home(request):
    is_auth_eisti, error = isUserAuthenticatedAndEistiStudent(request)
    if not is_auth_eisti:
        return render(request, 'index.html', {'error': error})

    initial = {
        'question_%d' % answer.question.pk: answer.choice
        for answer in request.user.answer_set.all()
        }

    form = LamouliesForm(initial=initial)
    return render(request, 'index.html', {'form': form})


@csrf_exempt
def postAnswer(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    is_auth_eisti, error = isUserAuthenticatedAndEistiStudent(request)
    if not is_auth_eisti:
        return HttpResponseForbidden()
    form = AnswerForm(request.POST)

    if form.is_valid():
        question = form.cleaned_data['question']
        answer = Answer.objects.filter(
            question=question,
            user=request.user)
        if not answer:
            answer = Answer(question=question, user=request.user)
        else:
            answer = answer.first()

        answer.choice = form.cleaned_data['choice']

        answer.save()
        return HttpResponse(status=204)
    return JsonResponse(dict(form.errors.items()), status=400)


@csrf_exempt
def delAnswer(request, pk=None):
    if request.method != 'DELETE':
        return HttpResponse(status=405)

    is_auth_eisti, error = isUserAuthenticatedAndEistiStudent(request)
    if not is_auth_eisti:
        return HttpResponseForbidden()

    try:
        answer = request.user.answer_set.get(question__pk=pk)
        answer.delete()
        return HttpResponse(status=204)
    except Answer.DoesNotExist:
        return HttpResponse(status=404)


def stats(request):
    if not request.user.is_staff:
        return HttpResponseForbidden

    questions = {question: getResults(question) for question in Question.objects.all()}
    return render(request, 'stats.html', {'questions': questions})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
