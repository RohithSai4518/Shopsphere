import json
from .models import SecurityAuditLog, SecurityThreatIP, FeatureFlag

class SecurityAuditService:
    @staticmethod
    def log_event(user, action, module, entity_type=None, entity_id=None, ip_address=None, metadata=None):
        meta_str = json.dumps(metadata or {})
        return SecurityAuditLog.objects.create(
            user=user if user and user.is_authenticated else None,
            action=action,
            module=module,
            entity_type=entity_type,
            entity_id=entity_id,
            ip_address=ip_address,
            metadata_json=meta_str
        )

    @staticmethod
    def is_ip_blocked(ip_address):
        if not ip_address:
            return False
        threat = SecurityThreatIP.objects.filter(ip_address=ip_address, is_blocked=True).first()
        return threat is not None

    @staticmethod
    def is_feature_enabled(flag_key, default=False):
        flag = FeatureFlag.objects.filter(flag_key=flag_key).first()
        return flag.is_enabled if flag else default
