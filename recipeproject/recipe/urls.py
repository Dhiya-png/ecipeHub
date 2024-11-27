from django.urls import path
from .views import*

urlpatterns=[
    path('reg/',registrationview),
    path('log/',loginview),
    path('profile/',userprofile),
    path('profileupdate/',profile_update),
    path('index/',index),
    path('upload/',recipe_uploading),
    path('recipes/', get_recipe, name='recipe_list'),
    path('juice/',get_juice),
    path('shakes/',get_shakes),
    path('desert/',get_desert),
    path('recipe_info/<int:recipe_id>/', get_recipe_info, name='get_recipe_info'),
    path('view_recipe/<int:id1>',view_recipe),
    path('update/<int:id1>',update),
    path('delete/<int:id1>',delete_recipe),
    path('add_to_wish/<int:itemid>',add_to_wishlist),
    path('wishlist/',wishlist)


]