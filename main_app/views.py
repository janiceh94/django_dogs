from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView

# Create your views here.

class Home(TemplateView):
    template_name = 'home.html'

class About(TemplateView): 
    template_name = 'about.html'

#fakebase
class Dog:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
#fakebase
dogs = [
    Dog("Odie", 36, "Male"),
    Dog("Blue", 26, "Female"),
    Dog("Spike", 31, "Male"),
    Dog("Snoopy", 72, "Male"),
    Dog("Pluto", 92, "Male"),
    Dog("Scoopy-Doo", 53, "Male"),
    Dog("Courage", 26, "Male")
]

class Dog_List(TemplateView):
    template_name = 'dog_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dogs"] = dogs
        return context


