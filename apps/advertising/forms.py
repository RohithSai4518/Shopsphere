from django import forms
from apps.advertising.models import *

class AdCampaignForm(forms.ModelForm):
    class Meta:
        model = AdCampaign
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AdGroupForm(forms.ModelForm):
    class Meta:
        model = AdGroup
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class KeywordTargetForm(forms.ModelForm):
    class Meta:
        model = KeywordTarget
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class NegativeKeywordForm(forms.ModelForm):
    class Meta:
        model = NegativeKeyword
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AdPlacementBidForm(forms.ModelForm):
    class Meta:
        model = AdPlacementBid
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AdImpressionLogForm(forms.ModelForm):
    class Meta:
        model = AdImpressionLog
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AdClickAttributionForm(forms.ModelForm):
    class Meta:
        model = AdClickAttribution
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AdSpendLedgerForm(forms.ModelForm):
    class Meta:
        model = AdSpendLedger
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CampaignPacingProfileForm(forms.ModelForm):
    class Meta:
        model = CampaignPacingProfile
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class TargetRoasThresholdForm(forms.ModelForm):
    class Meta:
        model = TargetRoasThreshold
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

