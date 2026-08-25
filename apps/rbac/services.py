from .models import Role, Permission, RolePermission, UserRole
from apps.audit.models import SecurityAuditLog

class RBACService:
    @staticmethod
    def user_has_permission(user, permission_code):
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser or user.role == 'ADMIN':
            return True

        # Check explicit UserRole linkage
        user_roles = UserRole.objects.filter(user=user).values_list('role_id', flat=True)
        return RolePermission.objects.filter(
            role_id__in=user_roles,
            permission__code=permission_code
        ).exists()

    @staticmethod
    def assign_role_to_user(user, role_name, assigned_by=None):
        role = Role.objects.filter(name=role_name).first()
        if not role:
            role = Role.objects.create(name=role_name, description=f"{role_name} System Role")

        user_role, created = UserRole.objects.get_or_create(user=user, role=role)
        user.role = role_name
        user.save()

        if assigned_by:
            SecurityAuditLog.objects.create(
                user=assigned_by,
                action='ROLE_ASSIGNED',
                module='rbac',
                entity_type='User',
                entity_id=user.id,
                metadata_json=f'{{"role": "{role_name}"}}'
            )

        return user_role
