# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Post.title'
        db.add_column(u'posts_post', 'title',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=75),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Post.title'
        db.delete_column(u'posts_post', 'title')


    models = {
        u'posts.post': {
            'Meta': {'object_name': 'Post'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'timeCreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'timeModified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '75'})
        }
    }

    complete_apps = ['posts']