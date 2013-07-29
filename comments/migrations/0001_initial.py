# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'comment'
        db.create_table(u'comments_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 29, 0, 0), auto_now_add=True, blank=True)),
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 29, 0, 0), auto_now=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('path', self.gf('comments.dbarray.IntegerArrayField')(blank=True)),
            ('depth', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'comments', ['comment'])


    def backwards(self, orm):
        # Deleting model 'comment'
        db.delete_table(u'comments_comment')


    models = {
        u'comments.comment': {
            'Meta': {'object_name': 'comment'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'depth': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('comments.dbarray.IntegerArrayField', [], {'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 29, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 29, 0, 0)', 'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['comments']