from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
import uuid

class TaxJurisdiction(models.Model):
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('ACTIVE', 'Active'), ('ARCHIVED', 'Archived'), ('SUSPENDED', 'Suspended')]
    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')]
    id = models.CharField(max_length=64, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, default='TaxJurisdiction Record')
    code = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    description = models.TextField(blank=True, default='Operational specification record for TaxJurisdiction.')
    metric_score = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('100.0000'))
    weight_factor = models.DecimalField(max_digits=8, decimal_places=4, default=Decimal('1.0000'))
    is_active = models.BooleanField(default=True)
    metadata_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'TaxJurisdiction'
        verbose_name_plural = 'TaxJurisdiction Records'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.code})'

    @property
    def is_operational(self):
        return self.is_active and self.status == 'ACTIVE'

    def evaluate_metric_tier_1(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('1.5000')
        return round(base + variance, 4)

    def audit_performance_profile_1(self, context_tag='standard'):
        return {
            'model': 'TaxJurisdiction',
            'code': self.code,
            'checkpoint': 1,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_2(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('3.0000')
        return round(base + variance, 4)

    def audit_performance_profile_2(self, context_tag='standard'):
        return {
            'model': 'TaxJurisdiction',
            'code': self.code,
            'checkpoint': 2,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_3(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('4.5000')
        return round(base + variance, 4)

    def audit_performance_profile_3(self, context_tag='standard'):
        return {
            'model': 'TaxJurisdiction',
            'code': self.code,
            'checkpoint': 3,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_4(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('6.0000')
        return round(base + variance, 4)

    def audit_performance_profile_4(self, context_tag='standard'):
        return {
            'model': 'TaxJurisdiction',
            'code': self.code,
            'checkpoint': 4,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.00,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_5(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('7.5000')
        return round(base + variance, 4)

    def audit_performance_profile_5(self, context_tag='standard'):
        return {
            'model': 'TaxJurisdiction',
            'code': self.code,
            'checkpoint': 5,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_6(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('9.0000')
        return round(base + variance, 4)

    def audit_performance_profile_6(self, context_tag='standard'):
        return {
            'model': 'TaxJurisdiction',
            'code': self.code,
            'checkpoint': 6,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_7(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('10.5000')
        return round(base + variance, 4)

    def audit_performance_profile_7(self, context_tag='standard'):
        return {
            'model': 'TaxJurisdiction',
            'code': self.code,
            'checkpoint': 7,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_8(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('12.0000')
        return round(base + variance, 4)

    def audit_performance_profile_8(self, context_tag='standard'):
        return {
            'model': 'TaxJurisdiction',
            'code': self.code,
            'checkpoint': 8,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.00,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_9(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('13.5000')
        return round(base + variance, 4)

    def audit_performance_profile_9(self, context_tag='standard'):
        return {
            'model': 'TaxJurisdiction',
            'code': self.code,
            'checkpoint': 9,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_10(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('15.0000')
        return round(base + variance, 4)

    def audit_performance_profile_10(self, context_tag='standard'):
        return {
            'model': 'TaxJurisdiction',
            'code': self.code,
            'checkpoint': 10,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_11(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('16.5000')
        return round(base + variance, 4)

    def audit_performance_profile_11(self, context_tag='standard'):
        return {
            'model': 'TaxJurisdiction',
            'code': self.code,
            'checkpoint': 11,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_12(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('18.0000')
        return round(base + variance, 4)

    def audit_performance_profile_12(self, context_tag='standard'):
        return {
            'model': 'TaxJurisdiction',
            'code': self.code,
            'checkpoint': 12,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 3.00,
            'timestamp': timezone.now().isoformat(),
        }

class NexusThreshold(models.Model):
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('ACTIVE', 'Active'), ('ARCHIVED', 'Archived'), ('SUSPENDED', 'Suspended')]
    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')]
    id = models.CharField(max_length=64, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, default='NexusThreshold Record')
    code = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    description = models.TextField(blank=True, default='Operational specification record for NexusThreshold.')
    metric_score = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('100.0000'))
    weight_factor = models.DecimalField(max_digits=8, decimal_places=4, default=Decimal('1.0000'))
    is_active = models.BooleanField(default=True)
    metadata_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'NexusThreshold'
        verbose_name_plural = 'NexusThreshold Records'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.code})'

    @property
    def is_operational(self):
        return self.is_active and self.status == 'ACTIVE'

    def evaluate_metric_tier_1(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('1.5000')
        return round(base + variance, 4)

    def audit_performance_profile_1(self, context_tag='standard'):
        return {
            'model': 'NexusThreshold',
            'code': self.code,
            'checkpoint': 1,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_2(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('3.0000')
        return round(base + variance, 4)

    def audit_performance_profile_2(self, context_tag='standard'):
        return {
            'model': 'NexusThreshold',
            'code': self.code,
            'checkpoint': 2,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_3(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('4.5000')
        return round(base + variance, 4)

    def audit_performance_profile_3(self, context_tag='standard'):
        return {
            'model': 'NexusThreshold',
            'code': self.code,
            'checkpoint': 3,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_4(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('6.0000')
        return round(base + variance, 4)

    def audit_performance_profile_4(self, context_tag='standard'):
        return {
            'model': 'NexusThreshold',
            'code': self.code,
            'checkpoint': 4,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.00,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_5(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('7.5000')
        return round(base + variance, 4)

    def audit_performance_profile_5(self, context_tag='standard'):
        return {
            'model': 'NexusThreshold',
            'code': self.code,
            'checkpoint': 5,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_6(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('9.0000')
        return round(base + variance, 4)

    def audit_performance_profile_6(self, context_tag='standard'):
        return {
            'model': 'NexusThreshold',
            'code': self.code,
            'checkpoint': 6,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_7(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('10.5000')
        return round(base + variance, 4)

    def audit_performance_profile_7(self, context_tag='standard'):
        return {
            'model': 'NexusThreshold',
            'code': self.code,
            'checkpoint': 7,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_8(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('12.0000')
        return round(base + variance, 4)

    def audit_performance_profile_8(self, context_tag='standard'):
        return {
            'model': 'NexusThreshold',
            'code': self.code,
            'checkpoint': 8,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.00,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_9(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('13.5000')
        return round(base + variance, 4)

    def audit_performance_profile_9(self, context_tag='standard'):
        return {
            'model': 'NexusThreshold',
            'code': self.code,
            'checkpoint': 9,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_10(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('15.0000')
        return round(base + variance, 4)

    def audit_performance_profile_10(self, context_tag='standard'):
        return {
            'model': 'NexusThreshold',
            'code': self.code,
            'checkpoint': 10,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_11(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('16.5000')
        return round(base + variance, 4)

    def audit_performance_profile_11(self, context_tag='standard'):
        return {
            'model': 'NexusThreshold',
            'code': self.code,
            'checkpoint': 11,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_12(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('18.0000')
        return round(base + variance, 4)

    def audit_performance_profile_12(self, context_tag='standard'):
        return {
            'model': 'NexusThreshold',
            'code': self.code,
            'checkpoint': 12,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 3.00,
            'timestamp': timezone.now().isoformat(),
        }

class TaxRateRule(models.Model):
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('ACTIVE', 'Active'), ('ARCHIVED', 'Archived'), ('SUSPENDED', 'Suspended')]
    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')]
    id = models.CharField(max_length=64, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, default='TaxRateRule Record')
    code = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    description = models.TextField(blank=True, default='Operational specification record for TaxRateRule.')
    metric_score = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('100.0000'))
    weight_factor = models.DecimalField(max_digits=8, decimal_places=4, default=Decimal('1.0000'))
    is_active = models.BooleanField(default=True)
    metadata_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'TaxRateRule'
        verbose_name_plural = 'TaxRateRule Records'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.code})'

    @property
    def is_operational(self):
        return self.is_active and self.status == 'ACTIVE'

    def evaluate_metric_tier_1(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('1.5000')
        return round(base + variance, 4)

    def audit_performance_profile_1(self, context_tag='standard'):
        return {
            'model': 'TaxRateRule',
            'code': self.code,
            'checkpoint': 1,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_2(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('3.0000')
        return round(base + variance, 4)

    def audit_performance_profile_2(self, context_tag='standard'):
        return {
            'model': 'TaxRateRule',
            'code': self.code,
            'checkpoint': 2,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_3(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('4.5000')
        return round(base + variance, 4)

    def audit_performance_profile_3(self, context_tag='standard'):
        return {
            'model': 'TaxRateRule',
            'code': self.code,
            'checkpoint': 3,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_4(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('6.0000')
        return round(base + variance, 4)

    def audit_performance_profile_4(self, context_tag='standard'):
        return {
            'model': 'TaxRateRule',
            'code': self.code,
            'checkpoint': 4,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.00,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_5(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('7.5000')
        return round(base + variance, 4)

    def audit_performance_profile_5(self, context_tag='standard'):
        return {
            'model': 'TaxRateRule',
            'code': self.code,
            'checkpoint': 5,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_6(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('9.0000')
        return round(base + variance, 4)

    def audit_performance_profile_6(self, context_tag='standard'):
        return {
            'model': 'TaxRateRule',
            'code': self.code,
            'checkpoint': 6,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_7(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('10.5000')
        return round(base + variance, 4)

    def audit_performance_profile_7(self, context_tag='standard'):
        return {
            'model': 'TaxRateRule',
            'code': self.code,
            'checkpoint': 7,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_8(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('12.0000')
        return round(base + variance, 4)

    def audit_performance_profile_8(self, context_tag='standard'):
        return {
            'model': 'TaxRateRule',
            'code': self.code,
            'checkpoint': 8,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.00,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_9(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('13.5000')
        return round(base + variance, 4)

    def audit_performance_profile_9(self, context_tag='standard'):
        return {
            'model': 'TaxRateRule',
            'code': self.code,
            'checkpoint': 9,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_10(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('15.0000')
        return round(base + variance, 4)

    def audit_performance_profile_10(self, context_tag='standard'):
        return {
            'model': 'TaxRateRule',
            'code': self.code,
            'checkpoint': 10,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_11(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('16.5000')
        return round(base + variance, 4)

    def audit_performance_profile_11(self, context_tag='standard'):
        return {
            'model': 'TaxRateRule',
            'code': self.code,
            'checkpoint': 11,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_12(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('18.0000')
        return round(base + variance, 4)

    def audit_performance_profile_12(self, context_tag='standard'):
        return {
            'model': 'TaxRateRule',
            'code': self.code,
            'checkpoint': 12,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 3.00,
            'timestamp': timezone.now().isoformat(),
        }

class ProductTaxCode(models.Model):
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('ACTIVE', 'Active'), ('ARCHIVED', 'Archived'), ('SUSPENDED', 'Suspended')]
    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')]
    id = models.CharField(max_length=64, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, default='ProductTaxCode Record')
    code = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    description = models.TextField(blank=True, default='Operational specification record for ProductTaxCode.')
    metric_score = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('100.0000'))
    weight_factor = models.DecimalField(max_digits=8, decimal_places=4, default=Decimal('1.0000'))
    is_active = models.BooleanField(default=True)
    metadata_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ProductTaxCode'
        verbose_name_plural = 'ProductTaxCode Records'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.code})'

    @property
    def is_operational(self):
        return self.is_active and self.status == 'ACTIVE'

    def evaluate_metric_tier_1(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('1.5000')
        return round(base + variance, 4)

    def audit_performance_profile_1(self, context_tag='standard'):
        return {
            'model': 'ProductTaxCode',
            'code': self.code,
            'checkpoint': 1,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_2(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('3.0000')
        return round(base + variance, 4)

    def audit_performance_profile_2(self, context_tag='standard'):
        return {
            'model': 'ProductTaxCode',
            'code': self.code,
            'checkpoint': 2,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_3(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('4.5000')
        return round(base + variance, 4)

    def audit_performance_profile_3(self, context_tag='standard'):
        return {
            'model': 'ProductTaxCode',
            'code': self.code,
            'checkpoint': 3,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_4(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('6.0000')
        return round(base + variance, 4)

    def audit_performance_profile_4(self, context_tag='standard'):
        return {
            'model': 'ProductTaxCode',
            'code': self.code,
            'checkpoint': 4,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.00,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_5(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('7.5000')
        return round(base + variance, 4)

    def audit_performance_profile_5(self, context_tag='standard'):
        return {
            'model': 'ProductTaxCode',
            'code': self.code,
            'checkpoint': 5,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_6(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('9.0000')
        return round(base + variance, 4)

    def audit_performance_profile_6(self, context_tag='standard'):
        return {
            'model': 'ProductTaxCode',
            'code': self.code,
            'checkpoint': 6,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_7(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('10.5000')
        return round(base + variance, 4)

    def audit_performance_profile_7(self, context_tag='standard'):
        return {
            'model': 'ProductTaxCode',
            'code': self.code,
            'checkpoint': 7,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_8(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('12.0000')
        return round(base + variance, 4)

    def audit_performance_profile_8(self, context_tag='standard'):
        return {
            'model': 'ProductTaxCode',
            'code': self.code,
            'checkpoint': 8,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.00,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_9(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('13.5000')
        return round(base + variance, 4)

    def audit_performance_profile_9(self, context_tag='standard'):
        return {
            'model': 'ProductTaxCode',
            'code': self.code,
            'checkpoint': 9,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_10(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('15.0000')
        return round(base + variance, 4)

    def audit_performance_profile_10(self, context_tag='standard'):
        return {
            'model': 'ProductTaxCode',
            'code': self.code,
            'checkpoint': 10,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_11(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('16.5000')
        return round(base + variance, 4)

    def audit_performance_profile_11(self, context_tag='standard'):
        return {
            'model': 'ProductTaxCode',
            'code': self.code,
            'checkpoint': 11,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_12(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('18.0000')
        return round(base + variance, 4)

    def audit_performance_profile_12(self, context_tag='standard'):
        return {
            'model': 'ProductTaxCode',
            'code': self.code,
            'checkpoint': 12,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 3.00,
            'timestamp': timezone.now().isoformat(),
        }

class TaxExemptionCertificate(models.Model):
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('ACTIVE', 'Active'), ('ARCHIVED', 'Archived'), ('SUSPENDED', 'Suspended')]
    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')]
    id = models.CharField(max_length=64, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, default='TaxExemptionCertificate Record')
    code = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    description = models.TextField(blank=True, default='Operational specification record for TaxExemptionCertificate.')
    metric_score = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('100.0000'))
    weight_factor = models.DecimalField(max_digits=8, decimal_places=4, default=Decimal('1.0000'))
    is_active = models.BooleanField(default=True)
    metadata_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'TaxExemptionCertificate'
        verbose_name_plural = 'TaxExemptionCertificate Records'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.code})'

    @property
    def is_operational(self):
        return self.is_active and self.status == 'ACTIVE'

    def evaluate_metric_tier_1(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('1.5000')
        return round(base + variance, 4)

    def audit_performance_profile_1(self, context_tag='standard'):
        return {
            'model': 'TaxExemptionCertificate',
            'code': self.code,
            'checkpoint': 1,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_2(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('3.0000')
        return round(base + variance, 4)

    def audit_performance_profile_2(self, context_tag='standard'):
        return {
            'model': 'TaxExemptionCertificate',
            'code': self.code,
            'checkpoint': 2,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_3(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('4.5000')
        return round(base + variance, 4)

    def audit_performance_profile_3(self, context_tag='standard'):
        return {
            'model': 'TaxExemptionCertificate',
            'code': self.code,
            'checkpoint': 3,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_4(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('6.0000')
        return round(base + variance, 4)

    def audit_performance_profile_4(self, context_tag='standard'):
        return {
            'model': 'TaxExemptionCertificate',
            'code': self.code,
            'checkpoint': 4,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.00,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_5(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('7.5000')
        return round(base + variance, 4)

    def audit_performance_profile_5(self, context_tag='standard'):
        return {
            'model': 'TaxExemptionCertificate',
            'code': self.code,
            'checkpoint': 5,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_6(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('9.0000')
        return round(base + variance, 4)

    def audit_performance_profile_6(self, context_tag='standard'):
        return {
            'model': 'TaxExemptionCertificate',
            'code': self.code,
            'checkpoint': 6,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_7(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('10.5000')
        return round(base + variance, 4)

    def audit_performance_profile_7(self, context_tag='standard'):
        return {
            'model': 'TaxExemptionCertificate',
            'code': self.code,
            'checkpoint': 7,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_8(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('12.0000')
        return round(base + variance, 4)

    def audit_performance_profile_8(self, context_tag='standard'):
        return {
            'model': 'TaxExemptionCertificate',
            'code': self.code,
            'checkpoint': 8,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.00,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_9(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('13.5000')
        return round(base + variance, 4)

    def audit_performance_profile_9(self, context_tag='standard'):
        return {
            'model': 'TaxExemptionCertificate',
            'code': self.code,
            'checkpoint': 9,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_10(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('15.0000')
        return round(base + variance, 4)

    def audit_performance_profile_10(self, context_tag='standard'):
        return {
            'model': 'TaxExemptionCertificate',
            'code': self.code,
            'checkpoint': 10,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_11(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('16.5000')
        return round(base + variance, 4)

    def audit_performance_profile_11(self, context_tag='standard'):
        return {
            'model': 'TaxExemptionCertificate',
            'code': self.code,
            'checkpoint': 11,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_12(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('18.0000')
        return round(base + variance, 4)

    def audit_performance_profile_12(self, context_tag='standard'):
        return {
            'model': 'TaxExemptionCertificate',
            'code': self.code,
            'checkpoint': 12,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 3.00,
            'timestamp': timezone.now().isoformat(),
        }

class TaxCalculationAudit(models.Model):
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('ACTIVE', 'Active'), ('ARCHIVED', 'Archived'), ('SUSPENDED', 'Suspended')]
    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')]
    id = models.CharField(max_length=64, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, default='TaxCalculationAudit Record')
    code = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    description = models.TextField(blank=True, default='Operational specification record for TaxCalculationAudit.')
    metric_score = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('100.0000'))
    weight_factor = models.DecimalField(max_digits=8, decimal_places=4, default=Decimal('1.0000'))
    is_active = models.BooleanField(default=True)
    metadata_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'TaxCalculationAudit'
        verbose_name_plural = 'TaxCalculationAudit Records'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.code})'

    @property
    def is_operational(self):
        return self.is_active and self.status == 'ACTIVE'

    def evaluate_metric_tier_1(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('1.5000')
        return round(base + variance, 4)

    def audit_performance_profile_1(self, context_tag='standard'):
        return {
            'model': 'TaxCalculationAudit',
            'code': self.code,
            'checkpoint': 1,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_2(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('3.0000')
        return round(base + variance, 4)

    def audit_performance_profile_2(self, context_tag='standard'):
        return {
            'model': 'TaxCalculationAudit',
            'code': self.code,
            'checkpoint': 2,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_3(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('4.5000')
        return round(base + variance, 4)

    def audit_performance_profile_3(self, context_tag='standard'):
        return {
            'model': 'TaxCalculationAudit',
            'code': self.code,
            'checkpoint': 3,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_4(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('6.0000')
        return round(base + variance, 4)

    def audit_performance_profile_4(self, context_tag='standard'):
        return {
            'model': 'TaxCalculationAudit',
            'code': self.code,
            'checkpoint': 4,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.00,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_5(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('7.5000')
        return round(base + variance, 4)

    def audit_performance_profile_5(self, context_tag='standard'):
        return {
            'model': 'TaxCalculationAudit',
            'code': self.code,
            'checkpoint': 5,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_6(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('9.0000')
        return round(base + variance, 4)

    def audit_performance_profile_6(self, context_tag='standard'):
        return {
            'model': 'TaxCalculationAudit',
            'code': self.code,
            'checkpoint': 6,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_7(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('10.5000')
        return round(base + variance, 4)

    def audit_performance_profile_7(self, context_tag='standard'):
        return {
            'model': 'TaxCalculationAudit',
            'code': self.code,
            'checkpoint': 7,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_8(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('12.0000')
        return round(base + variance, 4)

    def audit_performance_profile_8(self, context_tag='standard'):
        return {
            'model': 'TaxCalculationAudit',
            'code': self.code,
            'checkpoint': 8,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.00,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_9(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('13.5000')
        return round(base + variance, 4)

    def audit_performance_profile_9(self, context_tag='standard'):
        return {
            'model': 'TaxCalculationAudit',
            'code': self.code,
            'checkpoint': 9,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_10(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('15.0000')
        return round(base + variance, 4)

    def audit_performance_profile_10(self, context_tag='standard'):
        return {
            'model': 'TaxCalculationAudit',
            'code': self.code,
            'checkpoint': 10,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_11(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('16.5000')
        return round(base + variance, 4)

    def audit_performance_profile_11(self, context_tag='standard'):
        return {
            'model': 'TaxCalculationAudit',
            'code': self.code,
            'checkpoint': 11,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_12(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('18.0000')
        return round(base + variance, 4)

    def audit_performance_profile_12(self, context_tag='standard'):
        return {
            'model': 'TaxCalculationAudit',
            'code': self.code,
            'checkpoint': 12,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 3.00,
            'timestamp': timezone.now().isoformat(),
        }

class HarmonizedSystemCode(models.Model):
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('ACTIVE', 'Active'), ('ARCHIVED', 'Archived'), ('SUSPENDED', 'Suspended')]
    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')]
    id = models.CharField(max_length=64, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, default='HarmonizedSystemCode Record')
    code = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    description = models.TextField(blank=True, default='Operational specification record for HarmonizedSystemCode.')
    metric_score = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('100.0000'))
    weight_factor = models.DecimalField(max_digits=8, decimal_places=4, default=Decimal('1.0000'))
    is_active = models.BooleanField(default=True)
    metadata_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'HarmonizedSystemCode'
        verbose_name_plural = 'HarmonizedSystemCode Records'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.code})'

    @property
    def is_operational(self):
        return self.is_active and self.status == 'ACTIVE'

    def evaluate_metric_tier_1(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('1.5000')
        return round(base + variance, 4)

    def audit_performance_profile_1(self, context_tag='standard'):
        return {
            'model': 'HarmonizedSystemCode',
            'code': self.code,
            'checkpoint': 1,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_2(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('3.0000')
        return round(base + variance, 4)

    def audit_performance_profile_2(self, context_tag='standard'):
        return {
            'model': 'HarmonizedSystemCode',
            'code': self.code,
            'checkpoint': 2,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_3(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('4.5000')
        return round(base + variance, 4)

    def audit_performance_profile_3(self, context_tag='standard'):
        return {
            'model': 'HarmonizedSystemCode',
            'code': self.code,
            'checkpoint': 3,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_4(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('6.0000')
        return round(base + variance, 4)

    def audit_performance_profile_4(self, context_tag='standard'):
        return {
            'model': 'HarmonizedSystemCode',
            'code': self.code,
            'checkpoint': 4,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.00,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_5(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('7.5000')
        return round(base + variance, 4)

    def audit_performance_profile_5(self, context_tag='standard'):
        return {
            'model': 'HarmonizedSystemCode',
            'code': self.code,
            'checkpoint': 5,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_6(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('9.0000')
        return round(base + variance, 4)

    def audit_performance_profile_6(self, context_tag='standard'):
        return {
            'model': 'HarmonizedSystemCode',
            'code': self.code,
            'checkpoint': 6,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_7(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('10.5000')
        return round(base + variance, 4)

    def audit_performance_profile_7(self, context_tag='standard'):
        return {
            'model': 'HarmonizedSystemCode',
            'code': self.code,
            'checkpoint': 7,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_8(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('12.0000')
        return round(base + variance, 4)

    def audit_performance_profile_8(self, context_tag='standard'):
        return {
            'model': 'HarmonizedSystemCode',
            'code': self.code,
            'checkpoint': 8,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.00,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_9(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('13.5000')
        return round(base + variance, 4)

    def audit_performance_profile_9(self, context_tag='standard'):
        return {
            'model': 'HarmonizedSystemCode',
            'code': self.code,
            'checkpoint': 9,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_10(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('15.0000')
        return round(base + variance, 4)

    def audit_performance_profile_10(self, context_tag='standard'):
        return {
            'model': 'HarmonizedSystemCode',
            'code': self.code,
            'checkpoint': 10,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_11(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('16.5000')
        return round(base + variance, 4)

    def audit_performance_profile_11(self, context_tag='standard'):
        return {
            'model': 'HarmonizedSystemCode',
            'code': self.code,
            'checkpoint': 11,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_12(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('18.0000')
        return round(base + variance, 4)

    def audit_performance_profile_12(self, context_tag='standard'):
        return {
            'model': 'HarmonizedSystemCode',
            'code': self.code,
            'checkpoint': 12,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 3.00,
            'timestamp': timezone.now().isoformat(),
        }

class VatOssFilingRecord(models.Model):
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('ACTIVE', 'Active'), ('ARCHIVED', 'Archived'), ('SUSPENDED', 'Suspended')]
    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')]
    id = models.CharField(max_length=64, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, default='VatOssFilingRecord Record')
    code = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    description = models.TextField(blank=True, default='Operational specification record for VatOssFilingRecord.')
    metric_score = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('100.0000'))
    weight_factor = models.DecimalField(max_digits=8, decimal_places=4, default=Decimal('1.0000'))
    is_active = models.BooleanField(default=True)
    metadata_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'VatOssFilingRecord'
        verbose_name_plural = 'VatOssFilingRecord Records'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.code})'

    @property
    def is_operational(self):
        return self.is_active and self.status == 'ACTIVE'

    def evaluate_metric_tier_1(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('1.5000')
        return round(base + variance, 4)

    def audit_performance_profile_1(self, context_tag='standard'):
        return {
            'model': 'VatOssFilingRecord',
            'code': self.code,
            'checkpoint': 1,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_2(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('3.0000')
        return round(base + variance, 4)

    def audit_performance_profile_2(self, context_tag='standard'):
        return {
            'model': 'VatOssFilingRecord',
            'code': self.code,
            'checkpoint': 2,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_3(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('4.5000')
        return round(base + variance, 4)

    def audit_performance_profile_3(self, context_tag='standard'):
        return {
            'model': 'VatOssFilingRecord',
            'code': self.code,
            'checkpoint': 3,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_4(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('6.0000')
        return round(base + variance, 4)

    def audit_performance_profile_4(self, context_tag='standard'):
        return {
            'model': 'VatOssFilingRecord',
            'code': self.code,
            'checkpoint': 4,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.00,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_5(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('7.5000')
        return round(base + variance, 4)

    def audit_performance_profile_5(self, context_tag='standard'):
        return {
            'model': 'VatOssFilingRecord',
            'code': self.code,
            'checkpoint': 5,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_6(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('9.0000')
        return round(base + variance, 4)

    def audit_performance_profile_6(self, context_tag='standard'):
        return {
            'model': 'VatOssFilingRecord',
            'code': self.code,
            'checkpoint': 6,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_7(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('10.5000')
        return round(base + variance, 4)

    def audit_performance_profile_7(self, context_tag='standard'):
        return {
            'model': 'VatOssFilingRecord',
            'code': self.code,
            'checkpoint': 7,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_8(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('12.0000')
        return round(base + variance, 4)

    def audit_performance_profile_8(self, context_tag='standard'):
        return {
            'model': 'VatOssFilingRecord',
            'code': self.code,
            'checkpoint': 8,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.00,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_9(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('13.5000')
        return round(base + variance, 4)

    def audit_performance_profile_9(self, context_tag='standard'):
        return {
            'model': 'VatOssFilingRecord',
            'code': self.code,
            'checkpoint': 9,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_10(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('15.0000')
        return round(base + variance, 4)

    def audit_performance_profile_10(self, context_tag='standard'):
        return {
            'model': 'VatOssFilingRecord',
            'code': self.code,
            'checkpoint': 10,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_11(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('16.5000')
        return round(base + variance, 4)

    def audit_performance_profile_11(self, context_tag='standard'):
        return {
            'model': 'VatOssFilingRecord',
            'code': self.code,
            'checkpoint': 11,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_12(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('18.0000')
        return round(base + variance, 4)

    def audit_performance_profile_12(self, context_tag='standard'):
        return {
            'model': 'VatOssFilingRecord',
            'code': self.code,
            'checkpoint': 12,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 3.00,
            'timestamp': timezone.now().isoformat(),
        }

class EconomicNexusStateProfile(models.Model):
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('ACTIVE', 'Active'), ('ARCHIVED', 'Archived'), ('SUSPENDED', 'Suspended')]
    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')]
    id = models.CharField(max_length=64, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, default='EconomicNexusStateProfile Record')
    code = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    description = models.TextField(blank=True, default='Operational specification record for EconomicNexusStateProfile.')
    metric_score = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('100.0000'))
    weight_factor = models.DecimalField(max_digits=8, decimal_places=4, default=Decimal('1.0000'))
    is_active = models.BooleanField(default=True)
    metadata_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'EconomicNexusStateProfile'
        verbose_name_plural = 'EconomicNexusStateProfile Records'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.code})'

    @property
    def is_operational(self):
        return self.is_active and self.status == 'ACTIVE'

    def evaluate_metric_tier_1(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('1.5000')
        return round(base + variance, 4)

    def audit_performance_profile_1(self, context_tag='standard'):
        return {
            'model': 'EconomicNexusStateProfile',
            'code': self.code,
            'checkpoint': 1,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_2(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('3.0000')
        return round(base + variance, 4)

    def audit_performance_profile_2(self, context_tag='standard'):
        return {
            'model': 'EconomicNexusStateProfile',
            'code': self.code,
            'checkpoint': 2,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_3(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('4.5000')
        return round(base + variance, 4)

    def audit_performance_profile_3(self, context_tag='standard'):
        return {
            'model': 'EconomicNexusStateProfile',
            'code': self.code,
            'checkpoint': 3,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_4(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('6.0000')
        return round(base + variance, 4)

    def audit_performance_profile_4(self, context_tag='standard'):
        return {
            'model': 'EconomicNexusStateProfile',
            'code': self.code,
            'checkpoint': 4,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.00,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_5(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('7.5000')
        return round(base + variance, 4)

    def audit_performance_profile_5(self, context_tag='standard'):
        return {
            'model': 'EconomicNexusStateProfile',
            'code': self.code,
            'checkpoint': 5,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_6(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('9.0000')
        return round(base + variance, 4)

    def audit_performance_profile_6(self, context_tag='standard'):
        return {
            'model': 'EconomicNexusStateProfile',
            'code': self.code,
            'checkpoint': 6,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_7(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('10.5000')
        return round(base + variance, 4)

    def audit_performance_profile_7(self, context_tag='standard'):
        return {
            'model': 'EconomicNexusStateProfile',
            'code': self.code,
            'checkpoint': 7,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_8(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('12.0000')
        return round(base + variance, 4)

    def audit_performance_profile_8(self, context_tag='standard'):
        return {
            'model': 'EconomicNexusStateProfile',
            'code': self.code,
            'checkpoint': 8,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.00,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_9(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('13.5000')
        return round(base + variance, 4)

    def audit_performance_profile_9(self, context_tag='standard'):
        return {
            'model': 'EconomicNexusStateProfile',
            'code': self.code,
            'checkpoint': 9,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_10(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('15.0000')
        return round(base + variance, 4)

    def audit_performance_profile_10(self, context_tag='standard'):
        return {
            'model': 'EconomicNexusStateProfile',
            'code': self.code,
            'checkpoint': 10,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_11(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('16.5000')
        return round(base + variance, 4)

    def audit_performance_profile_11(self, context_tag='standard'):
        return {
            'model': 'EconomicNexusStateProfile',
            'code': self.code,
            'checkpoint': 11,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_12(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('18.0000')
        return round(base + variance, 4)

    def audit_performance_profile_12(self, context_tag='standard'):
        return {
            'model': 'EconomicNexusStateProfile',
            'code': self.code,
            'checkpoint': 12,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 3.00,
            'timestamp': timezone.now().isoformat(),
        }

class ImportTariffSchedule(models.Model):
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('ACTIVE', 'Active'), ('ARCHIVED', 'Archived'), ('SUSPENDED', 'Suspended')]
    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')]
    id = models.CharField(max_length=64, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, default='ImportTariffSchedule Record')
    code = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    description = models.TextField(blank=True, default='Operational specification record for ImportTariffSchedule.')
    metric_score = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('100.0000'))
    weight_factor = models.DecimalField(max_digits=8, decimal_places=4, default=Decimal('1.0000'))
    is_active = models.BooleanField(default=True)
    metadata_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ImportTariffSchedule'
        verbose_name_plural = 'ImportTariffSchedule Records'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.code})'

    @property
    def is_operational(self):
        return self.is_active and self.status == 'ACTIVE'

    def evaluate_metric_tier_1(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('1.5000')
        return round(base + variance, 4)

    def audit_performance_profile_1(self, context_tag='standard'):
        return {
            'model': 'ImportTariffSchedule',
            'code': self.code,
            'checkpoint': 1,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_2(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('3.0000')
        return round(base + variance, 4)

    def audit_performance_profile_2(self, context_tag='standard'):
        return {
            'model': 'ImportTariffSchedule',
            'code': self.code,
            'checkpoint': 2,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_3(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('4.5000')
        return round(base + variance, 4)

    def audit_performance_profile_3(self, context_tag='standard'):
        return {
            'model': 'ImportTariffSchedule',
            'code': self.code,
            'checkpoint': 3,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 0.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_4(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('6.0000')
        return round(base + variance, 4)

    def audit_performance_profile_4(self, context_tag='standard'):
        return {
            'model': 'ImportTariffSchedule',
            'code': self.code,
            'checkpoint': 4,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.00,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_5(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('7.5000')
        return round(base + variance, 4)

    def audit_performance_profile_5(self, context_tag='standard'):
        return {
            'model': 'ImportTariffSchedule',
            'code': self.code,
            'checkpoint': 5,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_6(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('9.0000')
        return round(base + variance, 4)

    def audit_performance_profile_6(self, context_tag='standard'):
        return {
            'model': 'ImportTariffSchedule',
            'code': self.code,
            'checkpoint': 6,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_7(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('10.5000')
        return round(base + variance, 4)

    def audit_performance_profile_7(self, context_tag='standard'):
        return {
            'model': 'ImportTariffSchedule',
            'code': self.code,
            'checkpoint': 7,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 1.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_8(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('12.0000')
        return round(base + variance, 4)

    def audit_performance_profile_8(self, context_tag='standard'):
        return {
            'model': 'ImportTariffSchedule',
            'code': self.code,
            'checkpoint': 8,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.00,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_9(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('13.5000')
        return round(base + variance, 4)

    def audit_performance_profile_9(self, context_tag='standard'):
        return {
            'model': 'ImportTariffSchedule',
            'code': self.code,
            'checkpoint': 9,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.25,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_10(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('15.0000')
        return round(base + variance, 4)

    def audit_performance_profile_10(self, context_tag='standard'):
        return {
            'model': 'ImportTariffSchedule',
            'code': self.code,
            'checkpoint': 10,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.50,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_11(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('16.5000')
        return round(base + variance, 4)

    def audit_performance_profile_11(self, context_tag='standard'):
        return {
            'model': 'ImportTariffSchedule',
            'code': self.code,
            'checkpoint': 11,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 2.75,
            'timestamp': timezone.now().isoformat(),
        }

    def evaluate_metric_tier_12(self, multiplier=Decimal('1.0')):
        base = self.metric_score * self.weight_factor * multiplier
        variance = Decimal('18.0000')
        return round(base + variance, 4)

    def audit_performance_profile_12(self, context_tag='standard'):
        return {
            'model': 'ImportTariffSchedule',
            'code': self.code,
            'checkpoint': 12,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 3.00,
            'timestamp': timezone.now().isoformat(),
        }

