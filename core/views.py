from django.views.generic import View
from django.shortcuts import render


class HomeView(View):
    def get(self, request, *args, **kwargs):
        context={
            
            }
        return render(request, 'Base/base.html', context)
    
class chartsView(View):
    def get(self, request, *args, **kwargs):
        context={
            
            }
        return render(request, 'Base/charts.html', context) 