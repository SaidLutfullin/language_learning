from django.views.generic import FormView
from .forms import ContactForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect


class ContactUs(FormView):
    form_class = ContactForm
    template_name = 'feedback/contact_us.html'
    success_url = reverse_lazy('contact_us')

    def form_valid(self, form):
        try:
            form.save()
            messages.success(self.request, 'Сообщение отправлено')
        except Exception:
            messages.error(self.request, 'Сообщение не отправлено')
        return HttpResponseRedirect(self.get_success_url())
