from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model



class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='A valid email address, please.', required=True)



    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user








class UserLoginForm(AuthenticationForm):


    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
        label="Username or Email*")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))







class UserUpdateMainForm(forms.ModelForm):


    class Meta:
        model = get_user_model()
        fields = ['username','message', 'notification', 'joined', 'timezone','profiles']


class UserUpdateEmailForm(forms.ModelForm):


    class Meta:
        model = get_user_model()
        fields = ['email']






class UserUpdateOpponents(forms.ModelForm):


    class Meta:
        model = get_user_model()
        fields = ['image','username','color','type']


class UserUpdateMainProfileForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.FileInput)

    class Meta:
        model = get_user_model()
        fields = ['sex','date_of_birth','image']



from django import forms

class UserUpdateRequestForm(forms.ModelForm):


    class Meta:
        model = get_user_model()
        fields = ['color','type','username']








