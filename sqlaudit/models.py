# -*- coding: utf-8 -*-

from django.db import models

from api.apps.user.models import Group, User
from ..common.fields import AESCharField

DB_TYPE_LIST = [(item, item) for item in ['mysql', 'sqlserver']]
APPROVAL_STATUS_LIST = [(item, item) for item in
                        ['approvaling', 'refuse', 'approval', 'cancel', 'success', 'failed']]  # TODO: 干掉
OPERATE_LIST = [(item, item) for item in ['submit', 'cancel', 'refuse', 'aproval', 'success', 'failed']]


class Instance(models.Model):
    name = models.CharField(max_length=128)
    host = models.CharField(max_length=128)
    port = models.CharField(max_length=128)
    db_type = models.CharField(max_length=128, choices=DB_TYPE_LIST)

    user = models.CharField(max_length=128)
    password = AESCharField(max_length=128)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', 'updated_at']


class DB(models.Model):
    name = models.CharField(max_length=128)
    alias_name = models.CharField(max_length=128)
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    project = models.ForeignKey(Group, null=True, default=None, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', 'updated_at']


class Table(models.Model):
    name = models.CharField(max_length=128)
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    db = models.ForeignKey(DB, on_delete=models.CASCADE, related_name='tablss')

    structure = models.TextField()
    index = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', 'updated_at']


class SearchOrder(models.Model):
    db = models.ForeignKey(DB, null=True, on_delete=models.SET_NULL, related_name='search_orders')
    sql = models.TextField()
    top_20_rows = models.TextField()
    row_count = models.IntegerField(null=True, default=None)
    exception = models.TextField()
    execute_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='search_orders')
    success = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', 'updated_at']


class SQLOrder(models.Model):
    db = models.ForeignKey(DB, null=True, on_delete=models.SET_NULL, related_name='sql_orders')
    comment = models.TextField()
    sql = models.TextField()
    created_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='create_sql_orders')
    approval_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='approval_sql_orders')
    status = models.CharField(max_length=128, default='approvaling', choices=APPROVAL_STATUS_LIST)
    approval_at = models.DateTimeField(null=True, default=None)  # TODO: 貌似没用了
    success = models.BooleanField(default=False)  # TODO: 貌似没用了
    result = models.TextField()
    back = models.BooleanField()  # 是否备份
    message_id = models.CharField(max_length=256, null=True, default=None)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', 'updated_at']


class SQLOrderProcess(models.Model):
    sql_order = models.ForeignKey(SQLOrder, on_delete=models.CASCADE, related_name='processes')
    operate = models.CharField(max_length=128, choices=OPERATE_LIST)
    operate_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class SQLCheckResults(models.Model):
    check_id = models.CharField(max_length=256, db_index=True)
    order = models.ForeignKey(SQLOrder, null=True, on_delete=models.SET_NULL, related_name='check_results')
    db = models.ForeignKey(DB, null=True, on_delete=models.SET_NULL)
    index = models.IntegerField()
    origin_sql = models.TextField()
    mode = models.CharField(max_length=32)
    count_sql = models.TextField()
    back_sql = models.TextField()
    back_data = models.TextField()
    affect_rows = models.IntegerField(null=True, default=None)
    warning = models.TextField()
    error = models.TextField()

    check_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
