# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Repo.repo_regex'
        db.add_column('hack_repo', 'repo_regex', self.gf('django.db.models.fields.CharField')(default='', max_length='100', blank=True), keep_default=False)

        # Adding field 'Repo.handler'
        db.add_column('hack_repo', 'handler', self.gf('django.db.models.fields.CharField')(default='', max_length='200'), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Repo.repo_regex'
        db.delete_column('hack_repo', 'repo_regex')

        # Deleting field 'Repo.handler'
        db.delete_column('hack_repo', 'handler')


    models = {
        'hack.category': {
            'Meta': {'ordering': "['title']", 'object_name': 'Category'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': "'50'"}),
            'title_plural': ('django.db.models.fields.CharField', [], {'max_length': "'50'", 'blank': 'True'})
        },
        'hack.commit': {
            'Meta': {'ordering': "['-commit_date']", 'object_name': 'Commit'},
            'commit_date': ('django.db.models.fields.DateTimeField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hack': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hack.Hack']"})
        },
        'hack.hack': {
            'Meta': {'ordering': "['title']", 'object_name': 'Hack'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hack.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'participants': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'related_hacks': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_hacks_rel_+'", 'blank': 'True', 'to': "orm['hack.Hack']"}),
            'repo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hack.Repo']", 'null': 'True'}),
            'repo_commits': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'repo_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'repo_forks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'repo_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'repo_watchers': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': "'100'"})
        },
        'hack.hackexample': {
            'Meta': {'ordering': "['title']", 'object_name': 'HackExample'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hack': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hack.Hack']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': "'100'"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'hack.repo': {
            'Meta': {'ordering': "['-is_supported', 'title']", 'object_name': 'Repo'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'handler': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': "'200'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_other': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_supported': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'repo_regex': ('django.db.models.fields.CharField', [], {'max_length': "'100'", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': "'50'"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user_regex': ('django.db.models.fields.CharField', [], {'max_length': "'100'", 'blank': 'True'})
        }
    }

    complete_apps = ['hack']
