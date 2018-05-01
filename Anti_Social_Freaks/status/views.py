from django.views.generic import TemplateView
from status.forms import StatusForm
from django.shortcuts import render


class StatusView(TemplateView):
    template_name = 'home/forms.html'

    def get(self, request):
        form = StatusForm()
        return render(request, self.template_name, {'form': form})
