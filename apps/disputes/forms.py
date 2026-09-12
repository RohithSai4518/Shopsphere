from django import forms
from apps.disputes.models import *

class DisputeClaimForm(forms.ModelForm):
    class Meta:
        model = DisputeClaim
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DisputeEvidenceForm(forms.ModelForm):
    class Meta:
        model = DisputeEvidence
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ArbitrationTimelineForm(forms.ModelForm):
    class Meta:
        model = ArbitrationTimeline
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class TribunalRulingForm(forms.ModelForm):
    class Meta:
        model = TribunalRuling
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EscrowDisputeHoldForm(forms.ModelForm):
    class Meta:
        model = EscrowDisputeHold
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DisputeAppealForm(forms.ModelForm):
    class Meta:
        model = DisputeAppeal
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MediatorNoteForm(forms.ModelForm):
    class Meta:
        model = MediatorNote
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ResolutionPolicyMatrixForm(forms.ModelForm):
    class Meta:
        model = ResolutionPolicyMatrix
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MerchantDisputeMetricsForm(forms.ModelForm):
    class Meta:
        model = MerchantDisputeMetrics
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DisputeSettlementVoucherForm(forms.ModelForm):
    class Meta:
        model = DisputeSettlementVoucher
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

