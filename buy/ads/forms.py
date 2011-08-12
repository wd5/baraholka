# -*- coding: utf-8 -*-
from django import forms
from buy.ads.models import Category
from django.forms.util import ErrorList
from django.contrib.auth.models import User

class SimpleSearchForm(forms.Form):
    category = forms.ChoiceField(label="")
    text = forms.CharField(label="")
    
    def __init__(self, *args, **kwargs):
	super(SimpleSearchForm, self).__init__(*args, **kwargs)
	cat_list=[(cat.id, cat.name) for cat in Category.objects.all().order_by('name')]
	self.fields['category'].choices = cat_list
	
class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='Комменть сюда')

class AddForm(forms.Form):
    name = forms.CharField(label="Название",max_length=100,widget=forms.TextInput(attrs={'size':55}))
    def clean_name(self):
	name = self.cleaned_data['name']
	if len(name.strip()) == 0:
	    self._errors['name'] = ErrorList([u"Тема не может быть пустой!"])
	return name.strip()
    
    text = forms.CharField(widget=forms.Textarea(), label="Описание", required=False)
    category = forms.ChoiceField(label="Категория")
    price = forms.CharField(label="Цена", required=False, max_length=32)
    place = forms.CharField(label="Место", required=False, max_length=128)
    #image_main = forms.FileField(label="Рисунок")
    
    def __init__(self, *args, **kwargs):
	super(AddForm, self).__init__(*args, **kwargs)
	cat_list=[(cat.id, cat.name) for cat in Category.objects.all().order_by('name')]
	self.fields['category'].choices = cat_list
	
class PassChangeForm(forms.Form):
    old_pass = forms.CharField(label="Старый пароль")
    new_pass = forms.CharField(label="Новый пароль")
    renew_pass = forms.CharField(label="Повторите пароль")
    
    def clean_new_pass(self):
	passw = self.cleaned_data['new_pass']
	if len(passw) < 5:
	    raise forms.ValidationError("Пароль должен быть длиннее 4 символов")
	return passw
		
    def clean(self):
	cleaned_data = self.cleaned_data
	new_pass = cleaned_data.get('new_pass')
	renew_pass = cleaned_data.get('renew_pass')
	
	if new_pass and renew_pass and new_pass != renew_pass:
	    msg = u"Пароли не совпадают."
	    self._errors['new_pass'] = ErrorList([msg])
	    self._errors['renew_pass'] = ErrorList([msg])
	    
	    del cleaned_data['new_pass']
	    del cleaned_data['renew_pass']
	    
	return cleaned_data
	
class RegForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=16)
    passw = forms.CharField(label='Пароль', max_length=64, widget = forms.PasswordInput())
    passw_again = forms.CharField(label='Пароль еще раз', max_length=64, widget = forms.PasswordInput())
    fullname = forms.CharField(label='Полное имя', max_length=128, required=False)
    email = forms.EmailField(label='E-mail адрес')
    info = forms.CharField(label='Дополнительная информация (контакты)',widget=forms.Textarea(), required=False)
    
    def clean_username(self):
	username = self.cleaned_data['username']
	if len(User.objects.filter(username=username)) != 0:
	    self._errors['username'] = ErrorList(["Такое имя пользователя уже занято"])
	return username
	
    
    def clean_passw(self):
	passwd = self.cleaned_data['passw']
	if len(passwd) < 5:
	    #raise forms.ValidationError("Пароль должен быть длиннее 4 символов")
	    self._errors['passw'] = ErrorList(["Пароль должен быть длиннее 4 символов"])
	return passwd
	
    def clean(self):
	cleaned_data = self.cleaned_data
	passwd = cleaned_data['passw']
	passwd_again = cleaned_data['passw_again']
	if passwd and passwd_again and passwd != passwd_again:
	    msg = u"Пароли не совпадают."
	    self._errors['passw'] = ErrorList([msg])
	    self._errors['passw_again'] = ErrorList([msg])
	    
	    del cleaned_data['passw']
	    del cleaned_data['passw_again']
	
	return cleaned_data