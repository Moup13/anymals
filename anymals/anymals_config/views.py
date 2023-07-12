from django.shortcuts import redirect
from django.shortcuts import render

from anymals_config.forms import ProductForm, ReviewForm
from anymals_config.models import Product, Review, News


def index(requests):
    return render(requests, 'index.html')


def services(request):
    return render(request, 'services.html')


def news(requests):
    news_action = News.objects.all()
    return render(requests, 'news.html',{'news_action':news_action})


def full_news(requests,id):
    news_full = News.objects.get(id=id)
    return render(requests, 'full_news.html',{'news_full':news_full})


def discounts(requests):
    return render(requests, 'discounts.html')


def cost_products(request):
    allproducts = Product.objects.all()
    context = {"product": allproducts}


    return render(request, 'cost.html', context)


# def reviews(request,id):
#     posted_rewiews = Reviews.objects.get(id=id)
#
#     if requests.method == "POST":
#         form = ReviewForm(request.POST or None)
#         if form.is_valid():
#             data = form.save(commit=False)
#             data.email = request.POST.get('email')
#             data.name = request.POST.get('name')
#             data.message= request.POST.get('message')
#             data.save()
#             return redirect('/')
#
#     else:
#         form = ReviewForm()
#     return render(request, 'reviews.html.html', {'form': form,'posted_rewiews':posted_rewiews})


def contact(requests):
    return render(requests, 'contact.html')


def detail(request, id):
    product = Product.objects.get(id=id)
    reviews = Review.objects.filter(product=id).order_by("-message")

    context = {
        "prod": product,
        "reviews": reviews,

    }

    return render(request, 'cost_product.html', context)


def add_products(request):
    if request.method == "POST":
        form = ProductForm(request.POST or None)

        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return redirect("/")
    else:
        form = ProductForm()
    return render(request, 'products.html', {"form": form, "controller": "Add Products"})


def edit_products(request, id):
    produs = Product.objects.all()
    produ = Product.objects.get(id=id)
    if request.method == "POST":
        form = ProductForm(request.POST or None, instance=produ)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return redirect("main:detail", id)
    else:
        form = ProductForm(instance=produ)
        return render(request, 'addproducts.html', {'form': form, "controller": "Edit Products"})


def delete_products(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            produ = Product.objects.get(id=id)
            produ.delete()
            return redirect("/")


def add_review(request, id):
    product = Product.objects.get(id=id)
    if request.method == "POST":
        form = ReviewForm(request.POST or None)
        if form.is_valid():
            data = form.save(commit=False)
            data.comment = request.POST["message"]
            data.product = product
            data.save()
            return redirect("anymals_config:detail", id)
    else:
        form = ReviewForm()
    return render(request, 'cost_product.html', {'form': form})


def edit_review(request, product_id, review_id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        review = Review.objects.get(product=product, id=review_id)
        if request.user == review.user:
            if request.method == "POST":
                form = ReviewForm(request.POST, instance=review)
                if form.is_valid():
                    data = form.save(commit=False)
                    if (data.rating > 10) or (data.rating < 0):
                        error = "Out of range. Please select rating from 0 to 10."
                        return render(request, 'main/editreview.html', {'error': error, "form": form})
                    else:
                        data.save()
                        return redirect("main:detail", product_id)
            else:
                form = ReviewForm(instance=review)
            return render(request, 'main/editreview.html', {"form": form})
        else:
            return redirect("main:detail", product_id)
    else:
        return redirect("accounts:login")


def delete_review(request, product_id, review_id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        review = Review.objects.get(product=product, id=review_id)
        if request.user == review.user:
            review.delete()
        return redirect("main:detail", product_id)
    else:
        return redirect("accounts:login")


def about(request):
    return render(request, 'main/about.html')
