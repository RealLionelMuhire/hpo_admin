from django import forms
from django.core.exceptions import ValidationError
from .models import Question, Player


class PlayerAdminForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = '__all__'
        widgets = {
            'player_name': forms.TextInput(attrs={'placeholder': 'Enter full name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
            'province': forms.Select(attrs={'onchange': 'filterDistricts(this.value)', 'id': 'id_province'}),
            'district': forms.Select(attrs={'id': 'id_district'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Province-District mapping
        self.province_districts = {
            'Kigali City': ['Gasabo', 'Kicukiro', 'Nyarugenge'],
            'Northern Province': ['Burera', 'Gakenke', 'Gicumbi', 'Musanze', 'Rulindo'],
            'Southern Province': ['Gisagara', 'Huye', 'Kamonyi', 'Muhanga', 'Nyamagabe', 'Nyanza', 'Nyaruguru', 'Ruhango'],
            'Eastern Province': ['Bugesera', 'Gatsibo', 'Kayonza', 'Kirehe', 'Ngoma', 'Nyagatare', 'Rwamagana'],
            'Western Province': ['Karongi', 'Ngororero', 'Nyabihu', 'Nyamasheke', 'Rubavu', 'Rusizi', 'Rutsiro'],
        }
        
        # Add help text for location fields
        self.fields['province'].help_text = 'Select your province in Rwanda'
        self.fields['district'].help_text = 'Select your district (filtered based on province)'
        
        # Make province and district more user-friendly
        self.fields['province'].empty_label = '--- Select Province ---'
        self.fields['district'].empty_label = '--- Select District ---'
        
        # If editing existing player with province selected, filter districts
        if self.instance and self.instance.pk and self.instance.province:
            district_choices = [('', '--- Select District ---')]
            for district in self.province_districts.get(self.instance.province, []):
                district_choices.append((district, district))
            self.fields['district'].choices = district_choices
    
    def clean(self):
        cleaned_data = super().clean()
        province = cleaned_data.get('province')
        district = cleaned_data.get('district')
        
        # Validate province-district combination
        if province and district:
            valid_districts = self.province_districts.get(province, [])
            if district not in valid_districts:
                raise ValidationError(f'District {district} is not valid for {province}')
        
        return cleaned_data
    
    class Media:
        js = ('admin/js/player_location_filter.js',)


class QuestionAdminForm(forms.ModelForm):
    # Additional fields for multiple choice options
    option_1 = forms.CharField(max_length=255, required=False, help_text="First option (required for multiple choice)")
    option_2 = forms.CharField(max_length=255, required=False, help_text="Second option (required for multiple choice)")
    option_3 = forms.CharField(max_length=255, required=False, help_text="Third option (optional)")
    option_4 = forms.CharField(max_length=255, required=False, help_text="Fourth option (optional)")
    
    class Meta:
        model = Question
        fields = [
            'question_text', 'question_type', 'card', 'options', 
            'correct_answer', 'explanation', 'points', 'difficulty'
        ]
        widgets = {
            'question_text': forms.Textarea(attrs={'rows': 4, 'cols': 80}),
            'explanation': forms.Textarea(attrs={'rows': 3, 'cols': 80}),
            'options': forms.HiddenInput(),  # Hide the raw JSON field
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # If editing existing question, populate option fields
        if self.instance and self.instance.pk:
            if self.instance.question_type == 'multiple_choice' and self.instance.options:
                options = self.instance.options
                for i, option in enumerate(options[:4]):  # Max 4 options
                    field_name = f'option_{i+1}'
                    if field_name in self.fields:
                        self.initial[field_name] = option
        
        # Add CSS classes and help text
        self.fields['question_text'].widget.attrs.update({
            'placeholder': 'Enter your question here...',
            'class': 'vLargeTextField'
        })
        
        self.fields['question_type'].widget.attrs.update({
            'class': 'question-type-selector',
            'onchange': 'toggleQuestionFields(this.value)'
        })
        
        # Simple card field - no special styling
        self.fields['card'].help_text = 'Choose a playing card to associate with this question (optional)'
        
        # Set help text based on question type
        if self.instance and self.instance.question_type == 'true_false':
            self.fields['correct_answer'].help_text = 'Select "True" or "False"'
            self.fields['correct_answer'].widget = forms.Select(choices=[
                ('', '--- Select ---'),
                ('True', 'True'),
                ('False', 'False')
            ])
        elif self.instance and self.instance.question_type == 'multiple_choice':
            self.fields['correct_answer'].help_text = 'Enter the exact text of the correct option'
    
    def clean(self):
        cleaned_data = super().clean()
        question_type = cleaned_data.get('question_type')
        correct_answer = cleaned_data.get('correct_answer')
        
        if question_type == 'true_false':
            if correct_answer not in ['True', 'False']:
                raise ValidationError('True/False questions must have correct_answer as "True" or "False"')
            # Set options automatically for true/false
            cleaned_data['options'] = ['True', 'False']
        
        elif question_type == 'multiple_choice':
            # Collect options from individual fields
            options = []
            for i in range(1, 5):  # option_1 to option_4
                option_value = cleaned_data.get(f'option_{i}', '').strip()
                if option_value:
                    options.append(option_value)
            
            if len(options) < 2:
                raise ValidationError('Multiple choice questions must have at least 2 options')
            
            if len(options) > 4:
                raise ValidationError('Multiple choice questions cannot have more than 4 options')
            
            if correct_answer and correct_answer not in options:
                raise ValidationError('Correct answer must be exactly one of the provided options')
            
            # IMPORTANT: Set the options in cleaned_data so it's available for saving
            cleaned_data['options'] = options
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Ensure options are set based on cleaned data
        if hasattr(self, 'cleaned_data') and self.cleaned_data.get('options'):
            instance.options = self.cleaned_data['options']
        elif instance.question_type == 'true_false':
            instance.options = ['True', 'False']
        elif instance.question_type == 'multiple_choice':
            # Collect options from form data if not already set
            options = []
            for i in range(1, 5):
                field_name = f'option_{i}'
                if field_name in self.cleaned_data:
                    option_value = self.cleaned_data[field_name].strip()
                    if option_value:
                        options.append(option_value)
            if options:
                instance.options = options
        
        if commit:
            instance.save()
        return instance

    class Media:
        js = ('admin/js/question_form.js',)
        css = {
            'all': ('admin/css/question_form.css',)
        }
