from django.db import models
import uuid
from apps.accounts.models import User

def generate_aud_id(): return f"aud_{uuid.uuid4().hex[:12]}"
def generate_thr_id(): return f"thr_{uuid.uuid4().hex[:12]}"
def generate_flg_id(): return f"flg_{uuid.uuid4().hex[:12]}"

class SecurityAuditLog(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_aud_id)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='security_audit_logs')
    action = models.CharField(max_length=100)
    module = models.CharField(max_length=50)
    entity_type = models.CharField(max_length=50, blank=True, null=True)
    entity_id = models.CharField(max_length=64, blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    metadata_json = models.TextField(default='{}')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.module}] {self.action} by {self.user.email if self.user else 'System'}"


class SecurityThreatIP(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_thr_id)
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.CharField(max_length=200)
    threat_level = models.CharField(max_length=20, default='MEDIUM')
    is_blocked = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class FeatureFlag(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_flg_id)
    flag_key = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_enabled = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.flag_key}: {'ENABLED' if self.is_enabled else 'DISABLED'}"
