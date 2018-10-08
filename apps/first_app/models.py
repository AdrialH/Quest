from __future__ import unicode_literals
from django.db import models
import bcrypt
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        
        if len(postData['firstname']) < 2:
            errors["first_name"] = "First name should be at least 2 characters."
        elif not str.isalpha(postData['firstname']):
            errors["first_name"] = "First name can not contain numbers."
        
        if len(postData['lastname']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters."
        elif not str.isalpha(postData['lastname']):
            errors["last_name"] = "Last name can not contain numbers."
        
        if len(postData['email']) < 1:
            errors["email"] = "Email is required."
        if len(postData['email']) > 40:
            errors["email"] = "Email is required to be coreect format,also no longer than forthy characters."
        elif not EMAIL_REGEX.match(postData['email']): 
            errors["email"] = "Must be valid email."
        elif User.objects.filter(email = postData['email']).exists():
            errors["email"] = "This email exist, please choose another email."
        
        if len(postData['password']) < 8:
            errors['password'] = "Password must be 8 or more characters long."
        elif not str.isalnum(postData['password']):
            errors['password'] = "Password must contain one or more numbers."
        elif len(postData['password']) > 10:
                errors["password"] = "Password can not be more than ten characters."
        elif str.isupper(postData['password']):
            errors['password'] = "Password can not be all caps."
        if not len(postData['passwordconfirmation']) == len(postData['password']):
            errors['passwordconfirmation'] = "Passwords do not match."

        return errors
    
    def login_validator(self, postData):
        
        errors = {}
        
        if len(postData['email']) < 1:
            errors["email"] = "Email can not be empty."
        elif not EMAIL_REGEX.match(postData['email']): 
            errors["email"] = "Must be valid email."
        elif not User.objects.filter(email = postData['email']).exists():
            errors["email"] = "This email does not exist, please register first."
        
        if len(postData['password']) < 1:
            errors["password"] = "Password can not be empty."
        elif len(postData['password']) > 10:
            errors["password"] = "Password can not be more than ten characters."
        if User.objects.filter(email = postData['email']).exists():
            user = User.objects.get(email = postData['email'])
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors['login'] = "Password does not match the one used to create account."
       
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    health = models.IntegerField()
    xp = models.IntegerField()
    gold = models.IntegerField()
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    def __repr__(self):
        return "<User {}|{}{}{}{}>".format(self.id,self.first_name,self.last_name, self.email)

class CharacterManager(models.Manager):
    def Char_validator(self, postData):
        errors = {}
        if Wishlist.objects.filter(item = postData['wish']).exists():
            errors['message'] = "Wish already exist on someone else's list."
        if len(postData['name']) > 10: 
            errors['name'] = "Name is to long, must be less than 10 charaters."
        elif len(postData['name']) < 1:
            errors['name'] = "Your Character must have a name."
        
        if len(postData['name']) < 2:
            errors["name"] = "Name should be at least 2 characters."
        elif not str.isalpha(postData['name']):
            errors["name"] = "Name can not contain numbers."
        return errors
        

class Character(models.Model):
    name = models.CharField(max_length=255)
    health = models.IntegerField()
    xp = models.IntegerField()
    gold = models.IntegerField()
    chars_user = models.ManyToManyField('User', related_name = "users_char")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = CharacterManager()

    def __repr__(self):
        return "<Character {}|{}{}{}>".format(self.id,self.name, self.health, self.xp)


class Image(models.Model):
    img_mon = models.ForeignKey('Monster', related_name = "mon_img")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Image {}|{}>".format(self.id,self.img)


class Shop(models.Model):
    item = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    img = models.ImageField(default='default.png',blank = True)
    items_owned = models.ManyToManyField('User', related_name= "owned_items")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __repr__(self):
        return "<Shop {}|{}{}>".format(self.id,self.item,self.price)


class Monster(models.Model):
    name = models.CharField(max_length=255)
    img = models.ImageField(default='default.png',blank = True)
    health = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __repr__(self):
        return "<Monster {}|{}{}>".format(self.id,self.name,self.health)

        
        
        
        
        
        
