from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from PIL import Image

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_student = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)
    image = models.ImageField(default='profile_pics/profile_placeholder.jpg', upload_to='profile_pics')
    hostel = models.CharField(max_length = 100, default = None, null = True, blank = True)
    room = models.CharField(max_length = 4, default = None, null = True, blank = True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Check if an image exists before processing
        if self.image and self.image.path:
            try:
                img = Image.open(self.image.path)

                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.image.path)
            except FileNotFoundError:
                # Log an error or handle the missing file gracefully
                pass
    

class books(models.Model):
    name = models.CharField(max_length = 150)
    author = models.CharField(max_length = 100)
    pub = models.CharField(max_length = 150)
    isbn = models.CharField(max_length = 20)
    copies_total = models.IntegerField()
    copies_available = models.IntegerField()
    cover_img = models.ImageField(default = 'default.jpg', upload_to = 'cover_image')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('lib_book-page', kwargs = {'pk': self.pk})
    
class File(models.Model):
    file = models.FileField(upload_to="excel") 

class library_settings(models.Model):
    late_fees = models.IntegerField()
    issue_period = models.IntegerField()

    def get_absolute_url(self):
        return reverse('lib_paramsDetail', kwargs = {'pk': self.pk})
    
class borrowBook(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    book = models.ForeignKey(books, on_delete=models.CASCADE)
    date_borrow = models.DateTimeField(default = timezone.now)
    date_return = models.DateTimeField(default = timezone.now)
    params = models.ForeignKey(library_settings, on_delete=models.CASCADE)
    
    
class returnBook(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    book = models.ForeignKey(books, on_delete=models.CASCADE)
    is_latefees = models.BooleanField(default=False)
    date_borrow = models.DateTimeField(default = timezone.now)
    date_return = models.DateTimeField(default = timezone.now)
    
class feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=60)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    feedbackImage = models.ImageField(null = True, blank = True, default = None, upload_to='feedbackImage')

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse ('student-home')
    
class rate(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    book = models.ForeignKey(books, on_delete=models.CASCADE)
    rating = models.IntegerField()