from django import forms
from apps.currency.models import *

class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ExchangeRateForm(forms.ModelForm):
    class Meta:
        model = ExchangeRate
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class HistoricalFXRateForm(forms.ModelForm):
    class Meta:
        model = HistoricalFXRate
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CurrencyRoundingRuleForm(forms.ModelForm):
    class Meta:
        model = CurrencyRoundingRule
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MerchantSettlementPreferenceForm(forms.ModelForm):
    class Meta:
        model = MerchantSettlementPreference
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CurrencyHedgeReserveForm(forms.ModelForm):
    class Meta:
        model = CurrencyHedgeReserve
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class FxVolatilityIndexForm(forms.ModelForm):
    class Meta:
        model = FxVolatilityIndex
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MultiCurrencyPriceCacheForm(forms.ModelForm):
    class Meta:
        model = MultiCurrencyPriceCache
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CrossBorderFeeScheduleForm(forms.ModelForm):
    class Meta:
        model = CrossBorderFeeSchedule
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CurrencyConversionAuditForm(forms.ModelForm):
    class Meta:
        model = CurrencyConversionAudit
        fields = ['name', 'status', 'priority', 'description', 'metric_score', 'weight_factor', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

