from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class CommentForm(forms.ModelForm):
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'rows':4
    }))
    class Meta:
        model = Comment
        fields = ('content',)


from django import forms
from .models import User


class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
                'class': 'form-control',
            }
        )
    )
    password2 = forms.CharField(
        label='Repite la contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repite la contraseña',
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]
        

    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas no son iguales')


class LoginForm(forms.Form):
    username = forms.CharField(label='',
                               widget=forms.TextInput(attrs={'class': 'inputText', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'inputText', 'placeholder': 'Password'}),
                               label='')