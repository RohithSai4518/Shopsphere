from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
import uuid

class LoyaltyTier(models.Model):
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('ACTIVE', 'Active'), ('ARCHIVED', 'Archived'), ('SUSPENDED', 'Suspended')]
    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')]
    id = models.CharField(max_length=64, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, default='LoyaltyTier Record')
    code = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    description = models.TextField(blank=True, default='Operational specification record for LoyaltyTier.')
    metric_score = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('100.0000'))
    weight_factor = models.DecimalField(max_digits=8, decimal_places=4, default=Decimal('1.0000'))
    is_active = models.BooleanField(default=True)
    metadata_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'LoyaltyTier'
        verbose_name_plural = 'LoyaltyTier Records'
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
            'model': 'LoyaltyTier',
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
            'model': 'LoyaltyTier',
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
            'model': 'LoyaltyTier',
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
            'model': 'LoyaltyTier',
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
            'model': 'LoyaltyTier',
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
            'model': 'LoyaltyTier',
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
            'model': 'LoyaltyTier',
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
            'model': 'LoyaltyTier',
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
            'model': 'LoyaltyTier',
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
            'model': 'LoyaltyTier',
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
            'model': 'LoyaltyTier',
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
            'model': 'LoyaltyTier',
            'code': self.code,
            'checkpoint': 12,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 3.00,
            'timestamp': timezone.now().isoformat(),
        }

class LoyaltyAccount(models.Model):
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('ACTIVE', 'Active'), ('ARCHIVED', 'Archived'), ('SUSPENDED', 'Suspended')]
    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')]
    id = models.CharField(max_length=64, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, default='LoyaltyAccount Record')
    code = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    description = models.TextField(blank=True, default='Operational specification record for LoyaltyAccount.')
    metric_score = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('100.0000'))
    weight_factor = models.DecimalField(max_digits=8, decimal_places=4, default=Decimal('1.0000'))
    is_active = models.BooleanField(default=True)
    metadata_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'LoyaltyAccount'
        verbose_name_plural = 'LoyaltyAccount Records'
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
            'model': 'LoyaltyAccount',
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
            'model': 'LoyaltyAccount',
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
            'model': 'LoyaltyAccount',
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
            'model': 'LoyaltyAccount',
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
            'model': 'LoyaltyAccount',
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
            'model': 'LoyaltyAccount',
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
            'model': 'LoyaltyAccount',
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
            'model': 'LoyaltyAccount',
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
            'model': 'LoyaltyAccount',
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
            'model': 'LoyaltyAccount',
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
            'model': 'LoyaltyAccount',
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
            'model': 'LoyaltyAccount',
            'code': self.code,
            'checkpoint': 12,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 3.00,
            'timestamp': timezone.now().isoformat(),
        }

class PointTransactionLedger(models.Model):
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('ACTIVE', 'Active'), ('ARCHIVED', 'Archived'), ('SUSPENDED', 'Suspended')]
    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')]
    id = models.CharField(max_length=64, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, default='PointTransactionLedger Record')
    code = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    description = models.TextField(blank=True, default='Operational specification record for PointTransactionLedger.')
    metric_score = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('100.0000'))
    weight_factor = models.DecimalField(max_digits=8, decimal_places=4, default=Decimal('1.0000'))
    is_active = models.BooleanField(default=True)
    metadata_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'PointTransactionLedger'
        verbose_name_plural = 'PointTransactionLedger Records'
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
            'model': 'PointTransactionLedger',
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
            'model': 'PointTransactionLedger',
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
            'model': 'PointTransactionLedger',
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
            'model': 'PointTransactionLedger',
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
            'model': 'PointTransactionLedger',
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
            'model': 'PointTransactionLedger',
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
            'model': 'PointTransactionLedger',
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
            'model': 'PointTransactionLedger',
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
            'model': 'PointTransactionLedger',
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
            'model': 'PointTransactionLedger',
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
            'model': 'PointTransactionLedger',
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
            'model': 'PointTransactionLedger',
            'code': self.code,
            'checkpoint': 12,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 3.00,
            'timestamp': timezone.now().isoformat(),
        }

