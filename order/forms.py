from django import forms
from order.models import UserInfo,Member
from django.core.exceptions import ValidationError

class UserInfoForm(forms.ModelForm):
    class Meta: #是內部類別,用來配置模型額外的選項,非必要性,要製定模型的行為或結構時,才採用之
        model=UserInfo
        fields="__all__"
        #fields=['username','password']



# class MemberForm(forms.ModelForm):
#     class Meta:
#         model=Member        
#         fields=('email','pwd','uname')
#         widgets={
#             'email':forms.EmailInput(attrs={'placeholder':'Enter Email'}),
#             'pwd':forms.PasswordInput(attrs={'placeholder':'Enter Password'}),
#             'uname':forms.TextInput(attrs={'placeholder':'Enter Name','value':''}),
#         }

# class MemberLogin(forms.ModelForm):
#     class Meta:
#         model=Member        
#         fields=('email','pwd')
#         widgets={
#             'email':forms.EmailInput(attrs={'placeholder':'Enter Email'}),
#             'pwd':forms.PasswordInput(attrs={'placeholder':'Enter Password'}),         
#         }


class MemberForm(forms.ModelForm):
    class Meta:
        model=Member        
        fields=('email','pwd','uname')
        widgets={
            'email':forms.EmailInput(attrs={'placeholder':'Enter Email'}),
            'pwd':forms.PasswordInput(attrs={'placeholder':'Enter Password'}),
            'uname':forms.TextInput(attrs={'placeholder':'Enter Name','value':''}),
        }

    def clean_password(self):
        password=self.cleaned_data.get('pwd')   #取得原始的密碼
        if not any(char.isdigit() for char in password):
            raise ValidationError('密碼要包含數字!!')
        if not any(char.islower() for char in password):
            raise ValidationError('密碼要包含小寫的字母!!')
        if not any(char.isupper() for char in password):
            raise ValidationError('密碼要包含大寫的字母!!')
        if len(password) < 8:
            raise ValidationError('密碼的長度不可小於8個字!!')
        return password

       
class MemberLogin(forms.ModelForm):
    class Meta:
        model=Member        
        fields=('email','pwd')
        widgets={
            'email':forms.EmailInput(attrs={'placeholder':'Enter Email'}),
            'pwd':forms.PasswordInput(attrs={'placeholder':'Enter Password'}),         
        }


#產品與訂單查詢
class ProductSearchForm(forms.Form):
    pid=forms.IntegerField(label="產品編號", min_value=1 )
