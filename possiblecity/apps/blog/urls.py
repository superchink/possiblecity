# blog/urls.py

from django.conf.urls.defaults import include, patterns, url
from django.views.generic import YearArchiveView, MonthArchiveView,\
    WeekArchiveView, DayArchiveView, TodayArchiveView,\
    DetailView, ListView

from possiblecity.blog.models import Entry
from possiblecity.blog.views import EntryDetailView

urlpatterns = patterns('',
    url(r'^$',
        ArchiveIndexView.as_view(
            queryset=Entry.objects.live(),
            date_field="published"),
        name = 'blog_entry_index'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        EntryDetailView.as_view(),
        name = 'blog_entry_detail'),

    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/$',
        DayArchiveView.as_view(
            queryset=Entry.objects.live(),
            date_field="published"),
        name='blog_archive_day'
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
        MonthArchiveView.as_view(
            queryset=Entry.objects.live(),
            date_field="published"),
        name='blog_archive_month'
    ),
    url(r'^(?P<year>\d{4})/$',
        YearArchiveView.as_view(
            queryset=Entry.objects.live(),
            date_field="published"),
        name='blog_archive_year'
    ),
)
