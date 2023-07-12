from django import forms

from anymals_config.models import Review, Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name','image','cost','description')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['email', 'name', 'message']
