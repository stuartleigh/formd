# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    plans = {
        "DEFAULT": {
            "name": "Trial",
            "key": "default",
            "rate": 0,
            "domain_limit": 1,
            "form_limit": 1,
            "message_limit": 25,
            "selectable": False,
        },
        "STANDARD": {
            "name": "Light",
            "key": "light_v01",
            "rate": 14,
            "domain_limit": 999,
            "form_limit": 999,
            "message_limit": 250,
            "selectable": True,
        },
        "MEDIUM": {
            "name": "Standard",
            "key": "standard_v01",
            "rate": 24,
            "domain_limit": 999,
            "form_limit": 999,
            "message_limit": 1000,
            "selectable": True,
        },
        "HIGH": {
            "name": "Heavy",
            "key": "heavy_v01",
            "rate": 49,
            "domain_limit": 999,
            "form_limit": 999,
            "message_limit": 5000,
            "selectable": True,
        },
    }

    def forwards(self, orm):
        for plan in self.plans.values():
            orm['plan.Plan'].objects.create(**plan)


    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'account.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'stripe_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
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
        u'plan.plan': {
            'Meta': {'object_name': 'Plan'},
            'domain_limit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'form_limit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'message_limit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Default Plan'", 'max_length': '50'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '6', 'decimal_places': '2'}),
            'selectable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'plan.userplan': {
            'Meta': {'object_name': 'UserPlan'},
            'domain_limit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'form_limit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'message_limit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Default Plan'", 'max_length': '50'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '6', 'decimal_places': '2'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'plan'", 'unique': 'True', 'to': u"orm['account.User']"})
        }
    }

    complete_apps = ['plan']
    symmetrical = True
