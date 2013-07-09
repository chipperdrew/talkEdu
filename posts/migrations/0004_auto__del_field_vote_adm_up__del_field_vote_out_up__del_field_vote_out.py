# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'vote.adm_up'
        db.delete_column(u'posts_vote', 'adm_up')

        # Deleting field 'vote.out_up'
        db.delete_column(u'posts_vote', 'out_up')

        # Deleting field 'vote.out_votes'
        db.delete_column(u'posts_vote', 'out_votes')

        # Deleting field 'vote.tea_up'
        db.delete_column(u'posts_vote', 'tea_up')

        # Deleting field 'vote.tea_votes'
        db.delete_column(u'posts_vote', 'tea_votes')

        # Deleting field 'vote.par_votes'
        db.delete_column(u'posts_vote', 'par_votes')

        # Deleting field 'vote.adm_votes'
        db.delete_column(u'posts_vote', 'adm_votes')

        # Deleting field 'vote.par_up'
        db.delete_column(u'posts_vote', 'par_up')

        # Deleting field 'vote.stu_votes'
        db.delete_column(u'posts_vote', 'stu_votes')

        # Deleting field 'vote.stu_up'
        db.delete_column(u'posts_vote', 'stu_up')

        # Adding field 'vote.up_votes'
        db.add_column(u'posts_vote', 'up_votes',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'vote.adm_up'
        db.add_column(u'posts_vote', 'adm_up',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'vote.out_up'
        db.add_column(u'posts_vote', 'out_up',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'vote.out_votes'
        db.add_column(u'posts_vote', 'out_votes',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'vote.tea_up'
        db.add_column(u'posts_vote', 'tea_up',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'vote.tea_votes'
        db.add_column(u'posts_vote', 'tea_votes',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'vote.par_votes'
        db.add_column(u'posts_vote', 'par_votes',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'vote.adm_votes'
        db.add_column(u'posts_vote', 'adm_votes',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'vote.par_up'
        db.add_column(u'posts_vote', 'par_up',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'vote.stu_votes'
        db.add_column(u'posts_vote', 'stu_votes',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'vote.stu_up'
        db.add_column(u'posts_vote', 'stu_up',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'vote.up_votes'
        db.delete_column(u'posts_vote', 'up_votes')


    models = {
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
        u'posts.eduuser': {
            'Meta': {'object_name': 'eduuser'},
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
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'user_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'posts.post': {
            'Meta': {'object_name': 'post'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 9, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 9, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': u"orm['posts.eduuser']"})
        },
        u'posts.vote': {
            'Meta': {'object_name': 'vote'},
            'post_id': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['posts.post']", 'unique': 'True', 'primary_key': 'True'}),
            'up_votes': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['posts']