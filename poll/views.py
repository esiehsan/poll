from django.shortcuts import render, get_object_or_404

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Question , Choise, Person, Vote
from django.urls import reverse
from django.views import generic
from django.db import IntegrityError

# Create your views here.

# def index(request):
#     NUMBER_OF_QUESTION = 5
#     latest_question_list = Question.objects.order_by("-pub_date")[:NUMBER_OF_QUESTION]
#     context = {
#         'latest_question_list': latest_question_list,
#         }

#     # template = loader.get_template('poll/index.html')
#     # return HttpResponse(template.render(context,request))
    
#     return render(request, 'poll/index.html', context) #this line instead of tow up lines



class IndexView(generic.ListView):
    """ class based view for home (index) page child of ListView 
    class that provide list of data in a html template """
    
    # determine name of context in template
    context_object_name = 'latest_question_list'

    # determine template name
    template_name = 'poll/index.html'

    def get_queryset(self, NUMBER_OF_QUESTION = 5):
        """ this function provide list of data for context """
        return Question.objects.order_by("-pub_date")[:NUMBER_OF_QUESTION]
    

# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk = question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("question does not exist")
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'poll/detail.html',{'question': question})


class DetailView(generic.DetailView):
    """ class base view for detail page child of DetailView 
    class that provide a question that url key determine in a template"""
    
    # determine model
    model = Question

    # determine template 
    template_name = 'poll/detail.html'


def result(request, question_id):
    """ function base view that display results of votes a question"""

    # calling question data in database and save in question variable
    question = get_object_or_404(Question, pk=question_id)

    # save user data in user variable. if not login user 'anonymoys'. this done for retrieve person data
    user = request.user
    
    #retriev person data and save in p variable
    p = Person()
    if(user.id):
        try:
            p = Person.objects.get(user=user)
        except Person.DoesNotExist:  # if no person for this user
            context = {'question': question, 'error_message': 'با این نام کاربری امکان مشاهده نتایج وجود ندارد'}
            return render(request, 'poll/detail.html', context)  
    else:                            # if user is anonymous
        context = {'question': question, 'error_message': 'برای مشاهده نتایج ابتدا لازم است وارد شوید'}
        return render(request, 'poll/detail.html', context)

    try:   # has this person voted on this question before
        _ = Vote.objects.get(person=p, question=question)
        return render(request, 'poll/results.html', {'question': question}) # show results
        
    except Vote.DoesNotExist: # this person has no vote yet
        context = {'question': question, 'error_message': 'شما هنوز در این نظرسنجی شرکت نکرده اید. بنابراین امکان مشاهده نتایج وجود ندارد'}
        return render(request, 'poll/detail.html', context)

# class ResultView(generic.DetailView):
#     model = Question
#     template_name = 'poll/results.html'


def vote(request, question_id):
    """ function based view for register a vote"""

    question = get_object_or_404(Question, pk=question_id) # retrieve question 
    user = request.user  # return user in request
    p = Person()

    # find person for that user
    if(user.id):
        try:
            p = Person.objects.get(user=user)
        except Person.DoesNotExist:
            context = {'question': question, 'error_message': 'با این نام کاربری امکان ثبت رای وجود ندارد'}
            return render(request, 'poll/detail.html', context)  
            
    try:
        choise_id = request.POST['choise'] # save user choice_id
        selected_choise = question.choise_set.get(pk=choise_id) # retrieve choise
    except (KeyError, Choise.DoesNotExist): # if user do not select a choice
        context = {'question': question, 'error_message': 'لطفا یکی از گزینه ها را انتخاب نمایید'}
        return render(request, 'poll/detail.html', context)
    else:
        selected_choise.votes += 1  # add to the choise votes
        vote = Vote(person=p, question=question, choise=selected_choise) 
        try:
            vote.save()  
        except IntegrityError : # if vote.save error meaning this exist a record with this person and question in vote table
            pre_vote = Vote.objects.get(person=p, question=question)
            context = {
                'question': question,
                'selected_choise': pre_vote.choise,
                'error_message': 'شما یک بار در این نظرسنجی شرکت کرده اید و امکان ثبت نظر مجدد نیست'
                }

            return render(request, 'poll/detail.html', context)
        else:
            selected_choise.save()
        return HttpResponseRedirect(reverse('poll:results', args=(question_id,))) # show results for this question
        