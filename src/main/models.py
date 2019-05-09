from django.db import models


class PastRecruiters(models.Model):
    company_order_no = models.PositiveIntegerField(default=64)
    company_name = models.CharField(default="test", max_length=50)
    company_logo = models.ImageField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.company_name
