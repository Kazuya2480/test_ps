from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta 


class StudentExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    enrollment = models.CharField(max_length=40)
    def __str__(self):
        return self.user.first_name+'['+str(self.enrollment)+']'
    @property
    def get_name(self):
        return self.user.first_name
    @property
    def getuserid(self):
        return self.user.id


class Book(models.Model):
    catchoice = [
        ('総記', '総記'),
        ('哲学', '哲学'),
        ('歴史', '歴史'),
        ('社会科学', '社会科学'),
        ('自然科学', '自然科学'),
        ('技術・工学', '技術・工学'),
        ('産業', '産業'),
        ('芸術・美術', '芸術・美術'),
        ('言語', '言語'),
        ('文学','文学')
        ]
    isbn=models.PositiveIntegerField()
    name=models.CharField(max_length=30)
    author=models.CharField(max_length=40)
    category=models.CharField(max_length=30,choices=catchoice,default='総記')
    publisher=models.CharField(max_length=60)
    publisheddate=models.DateField()
    image=models.ImageField(upload_to='image/')
    version=models.CharField(max_length=30)
    place=models.CharField(max_length=40)

    def __str__(self):
  
        return str(self.name)+"["+str(self.isbn)+']'
    
    def get_rating(self):
        total = sum(int(review['stars']) for review in self.reviews.values())

        if self.reviews.count() > 0:
            return total / self.reviews.count()
        else:
            return 0
    
    
def get_expiry():
    return datetime.today() + timedelta(days=15)
class IssuedBook(models.Model):
    #moved this in forms.py
    #enrollment=[(student.enrollment,str(student.get_name)+' ['+str(student.enrollment)+']') for student in StudentExtra.objects.all()]
    enrollment=models.CharField(max_length=30)
    #isbn=[(str(book.isbn),book.name+' ['+str(book.isbn)+']') for book in Book.objects.all()]
    isbn=models.CharField(max_length=30)
    issuedate=models.DateField(auto_now=True)
    expirydate=models.DateField(default=get_expiry)
    def __str__(self):
        return self.enrollment
    

class Carts(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )

    class Meta:
        db_table = 'carts'

class CartItemsManager(models.Manager):

    def save_item(self, book_id, book_isbn, cart):
        c = self.model(book_id=book_id, book_isbn=book_isbn, cart=cart)
        c.save()

class CartItems(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE
    )
    cart = models.ForeignKey(
        Carts, on_delete=models.CASCADE
    )
    book_isbn = models.CharField(max_length=30)
    date = models.DateField(auto_now=True)

    objects = CartItemsManager()


    class Meta:
        db_table = 'cart_items'
        unique_together = [['book', 'cart']]

class BookReview(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)

    content = models.TextField(blank=True, null=True)
    stars = models.IntegerField()

    data_added = models.DateTimeField(auto_now_add=True)

class BookHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


