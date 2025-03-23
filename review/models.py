from django.db import models

# Create your models here.
class menu(models.Model):
    item_name = models.CharField( max_length=50)
    item_price = models.CharField(max_length=10)



    def __str__(self):
        return self.item_name

class SelectedItems(models.Model):
    items = models.CharField(max_length=255)
    reviews = models.TextField(max_length=255,null=True )
    

    def __str__(self):
        return self.items

    def get_items_list(self):
        return self.items.split(',')
    

class Casestudy(models.Model):
    keywords = models.CharField( max_length=50,null = True)
    review_pista = models.CharField( max_length=500)
    processed = models.CharField( max_length=50,null = True,blank=True)
    sarcasm = models.CharField(  max_length=50,null = True,blank=True)



    def __str__(self):
        return self.review_pista
