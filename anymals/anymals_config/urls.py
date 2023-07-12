from django.urls import path



from anymals_config.views import services, index, detail, add_products, edit_products, delete_products, add_review, \
    edit_review, delete_review, cost_products, full_news

from anymals_config.views import news

from anymals_config.views import discounts



from anymals_config.views import contact

app_name = 'anymals_config'
urlpatterns = [
    path('', index, name = 'index'),
    path('contact/', contact, name = 'contact'),
    path('cost/', cost_products, name='cost'),
    path('news/', news, name = 'news'),
    path('news/<int:id>/', full_news, name='full_news'),
    path('cost/<int:id>/',detail,name="detail"),
    path('addproducts/',add_products,name="add_products"),
    path('editproducts/<int:id>/',edit_products,name="edit_products"),
    path('deleteproducts/<int:id>/',delete_products,name="delete_products"),
    path('addreview/<int:id>/',add_review,name="add_review"),
    path('editreview/<int:product_id>/<int:review_id>',edit_review,name="edit_review"),
    path('deletereview/<int:product_id>/<int:review_id>',delete_review,name="delete_review"),


]


