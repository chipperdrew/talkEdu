# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'post'
        db.create_table(u'posts_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 9, 11, 0, 0), auto_now_add=True, db_index=True, blank=True)),
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 9, 11, 0, 0), auto_now=True, blank=True)),
            ('up_votes', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('total_votes', self.gf('django.db.models.fields.SmallIntegerField')(default=0, db_index=True)),
            ('vote_percentage', self.gf('django.db.models.fields.FloatField')(default=0, db_index=True)),
            ('votes_by_user_type', self.gf('picklefield.fields.PickledObjectField')(default={'STU': [0, 0, 0], 'PAR': [0, 0, 0], 'ADM': [0, 0, 0], 'OUT': [0, 0, 0], 'TEA': [0, 0, 0]})),
            ('spam_count', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('user_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='posts', to=orm['accounts.eduuser'])),
            ('page_type', self.gf('django.db.models.fields.CharField')(max_length=3, db_index=True)),
        ))
        db.send_create_signal(u'posts', ['post'])


    def backwards(self, orm):
        # Deleting model 'post'
        db.delete_table(u'posts_post')


    models = {
        u'accounts.eduuser': {
            'Meta': {'object_name': 'eduuser'},
            'akismet_hits': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'total_votes': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'up_votes': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'user_type': ('django.db.models.fields.CharField', [], {'default': "'STU'", 'max_length': '3'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'vote_percentage': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'posts.post': {
            'Meta': {'ordering': "['-time_created']", 'object_name': 'post'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_type': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True'}),
            'spam_count': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 9, 11, 0, 0)', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 9, 11, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'total_votes': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'up_votes': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': u"orm['accounts.eduuser']"}),
            'vote_percentage': ('django.db.models.fields.FloatField', [], {'default': '0', 'db_index': 'True'}),
            'votes_by_user_type': ('picklefield.fields.PickledObjectField', [], {'default': "{'STU': [0, 0, 0], 'PAR': [0, 0, 0], 'ADM': [0, 0, 0], 'OUT': [0, 0, 0], 'TEA': [0, 0, 0]}"})
        }
    }

    complete_apps = ['posts']