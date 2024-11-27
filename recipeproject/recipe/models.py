from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# recipe upload

class RecipeModel(models.Model):
    images = models.ImageField(upload_to='recipes/')
    title = models.CharField(max_length=100)
    ingrediance = models.TextField(max_length=3000)
    description = models.CharField(max_length=10000)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    Created_at = models.DateTimeField(auto_now_add=True)


# wishlist
class WishlistModel(models.Model):
    userid =  models.IntegerField()
    items = models.ForeignKey(RecipeModel,on_delete=models.CASCADE)

    