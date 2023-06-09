from django.db import models
from django.urls import reverse
import uuid
from datetime import datetime, date
from django.contrib.auth.models import User
# Create your models here.
class Language(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a book genre. Eg-Science Fiction")

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    class Meta:
        ordering = ['last_name', 'first_name']
    def get_absolute_url(self):
        return reverse('catalog:author-detail', args=[str(self.id)])
    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
    def dead_or_not(self):
        if self.date_of_death == None or self.date_of_death > datetime.now():
            return 'Not dead yet!'
        else:
            return str(self.date_of_death)
    dead_or_not.short_description = 'Died?'

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Write a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('catalog:book-detail', args=[str(self.id)])
    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = 'Genre'

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID of this particular book across entire library")
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=100)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text="Book availability")

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)
    def __str__(self):
        return f'{self.book.title} ({self.id})'

    @property
    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)
