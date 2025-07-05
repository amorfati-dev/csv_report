"""Django models compatible with existing SQLModel structure."""

from django.db import models


class Run(models.Model):
    """Run model compatible with csv_report SQLModel."""

    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    csv_file = models.CharField(max_length=255)
    output_format = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    rows_processed = models.IntegerField()
    error_message = models.TextField(blank=True, default="")
    duration = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "run"
        managed = False  # Django doesn't manage this table

    def __str__(self) -> str:
        """Return string representation of the Run model."""
        return f"Run {self.id} - {self.csv_file} ({self.status})"


class KPI(models.Model):
    """KPI model compatible with csv_report SQLModel."""

    id = models.AutoField(primary_key=True)
    run_id = models.IntegerField()
    name = models.CharField(max_length=100)
    value = models.FloatField()
    unit = models.CharField(max_length=50)
    description = models.TextField()
    calculated_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50)

    class Meta:
        db_table = "kpi"
        managed = False  # Django doesn't manage this table

    def __str__(self) -> str:
        """Return string representation of the KPI model."""
        return f"KPI {self.name}: {self.value} ({self.category})"
