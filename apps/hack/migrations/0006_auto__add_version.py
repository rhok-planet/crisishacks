# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Version'
        db.create_table('hack_version', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('hack', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hack.Hack'])),
            ('number', self.gf('django.db.models.fields.CharField')(max_length='100')),
            ('downloads', self.gf('django.db.models.fields.IntegerField')()),
            ('license', self.gf('django.db.models.fields.CharField')(max_length='100')),
        ))
        db.send_create_signal('hack', ['Version'])


    def backwards(self, orm):
        
        # Deleting model 'Version'
        db.delete_table('hack_version')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
            'title': ('django.db.models.fields.CharField', [], {'max_length': "'100'"}),
            'usage': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'})
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
            'handler': ('django.db.models.fields.CharField', [], {'default': "'hack.handlers.unsupported'", 'max_length': "'200'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_other': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_supported': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'repo_regex': ('django.db.models.fields.CharField', [], {'max_length': "'100'", 'blank': 'True'}),
            'slug_regex': ('django.db.models.fields.CharField', [], {'max_length': "'100'", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': "'50'"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user_regex': ('django.db.models.fields.CharField', [], {'max_length': "'100'", 'blank': 'True'})
        },
        'hack.version': {
            'Meta': {'ordering': "['number']", 'object_name': 'Version'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'downloads': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.CharField', [], {'max_length': "'100'"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': "'100'"}),
            'hack': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hack.Hack']"})
        }
    }

    complete_apps = ['hack']