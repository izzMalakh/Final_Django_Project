from email import message
from email.policy import default
from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class CustomerManager(models.Manager):
    def customer_validator(self, postData):
        errors = {}
        if len(postData['name']) < 5:
            errors['name'] = "The Name Should be atleast 5 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        
        PHONE_REGEX = re.compile(r'^05(9[987542]|6[982])\d{6}$')
        if not PHONE_REGEX.match(postData['phoneNumber'] ):
            errors['phoneNumber'] = "Invalid phone number; number should start: 056 or 059 and must be 10 numbers."
        return errors

    
    

class MealManager(models.Manager):
    def Meal_validator(self, postData):
        errors = {}
        if len(postData['mealName']) == 0:
            errors['mealName'] = "The Name is required "
        if postData['mealType'] == "none":
            errors['mealType'] = "Meal type is required!"
        if len(postData['price']) == 0:
            errors['price'] = "Price is required!"
        return errors

class EmployeeManager(models.Manager):
    def Employee_validator(self, postData):
        errors = {}
        if len(postData['firstname']) < 2:
            errors['first_name'] = "The first name must be atleast 2 characters" 
        if len(postData['lastname']) < 2:
            errors['last_name'] = "The last name must be atleast 2 characters" 
        if len(postData['idnumber']) == 0:
            errors['id'] = "ID Number is required"
        
        PHONE_REGEX = re.compile(r'^05(9[987542]|6[982])\d{6}$')
        if not PHONE_REGEX.match(postData['phone'] ):
            errors['phone_number'] = "Invalid phone number; number should start: 056 or 059 and must be 10 numbers."
        return errors

    def edit_validator(self, postData):
        errors = {}
        if len(postData['editfirstname']) < 2:
            errors["firstname"] = "The first name must be atleast 2 characters"
        if len(postData['editlastname']) < 2:
            errors["lastname"] = "The last name must be atleast 2 characters" 
        if len(postData['editidnumber']) == 0:
            errors["id"] = "ID Number is required"
        PHONE_REGEX = re.compile(r'^5(9[987542]|6[982])\d{6}$')
        if not PHONE_REGEX.match(postData['editphone'] ):
            errors['phonenumber'] = "Invalid phone number; number should start: 056 or 059 and must be 10 numbers."
        
        return errors

class SoftDeleteModel(models.Model):

    is_deleted = models.BooleanField(default=False)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True

class CustomerManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        
        if len(postData['name']) < 2:
            errors["name"] = "First name should be at least 2 characters"
        PHONE_REGEX = re.compile(r'^05(9[987542]|6[982])\d{6}$')         
        if not PHONE_REGEX.match(postData['phone_number'] ):           
            errors['phone_number'] = "Invalid phone number; number should start: 056 or 059 and must be 10 numbers."

        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        
        if len(postData['email']) == 0:
            errors["email"] = "email is empty!"

        users= Customer.objects.all()
        for user in users:
            if user.email == postData['email']:
                errors['email']="this email already selected before in our database"
        
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid Email Address!"
            
        return errors
class CustomerManager(models.Manager):
    def editProfile_validator(self, postData):
        errors = {}
        if len(postData['EditName']) < 5:
            errors['name'] = "The Name Should be atleast 5 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['EditEmail']):
            errors['email'] = "Invalid email address!"
        
        PHONE_REGEX = re.compile(r'^05(9[987542]|6[982])\d{6}$')
        if not PHONE_REGEX.match(postData['EditPhone'] ):
            errors['phoneNumber'] = "Invalid phone number; number should start: 056 or 059 and must be 10 numbers."
        return errors

class ReservationManager(models.Manager):
    def Reservation_validator(self, postData):
        errors ={}
        if len(postData['number_of_persons']) == 0:
            errors['number_of_persons'] = "Attendees number is empty"
        elif int(postData['number_of_persons']) not in range (2,20) :
            errors['number_of_persons'] = "Attendees number must not excseed 20 and not less than 2"
        if len(postData['numberofHours']) == 0:
            errors['number_of_hours'] = "Number of Hours is empty"
        elif int(postData['numberofHours']) not in range (1,24) :
            errors['number_of_hours'] = "Allowed hours to make a reservaetion is alteast 1 hour and not exceed 24 hours"
        return errors
        
class Employee(SoftDeleteModel):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    id_number = models.IntegerField()
    phone_number = models.IntegerField()
    working_hours = models.IntegerField()
    salary = models.IntegerField()
    age = models.IntegerField()
    position = models.CharField(max_length = 255)
    started_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = EmployeeManager()

class Meal(models.Model):
    name = models.CharField(max_length = 255)
    type = models.CharField(max_length = 255)
    description = models.CharField(max_length=255)
    count = models.IntegerField(default=0)
    price = models.IntegerField()
    image=models.ImageField(upload_to='images',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = MealManager()

class Customer(models.Model):
    name = models.CharField(max_length = 255)
    phone_number = models.IntegerField()
    password = models.CharField(max_length=255)
    email = models.CharField(max_length = 255)
    address = models.CharField(max_length = 255)
    count1 = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = CustomerManager()

class Order(models.Model):
    process = models.BooleanField(default = False)
    customer = models.ForeignKey(Customer, related_name = "orders", on_delete = models.DO_NOTHING)
    final_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Cart(models.Model):
    meal  = models.ForeignKey(Meal, related_name = "ordered", on_delete=models.PROTECT )
    quantity = models.IntegerField()
    customer = models.ForeignKey(Customer, related_name = "orderPerItem", on_delete = models.DO_NOTHING)
    order  = models.ForeignKey(Order, related_name = "cart_item", on_delete = models.CASCADE )
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    
class Reservation(models.Model):
    number_of_persons =  models.IntegerField()
    date_time = models.CharField(max_length = 255)
    number_of_hours = models.IntegerField()
    occassion = models.CharField(max_length = 255)
    message = models.CharField(max_length = 255)
    cost = models.IntegerField()
    customer = models.ForeignKey(Customer , related_name = "reserved_event", on_delete = models.DO_NOTHING)
    status=models.CharField(max_length = 255,default="notyet")
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ReservationManager()

class Special(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price =  models.IntegerField()
    customer_order = models.ManyToManyField(Customer, related_name="specail_order")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Review(models.Model):
    Message = models.CharField(max_length=200)
    customer_order = models.ManyToManyField(Customer, related_name="review_message")
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)