class LoyaltyReward(models.Model):
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('ACTIVE', 'Active'), ('ARCHIVED', 'Archived'), ('SUSPENDED', 'Suspended')]
    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')]
    id = models.CharField(max_length=64, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, default='LoyaltyReward Record')
    code = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    description = models.TextField(blank=True, default='Operational specification record for LoyaltyReward.')
    metric_score = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('100.0000'))
    weight_factor = models.DecimalField(max_digits=8, decimal_places=4, default=Decimal('1.0000'))
    is_active = models.BooleanField(default=True)
    metadata_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'LoyaltyReward'
        verbose_name_plural = 'LoyaltyReward Records'
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
            'model': 'LoyaltyReward',
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
            'model': 'LoyaltyReward',
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
            'model': 'LoyaltyReward',
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
            'model': 'LoyaltyReward',
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
            'model': 'LoyaltyReward',
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
            'model': 'LoyaltyReward',
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
            'model': 'LoyaltyReward',
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
            'model': 'LoyaltyReward',
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
            'model': 'LoyaltyReward',
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
            'model': 'LoyaltyReward',
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
            'model': 'LoyaltyReward',
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
            'model': 'LoyaltyReward',
            'code': self.code,
            'checkpoint': 12,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 3.00,
            'timestamp': timezone.now().isoformat(),
        }

class GamificationBadge(models.Model):
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('ACTIVE', 'Active'), ('ARCHIVED', 'Archived'), ('SUSPENDED', 'Suspended')]
    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')]
    id = models.CharField(max_length=64, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, default='GamificationBadge Record')
    code = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    description = models.TextField(blank=True, default='Operational specification record for GamificationBadge.')
    metric_score = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('100.0000'))
    weight_factor = models.DecimalField(max_digits=8, decimal_places=4, default=Decimal('1.0000'))
    is_active = models.BooleanField(default=True)
    metadata_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'GamificationBadge'
        verbose_name_plural = 'GamificationBadge Records'
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
            'model': 'GamificationBadge',
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
            'model': 'GamificationBadge',
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
            'model': 'GamificationBadge',
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
            'model': 'GamificationBadge',
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
            'model': 'GamificationBadge',
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
            'model': 'GamificationBadge',
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
            'model': 'GamificationBadge',
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
            'model': 'GamificationBadge',
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
            'model': 'GamificationBadge',
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
            'model': 'GamificationBadge',
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
            'model': 'GamificationBadge',
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
            'model': 'GamificationBadge',
            'code': self.code,
            'checkpoint': 12,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 3.00,
            'timestamp': timezone.now().isoformat(),
        }

class MilestoneStreak(models.Model):
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('ACTIVE', 'Active'), ('ARCHIVED', 'Archived'), ('SUSPENDED', 'Suspended')]
    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')]
    id = models.CharField(max_length=64, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, default='MilestoneStreak Record')
    code = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    description = models.TextField(blank=True, default='Operational specification record for MilestoneStreak.')
    metric_score = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('100.0000'))
    weight_factor = models.DecimalField(max_digits=8, decimal_places=4, default=Decimal('1.0000'))
    is_active = models.BooleanField(default=True)
    metadata_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'MilestoneStreak'
        verbose_name_plural = 'MilestoneStreak Records'
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
            'model': 'MilestoneStreak',
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
            'model': 'MilestoneStreak',
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
            'model': 'MilestoneStreak',
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
            'model': 'MilestoneStreak',
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
            'model': 'MilestoneStreak',
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
            'model': 'MilestoneStreak',
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
            'model': 'MilestoneStreak',
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
            'model': 'MilestoneStreak',
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
            'model': 'MilestoneStreak',
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
            'model': 'MilestoneStreak',
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
            'model': 'MilestoneStreak',
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
            'model': 'MilestoneStreak',
            'code': self.code,
            'checkpoint': 12,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 3.00,
            'timestamp': timezone.now().isoformat(),
        }

class BonusPointEvent(models.Model):
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('ACTIVE', 'Active'), ('ARCHIVED', 'Archived'), ('SUSPENDED', 'Suspended')]
    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')]
    id = models.CharField(max_length=64, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, default='BonusPointEvent Record')
    code = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    description = models.TextField(blank=True, default='Operational specification record for BonusPointEvent.')
    metric_score = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('100.0000'))
    weight_factor = models.DecimalField(max_digits=8, decimal_places=4, default=Decimal('1.0000'))
    is_active = models.BooleanField(default=True)
    metadata_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'BonusPointEvent'
        verbose_name_plural = 'BonusPointEvent Records'
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
            'model': 'BonusPointEvent',
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
            'model': 'BonusPointEvent',
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
            'model': 'BonusPointEvent',
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
            'model': 'BonusPointEvent',
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
            'model': 'BonusPointEvent',
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
            'model': 'BonusPointEvent',
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
            'model': 'BonusPointEvent',
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
            'model': 'BonusPointEvent',
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
            'model': 'BonusPointEvent',
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
            'model': 'BonusPointEvent',
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
            'model': 'BonusPointEvent',
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
            'model': 'BonusPointEvent',
            'code': self.code,
            'checkpoint': 12,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 3.00,
            'timestamp': timezone.now().isoformat(),
        }

