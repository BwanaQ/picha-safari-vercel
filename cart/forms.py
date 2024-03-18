from django import forms

class NewsletterForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Invalid email address")
        return email