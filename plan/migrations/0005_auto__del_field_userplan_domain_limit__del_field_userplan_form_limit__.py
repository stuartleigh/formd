# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'UserPlan.domain_limit'
        db.delete_column(u'plan_userplan', 'domain_limit')

        # Deleting field 'UserPlan.form_limit'
        db.delete_column(u'plan_userplan', 'form_limit')

        # Deleting field 'Plan.domain_limit'
        db.delete_column(u'plan_plan', 'domain_limit')

        # Deleting field 'Plan.form_limit'
        db.delete_column(u'plan_plan', 'form_limit')


    def backwards(self, orm):
        # Adding field 'UserPlan.domain_limit'
        db.add_column(u'plan_userplan', 'domain_limit',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'UserPlan.form_limit'
        db.add_column(u'plan_userplan', 'form_limit',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Plan.domain_limit'
        db.add_column(u'plan_plan', 'domain_limit',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Plan.form_limit'
        db.add_column(u'plan_plan', 'form_limit',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'message_limit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Default Plan'", 'max_length': '50'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '6', 'decimal_places': '2'}),
            'selectable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'plan.userplan': {
            'Meta': {'object_name': 'UserPlan'},
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