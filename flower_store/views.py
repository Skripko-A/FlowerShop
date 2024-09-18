from django.shortcuts import render

# Create your views here.
def show_index(request):

    return render(
        request,
        'index.html',
        context={},
    )

def show_quiz(request):

    return render(
        request,
        'quiz.html',
        context={},
    )
