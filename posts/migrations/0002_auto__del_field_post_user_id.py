# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Post.user_id'
        db.delete_column(u'posts_post', 'user_id_id')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Post.user_id'
        raise RuntimeError("Cannot reverse this migration. 'Post.user_id' and its values cannot be restored.")

    models = {
        u'posts.post': {
            'Meta': {'object_name': 'Post'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'timeCreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'timeModified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['posts']