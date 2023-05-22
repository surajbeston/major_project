from django.shortcuts import render
from joblib import load
import csv

import numpy as np

from django.conf import settings

from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import generics, mixins, status
from rest_framework.decorators import api_view


from .forms import SearchForm



from .serializers import CategorizeSerializer
from .models  import Product

# text_clf = load("/home/badu/workspace/collegeProject/ecommerce-product-classifier/classification_model1.joblib")
# encoder = load("/home/badu/workspace/collegeProject/ecommerce-product-classifier/category_encoder1.joblib")
text_clf = load( settings.BASE_DIR / "classification_model_sdg1.joblib")
encoder = load( settings.BASE_DIR / "category_encoder2.joblib")

brand_clf = load(settings.BASE_DIR / "gadgets_brand_model.joblib")
brand_encoder = load(settings.BASE_DIR / "gadgets_brand_encoder.joblib")


categories_prices = {}

def load_data():
    with open(settings.BASE_DIR / "price_data.csv", 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            try:
                category = str(row[1])
                price = float(row[2])
            except:
                continue

            try:
                categories_prices[category].append(price)
            except KeyError:
                categories_prices[category] = [price]

load_data()

def home(request):
    name = request.GET.get("name", None)
    description = request.GET.get("description", None)

    if name and description:
        classify_text = name + description
    elif name:
        classify_text = name
    elif description:
        classify_text = description
    else:
        return render(request , "home.html", {})

    categories = encoder.inverse_transform([text_clf.predict([classify_text])])
    brands = None
    if categories:
        category = categories[0][0]
        if "Electronic Accessories" == category and name:
            brands = brand_encoder.inverse_transform([brand_clf.predict([name])])
            if brands:
                brands = brands[0]
        category_prices = np.array(categories_prices[category])
        quantiles = {}
        quantiles["first"] = np.quantile(category_prices, 0.20)
        quantiles["second"] = np.quantile(category_prices, 0.40)
        quantiles["third"] = np.quantile(category_prices, 0.60)
        quantiles["fourth"] = np.quantile(category_prices, 0.80)
        quantiles["fifth"] = np.quantile(category_prices, 1.00)

        given_price = request.GET.get("price", None)
        if given_price:
            given_price = float(given_price)
            if given_price <= quantiles["first"]:
                quantiles["this"] = "Very Low"
            elif given_price <= quantiles["second"]:
                quantiles["this"] = "Low"
            elif given_price <= quantiles["third"]:
                quantiles["this"] = "Medium"
            elif given_price <= quantiles["fourth"]:
                quantiles["this"] = "High"
            else:
                quantiles["this"] = "Very High"

    return render(request , "home.html",  {"categories": categories, "brand": brands, "quantiles": quantiles})


category_clf = load( settings.BASE_DIR / f"models/CategoryClassifier.joblib")
category_encoder = load( settings.BASE_DIR / f"encoders/CategoryEncoder.joblib")

@swagger_auto_schema(request_body=CategorizeSerializer, method = 'post')
@api_view(['GET', 'POST'])
def get_cateogry(request):
    serializer = CategorizeSerializer(data = request.data)
    if serializer.is_valid():
        title = serializer.data.get("title", None)
        description = serializer.data.get("description", None)

        if title and description:
            classify_text = str(title) + " " + str(description)
        elif title:
            classify_text = str(title)
        elif description:
            classify_text = str(description)


        categories = category_encoder.inverse_transform([category_clf.predict([classify_text])])
        if categories:
            category = categories[0][0]
            sub_category_clf = load( settings.BASE_DIR / f"models/{category}.joblib")
            sub_category_encoder = load( settings.BASE_DIR / f"encoders/{category}.joblib")

            sub_categories = sub_category_encoder.inverse_transform([sub_category_clf.predict([classify_text])])
            if sub_categories:
                sub_category = sub_categories[0][0]
                if sub_category == "Mobile & Tablet Accessories":
                    brand = brand_encoder.inverse_transform([brand_clf.predict([classify_text])])
                    return Response({"sub_category": sub_categories[0][0], "category": category, "brand": brand[0][0]})
                return Response({"sub_category": sub_categories[0][0], "category": category})
            else:
                return Response({"category": category, "sub_category": None})
        return Response({"message": "Cannot categorize"}, status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

import re 
def remove_tags(string):
    result = re.sub('<.*?>','',string)
    return result

def search(request):
    if request.method == 'POST':
        query = request.POST.get("query", None)
        products = []
        if query:
            products = Product.objects.filter(name__search= query)
            
        return render( request,"search.html", {"query": query, "products": products})
    if request.method == 'GET':
        category = request.GET.get('category', None)
        sub_category = request.GET.get('sub_category', None)
        brand = request.GET.get('brand', None)

        products = []

        if category:
            products = Product.objects.filter(category = category)
        if sub_category:
            products = Product.objects.filter(sub_category__search = sub_category)
        if brand:
            products = Product.objects.filter(brand = brand)
        return render( request,"search.html", {'produts': products})
    
def filter_by_category(request, category_slug):
    products = Product.objects.filter(category_slug = category_slug)
    return render(request, "search.html", {'products': products})

def filter_by_sub_category(request, sub_category_slug):
    products = Product.objects.filter(sub_category_slug = sub_category_slug)
    return render(request, "search.html", {'products': products})

def filter_by_brand(request, brand):
    products = Product.objects.filter(brand = brand)
    return render(request, "search.html", {'products': products})