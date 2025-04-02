from django import forms


# Form Classes
# ============
class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=64, widget=forms.TextInput({"class": "m-1 form-control"}))
    password = forms.CharField(max_length=128, widget=forms.PasswordInput({"class": "m-1 form-control"}))
    confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput({"class": "m-1 form-control"}))

    def clean_confirm_password(self):
        # Password and confirm password must match
        if self.cleaned_data["password"] != self.cleaned_data["confirm_password"]:
            raise forms.ValidationError("The passwords must match.")
        

class LoginForm(forms.Form):
    username = forms.CharField(max_length=64, widget=forms.TextInput({"class": "m-1 form-control"}))
    password = forms.CharField(max_length=128, widget=forms.PasswordInput({"class": "m-1 form-control"}))
