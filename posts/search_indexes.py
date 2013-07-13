import datetime
from haystack import indexes
from .models import post


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='user_id')
    time_created = indexes.DateTimeField(model_attr='time_created')

    def get_model(self):
        return post

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(time_created__lte=datetime.datetime.now())