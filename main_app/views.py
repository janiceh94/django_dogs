from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Dog, DogToy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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

class Dog_Create(LoginRequiredMixin,CreateView):
    model = Dog
    fields = ["name", "img", "age", "gender", 'dogtoys']
    template_name = "dog_create.html"
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect('/dogs')

class Dog_Detail(DetailView):
    model = Dog
    template_name = "dog_detail.html"

class Dog_Update(LoginRequiredMixin, UpdateView):
    model = Dog
    fields = ["name", "img", "age", "gender", 'dogtoys']
    template_name = 'dog_update.html'
    def get_success_url(self):
        return reverse('dog_detail', kwargs={'pk': self.object.pk})

class Dog_Delete(LoginRequiredMixin, DeleteView):
    model = Dog
    template_name = 'dog_delete.html'
    success_url = '/dogs/'

@login_required
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

class DogToyCreate(LoginRequiredMixin, CreateView):
    model = DogToy
    fields = '__all__'
    template_name = 'dogtoy_form.html'
    success_url='/dogtoys'

class DogToyUpdate(LoginRequiredMixin, UpdateView):
    model = DogToy
    fields = ['name', 'color']
    template_name = 'dogtoy_update.html'
    success_url='/dogtoys'

class DogToyDelete(LoginRequiredMixin, DeleteView):
    model = DogToy
    template_name='dogtoy_delete.html'
    success_url='/dogtoys'

# auth
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if(form.is_valid()):
            user = form.save()
            login(request, user)
            print('Hello', user.username)
            return HttpResponseRedirect('/user/' + str(user.username))
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})