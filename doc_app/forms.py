from django import forms

DOC_TYPES = [
    ('SOP', 'Standard Operating Procedure'),
    ('HR', 'HR Policy'),
    ('QUALITY', 'Quality Manual')
]

class DocumentRequestForm(forms.Form):
    nic_number = forms.CharField(max_length=12, label="NIC Number")
    company_name = forms.CharField(max_length=100)
    logo = forms.ImageField(required=False)
    doc_number = forms.CharField(max_length=50, label="Document Number")
    effective_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    company_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    document_type = forms.ChoiceField(choices=DOC_TYPES)