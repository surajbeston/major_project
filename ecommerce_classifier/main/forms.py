from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(max_length= 100)
    category = forms.ChoiceField(choices = [('Groceries', 'Groceries'), ('G-Bar', 'G-Bar'), ('Electronics', 'Electronics'), ('Electronic Accessories', 'Electronic Accessories'), ('Fashion', 'Fashion'), ('Beauty & Health', 'Beauty & Health'), ('TV & Home Appliances', 'TV & Home Appliances'), ('Home & Lifestyle', 'Home & Lifestyle'), ('Fitness', 'Fitness')])

