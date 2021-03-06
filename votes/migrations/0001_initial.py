# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'vote'
        db.create_table(u'votes_vote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='votes', null=True, to=orm['posts.post'])),
            ('comment_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='votes', null=True, to=orm['comments.comment'])),
            ('user_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='votes', to=orm['accounts.eduuser'])),
            ('vote_choice', self.gf('django.db.models.fields.CharField')(default='upvote', max_length=8)),
        ))
        db.send_create_signal(u'votes', ['vote'])

        # Adding model 'spam'
        db.create_table(u'votes_spam', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='spam', null=True, to=orm['posts.post'])),
            ('comment_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='spam', null=True, to=orm['comments.comment'])),
            ('user_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='spam', to=orm['accounts.eduuser'])),
        ))
        db.send_create_signal(u'votes', ['spam'])


    def backwards(self, orm):
        # Deleting model 'vote'
        db.delete_table(u'votes_vote')

        # Deleting model 'spam'
        db.delete_table(u'votes_spam')


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
        u'comments.comment': {
            'Meta': {'ordering': "['path']", 'object_name': 'comment'},
            'children': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'depth': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('comments.dbarray.IntegerArrayField', [], {'db_index': 'True', 'blank': 'True'}),
            'post_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['posts.post']"}),
            'spam_count': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 9, 11, 0, 0)', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 9, 11, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'total_votes': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'up_votes': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['accounts.eduuser']"}),
            'vote_percentage': ('django.db.models.fields.FloatField', [], {'default': '0', 'db_index': 'True'}),
            'votes_by_user_type': ('picklefield.fields.PickledObjectField', [], {'default': "{'STU': [0, 0, 0], 'PAR': [0, 0, 0], 'ADM': [0, 0, 0], 'OUT': [0, 0, 0], 'TEA': [0, 0, 0]}"})
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
        },
        u'votes.spam': {
            'Meta': {'object_name': 'spam'},
            'comment_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'spam'", 'null': 'True', 'to': u"orm['comments.comment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'spam'", 'null': 'True', 'to': u"orm['posts.post']"}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'spam'", 'to': u"orm['accounts.eduuser']"})
        },
        u'votes.vote': {
            'Meta': {'object_name': 'vote'},
            'comment_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'null': 'True', 'to': u"orm['comments.comment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'null': 'True', 'to': u"orm['posts.post']"}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': u"orm['accounts.eduuser']"}),
            'vote_choice': ('django.db.models.fields.CharField', [], {'default': "'upvote'", 'max_length': '8'})
        }
    }

    complete_apps = ['votes']