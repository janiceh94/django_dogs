from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from .models import Dog

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
        else:
            context["dogs"] = Dog.objects.all()
        return context


