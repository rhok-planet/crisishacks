# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Category'
        db.create_table('hack_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length='50')),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('hack', ['Category'])

        # Adding model 'Repo'
        db.create_table('hack_repo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('is_supported', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length='50')),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('hack', ['Repo'])

        # Adding model 'Hack'
        db.create_table('hack_hack', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length='100')),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hack.Category'])),
            ('repo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hack.Repo'], null=True)),
            ('repo_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('repo_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('repo_watchers', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('repo_forks', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('repo_commits', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('participants', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('hack', ['Hack'])

        # Adding M2M table for field related_hacks on 'Hack'
        db.create_table('hack_hack_related_hacks', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_hack', models.ForeignKey(orm['hack.hack'], null=False)),
            ('to_hack', models.ForeignKey(orm['hack.hack'], null=False))
        ))
        db.create_unique('hack_hack_related_hacks', ['from_hack_id', 'to_hack_id'])

        # Adding model 'HackExample'
        db.create_table('hack_hackexample', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('hack', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hack.Hack'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length='100')),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('hack', ['HackExample'])

        # Adding model 'Commit'
        db.create_table('hack_commit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('hack', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hack.Hack'])),
            ('commit_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('hack', ['Commit'])


    def backwards(self, orm):
        
        # Deleting model 'Category'
        db.delete_table('hack_category')

        # Deleting model 'Repo'
        db.delete_table('hack_repo')

        # Deleting model 'Hack'
        db.delete_table('hack_hack')

        # Removing M2M table for field related_hacks on 'Hack'
        db.delete_table('hack_hack_related_hacks')

        # Deleting model 'HackExample'
        db.delete_table('hack_hackexample')

        # Deleting model 'Commit'
        db.delete_table('hack_commit')


    models = {
        'hack.category': {
            'Meta': {'ordering': "['title']", 'object_name': 'Category'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': "'50'"})
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_supported': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': "'50'"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['hack']
