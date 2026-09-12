from django import forms
from apps.fraud_detection.models import *

class FraudRuleForm(forms.ModelForm):
    class Meta:
        model = FraudRule
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CheckoutRiskScoreForm(forms.ModelForm):
    class Meta:
        model = CheckoutRiskScore
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class VelocityCounterForm(forms.ModelForm):
    class Meta:
        model = VelocityCounter
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BlacklistedIdentifierForm(forms.ModelForm):
    class Meta:
        model = BlacklistedIdentifier
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class QuarantinedOrderForm(forms.ModelForm):
    class Meta:
        model = QuarantinedOrder
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class FraudInvestigationCaseForm(forms.ModelForm):
    class Meta:
        model = FraudInvestigationCase
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DeviceFingerprintProfileForm(forms.ModelForm):
    class Meta:
        model = DeviceFingerprintProfile
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class GeographicAnomalyLogForm(forms.ModelForm):
    class Meta:
        model = GeographicAnomalyLog
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ChargebackRiskIndexForm(forms.ModelForm):
    class Meta:
        model = ChargebackRiskIndex
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class TrustFactorCredentialForm(forms.ModelForm):
    class Meta:
        model = TrustFactorCredential
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

