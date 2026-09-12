from django import forms
from apps.loyalty.models import *

class LoyaltyTierForm(forms.ModelForm):
    class Meta:
        model = LoyaltyTier
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LoyaltyAccountForm(forms.ModelForm):
    class Meta:
        model = LoyaltyAccount
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PointTransactionLedgerForm(forms.ModelForm):
    class Meta:
        model = PointTransactionLedger
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LoyaltyRewardForm(forms.ModelForm):
    class Meta:
        model = LoyaltyReward
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class GamificationBadgeForm(forms.ModelForm):
    class Meta:
        model = GamificationBadge
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MilestoneStreakForm(forms.ModelForm):
    class Meta:
        model = MilestoneStreak
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BonusPointEventForm(forms.ModelForm):
    class Meta:
        model = BonusPointEvent
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RewardRedemptionOptionForm(forms.ModelForm):
    class Meta:
        model = RewardRedemptionOption
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class TierQualificationRuleForm(forms.ModelForm):
    class Meta:
        model = TierQualificationRule
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LoyaltyEngagementAuditForm(forms.ModelForm):
    class Meta:
        model = LoyaltyEngagementAudit
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

