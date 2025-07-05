"""
Django models compatible with existing SQLModel structure.
"""

from django.db import models


class Run(models.Model):
    """Run model compatible with csv_report SQLModel."""
    
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    csv_file = models.CharField(max_length=255)
    output_format = models.CharField(max_length=10)
    status = models.CharField(max_length=20)
    rows_processed = models.IntegerField()
    error_message = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'run'
        managed = False  # Django doesn't manage this table


class KPI(models.Model):
    """KPI model compatible with csv_report SQLModel."""
    
    id = models.AutoField(primary_key=True)
    run_id = models.IntegerField()
    name = models.CharField(max_length=255)
    value = models.FloatField()
    unit = models.CharField(max_length=50)
    description = models.TextField()
    calculated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'kpi'
        managed = False  # Django doesn't manage this table
