from django.shortcuts import render
from .models import Student
from .forms import StudentForm
from django.http import HttpResponseRedirect

def index(request):
    students = Student.get_all()
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reversed("index"))
    else:
        form = StudentForm()

    context ={
        'students':students,
        'form':form,
    }
    return render(request,"index.html",context=context)