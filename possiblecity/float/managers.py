# float/managers.py

import datetime

from django.db import models
from django.db.models.query import QuerySet

class ProjectQuerySet(QuerySet):
    def live(self):
        return self.get_query_set().filter(status=self.model.STATUS_LIVE,
            published__lte=datetime.datetime.now())