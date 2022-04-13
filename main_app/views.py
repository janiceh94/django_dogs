from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from .models import Dog, DogToy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

# Create your views here.

class Home(TemplateView):
    template_name = 'home.html'

class About(TemplateView): 
    template_name = 'about.html'

class Dog_List(TemplateView):
    template_name = 'dog_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        if name != None:
            context["dogs"] = Dog.objects.filter(name__icontains=name)
            context["header"] = f"Searching for {name}"
        else:
            context["dogs"] = Dog.objects.all()
            context["header"] = "All Our Dogs"
        return context

class Dog_Create(CreateView):
    model = Dog
    fields = ["name", "img", "age", "gender"]
    template_name = "dog_create.html"
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect('/dogs')

class Dog_Detail(DetailView):
    model = Dog
    template_name = "dog_detail.html"

class Dog_Update(UpdateView):
    model = Dog
    fields = ["name", "img", "age", "gender"]
    template_name = 'dog_update.html'
    def get_success_url(self):
        return reverse('dog_detail', kwargs={'pk': self.object.pk})

class Dog_Delete(DeleteView):
    model = Dog
    template_name = 'dog_delete.html'
    success_url = '/dogs/'

def profile(request, username):
    user = User.objects.get(username=username)
    dogs = Dog.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username, 'dogs': dogs})

def dogtoys_index(request):
    dogtoys = DogToy.objects.all()
    return render (request, 'dogtoy_index.html', {'dogtoys': dogtoys})

def dogtoys_show(request, dogtoy_id):
    dogtoy = DogToy.objects.get(id=dogtoy_id)
    return render(request, 'dogtoy_show.html', {'dogtoy': dogtoy})

class DogToyCreate(CreateView):
    model = DogToy
    fields = '__all__'
    template_name = 'dogtoy_form.html'
    success_url='/dogtoys'

class DogToyUpdate(UpdateView):
    model = DogToy
    fields = ['name', 'color']
    template_name = 'dogtoy_update.html'
    success_url='/dogtoys'

class DogToyDelete(DeleteView):
    model = DogToy
    template_name='dogtoy_delete.html'
    success_url='/dogtoys'