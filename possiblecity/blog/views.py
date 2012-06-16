# blog/views.py

from django.conf import settings
from django.db.models import F
from django.views.generic import DateDetailView, ArchiveIndexView

from blog.models import Entry

class EntryDetailView(DateDetailView):
    queryset = Entry.objects.live()
    context_object_name = "entry"
    date_field="published"

    def get_object(self):
        # Call the superclass
        object = super(EntryDetailView, self).get_object()
        # Record this visit
        if not self.request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
            object.visits = F('visits') + 1
            object.save()
            # Return the object
        return object