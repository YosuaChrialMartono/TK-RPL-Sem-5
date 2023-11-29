from django.shortcuts import render
from django.http import HttpResponse
from .decorators import mentor_required
from django.db import DatabaseError
from .forms import KelasForm
# Create your views here.

@mentor_required(login_url='authuser:login')
def index(request):
    return HttpResponse("Hello, world. You're at the mentor index.")

def create_kelas(request):
    if request.method == 'POST':
        form = KelasForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                # Redirect after successful save
            except DatabaseError:
                form.add_error(None, 'Failed to save data to the database.')
    else:
        form = KelasForm()

    return render(request, 'your_template.html', {'form': form})