class RewardRedemptionOption(models.Model):
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('ACTIVE', 'Active'), ('ARCHIVED', 'Archived'), ('SUSPENDED', 'Suspended')]
    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')]
    id = models.CharField(max_length=64, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, default='RewardRedemptionOption Record')
    code = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    description = models.TextField(blank=True, default='Operational specification record for RewardRedemptionOption.')
    metric_score = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('100.0000'))
    weight_factor = models.DecimalField(max_digits=8, decimal_places=4, default=Decimal('1.0000'))
    is_active = models.BooleanField(default=True)
    metadata_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'RewardRedemptionOption'
        verbose_name_plural = 'RewardRedemptionOption Records'
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
            'model': 'RewardRedemptionOption',
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
            'model': 'RewardRedemptionOption',
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
            'model': 'RewardRedemptionOption',
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
            'model': 'RewardRedemptionOption',
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
            'model': 'RewardRedemptionOption',
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
            'model': 'RewardRedemptionOption',
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
            'model': 'RewardRedemptionOption',
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
            'model': 'RewardRedemptionOption',
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
            'model': 'RewardRedemptionOption',
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
            'model': 'RewardRedemptionOption',
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
            'model': 'RewardRedemptionOption',
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
            'model': 'RewardRedemptionOption',
            'code': self.code,
            'checkpoint': 12,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 3.00,
            'timestamp': timezone.now().isoformat(),
        }

class TierQualificationRule(models.Model):
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('ACTIVE', 'Active'), ('ARCHIVED', 'Archived'), ('SUSPENDED', 'Suspended')]
    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')]
    id = models.CharField(max_length=64, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, default='TierQualificationRule Record')
    code = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    description = models.TextField(blank=True, default='Operational specification record for TierQualificationRule.')
    metric_score = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('100.0000'))
    weight_factor = models.DecimalField(max_digits=8, decimal_places=4, default=Decimal('1.0000'))
    is_active = models.BooleanField(default=True)
    metadata_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'TierQualificationRule'
        verbose_name_plural = 'TierQualificationRule Records'
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
            'model': 'TierQualificationRule',
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
            'model': 'TierQualificationRule',
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
            'model': 'TierQualificationRule',
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
            'model': 'TierQualificationRule',
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
            'model': 'TierQualificationRule',
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
            'model': 'TierQualificationRule',
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
            'model': 'TierQualificationRule',
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
            'model': 'TierQualificationRule',
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
            'model': 'TierQualificationRule',
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
            'model': 'TierQualificationRule',
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
            'model': 'TierQualificationRule',
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
            'model': 'TierQualificationRule',
            'code': self.code,
            'checkpoint': 12,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 3.00,
            'timestamp': timezone.now().isoformat(),
        }

class LoyaltyEngagementAudit(models.Model):
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('ACTIVE', 'Active'), ('ARCHIVED', 'Archived'), ('SUSPENDED', 'Suspended')]
    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')]
    id = models.CharField(max_length=64, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, default='LoyaltyEngagementAudit Record')
    code = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    description = models.TextField(blank=True, default='Operational specification record for LoyaltyEngagementAudit.')
    metric_score = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('100.0000'))
    weight_factor = models.DecimalField(max_digits=8, decimal_places=4, default=Decimal('1.0000'))
    is_active = models.BooleanField(default=True)
    metadata_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'LoyaltyEngagementAudit'
        verbose_name_plural = 'LoyaltyEngagementAudit Records'
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
            'model': 'LoyaltyEngagementAudit',
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
            'model': 'LoyaltyEngagementAudit',
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
            'model': 'LoyaltyEngagementAudit',
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
            'model': 'LoyaltyEngagementAudit',
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
            'model': 'LoyaltyEngagementAudit',
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
            'model': 'LoyaltyEngagementAudit',
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
            'model': 'LoyaltyEngagementAudit',
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
            'model': 'LoyaltyEngagementAudit',
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
            'model': 'LoyaltyEngagementAudit',
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
            'model': 'LoyaltyEngagementAudit',
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
            'model': 'LoyaltyEngagementAudit',
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
            'model': 'LoyaltyEngagementAudit',
            'code': self.code,
            'checkpoint': 12,
            'context': context_tag,
            'operational': self.is_operational,
            'calculated_index': float(self.metric_score) * 3.00,
            'timestamp': timezone.now().isoformat(),
        }

