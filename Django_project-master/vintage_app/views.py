from contextlib import ContextDecorator
from email.headerregistry import Address
from multiprocessing import context
from django.shortcuts import render,redirect
from .models import * 
from django.contrib import messages
import bcrypt, random
import json
from django.http import JsonResponse
import os
def method(request):
    request.session['admin'] = "user"
    softdrinks=Meal.objects.filter(type="softdrinks") 
    hotdrinks=Meal.objects.filter(type="hotdrinks") 
    Sparklings=Meal.objects.filter(type="Sparklings") 
    IcedDrinks=Meal.objects.filter(type="iced") 
    Drinks=Meal.objects.filter(type="drinks")
    Milkshakes=Meal.objects.filter(type="milkshakes")
    Cocktails=Meal.objects.filter(type="cocktails")
    freshJuice=Meal.objects.filter(type="freshJuice")
    Starters=Meal.objects.filter(type="Starter")
    Salad=Meal.objects.filter(type="salad")
    Main=Meal.objects.filter(type="mainMeals")
    Chinese=Meal.objects.filter(type="Chinese")
    Sandwishes=Meal.objects.filter(type="Sandwishes")
    breakfast=Meal.objects.filter(type="breakfast")

    re = Reservation.objects.all()
    specialty= Meal.objects.all().order_by('-count')
    context={
        'almeals': Meal.objects.all(),
        'softdrinks':softdrinks,
        'hotdrinks':hotdrinks,
        'sparklings':Sparklings,
        'IcedDrinks':IcedDrinks,
        'drinks':Drinks,
        'milkshakes':Milkshakes,
        'cocktails':Cocktails,
        'freshJuice':freshJuice,
        'Starter':Starters,
        'salad':Salad,
        'mainMeals':Main,
        'Chinese':Chinese,
        'Sandwishes':Sandwishes,
        'breakfast':breakfast,
        're':re,
        'specialty' : specialty,
    }
    return render(request, "home.html",context)

def login(request):
    return render(request, "login.html")
def userlogin(request):
    user = Customer.objects.filter(email=request.POST['login_email'])
    if user: 
        logged_user=user[0]
        if bcrypt.checkpw(request.POST['login_password'].encode(), logged_user.password.encode()):
            user = Customer.objects.get(email=request.POST['login_email'])
            request.session['name_of_user'] = user.name
            request.session['id_of_user'] = user.id
            return redirect('/')
        messages.error(request, "Invalid email or password", extra_tags="wrong")
        return redirect('/login')
    messages.error(request, "Invalid email or password", extra_tags="wrong")
    return redirect('/login')

def signup(request):
    return render(request, "reg.html")

def newuserRegistration(request):
    errors = Customer.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            print(errors)
        return redirect('/signup')
    fname= request.POST["name"]
    email= request.POST["email"]
    password = request.POST['password']
    phone_number = request.POST['phone_number']
    address = request.POST['adress']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = Customer.objects.create(name=fname, email=email, password=pw_hash, phone_number=phone_number,address=address)
    user.save()
    messages.success(request, "Thank you! account successfully registered, Please login", extra_tags="suc")
    return redirect('/signup')
def logout(request):
    request.session.delete()
    return redirect('/')

def writePassword(request):
    return render(request, "adminpage.html")

def confirmAdminPassword(request):
    
    if request.POST['passadmin'] == "admin0000":
        request.session['admin'] = "Joseph"
        return redirect("/adminDashboard")
    else:
        messages.error(request, "Invalid password", extra_tags="invalid")
        return redirect("/admin")

        
    

def ShowadminDashboard(request):
    if request.session['admin'] == "Joseph":
        context = {
            'employee'  :  Employee.objects.all(),
            'meal'      :  Meal.objects.all(),
            'special'   :  Special.objects.all(),
            'reviews'   :  Review.objects.all(),
            'reservation': Reservation.objects.all(),
            
        }
        return render(request, "adminDashboard.html",context)

def showallUsers(request):
    if request.session['admin'] == "Joseph":
        context={
            'users':Customer.objects.all()
        }
        return render(request, "allusers.html",context)

def showallEmployees(request):
    if request.session['admin'] == "Joseph":
        context={
            'allemployees':Employee.objects.all()
        }
    if 'firstname' in request.POST:
        qs = Employee.objects.filter(title__icontains=request.POST.get('firstname'))
        titles = list()
        for e in qs:
            titles.append(e.title)
        titles = [e.title for e in qs]
        return JsonResponse(titles, safe=False)
    return render(request, "allemployees.html",context)

def addMenu(request):
    print("izz")
    errors = Meal.objects.Meal_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/adminDashboard") 
    type = request.POST['mealType']
    price = request.POST['price']
    mealName = request.POST['mealName']
    Pimage=request.FILES['image']
    desc = request.POST['description']
    Meal.objects.create(name = mealName , price = price , description = desc , type = type, image=Pimage)
    return redirect("/adminDashboard")

def addemployee(request):
    errors = Employee.objects.Employee_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/showallEmployees')
    first_name = request.POST['firstname']
    last_name = request.POST['lastname']
    id_number = request.POST['idnumber']
    phone_number = request.POST['phone']
    working_hours = request.POST['workinghours']
    salary = int(working_hours)*10
    age = request.POST['age']
    position = request.POST['positionselect']
    started_date = request.POST['started_date']
    current_situation = request.POST['currentsituation']
    Employee.objects.create(first_name=first_name,last_name=last_name,id_number=id_number,phone_number=phone_number,working_hours=working_hours,salary=salary,age=age,position=position,started_date=started_date,current_situation=current_situation)
    return redirect('/showallEmployees')

def deleteEmployee(request,id):
    em = Employee.objects.get(id=id)
    em.soft_delete()
    return redirect('/showallEmployees')
def pre(request):
    context={
        'em' : Employee.objects.all(),
    }
    return render(request,"all.html",context)
def restore(request,id):
    emp= Employee.objects.get(id=id)
    emp.restore()
    emp.save()
    return redirect('/viewPreEmployee')

def editEmployee(request,id):
    context={
        'em':Employee.objects.get(id=id)
    }
    return render(request,"editemployeePage.html",context)
    
def updateEmployeee(request,id):
    errors = Employee.objects.edit_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        
        return redirect('/editEmployee/'+ str(id))
    else:
        emp = Employee.objects.get(id=id)
        emp.first_name = request.POST['editfirstname']
        emp.last_name = request.POST['editlastname']
        emp.id_number = request.POST['editidnumber']
        emp.phone_number = request.POST['editphone']
        emp.working_hours = request.POST['editworkinghours']
        emp.salary = request.POST['editsalary']
        emp.age = request.POST['editage']
        emp.started_date = request.POST['editstarted_date']
        emp.current_situation = request.POST['editcurrentsituation']
        emp.position = request.POST['editpositionselect']
        emp.save()
        messages.success(request, "Updated successfully")
        return redirect('/editEmployee/'+ str(id))

def showEmployee(request,id):
    emp= Employee.objects.get(id=id)
    context={
        'emp': Employee.objects.get(id=id),
        'empm': emp.salary*30
    }
    return render(request,"showDetailsEmployee.html",context)

def bookTable(request):
    errors = Reservation.objects.Reservation_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value ,extra_tags=key)
        return redirect('/#book-a-table')
    numberPersons = request.POST['number_of_persons']
    date = request.POST['date']
    numberHours = request.POST['numberofHours']
    occassion = request.POST['occassion']
    message =request.POST['message']
    cost = int(numberHours)+int(numberPersons)*35
    customer = Customer.objects.get(id=request.session['id_of_user'])
    Reservation.objects.create(number_of_persons = numberPersons, date_time = date, number_of_hours= numberHours,
    occassion = occassion,message=message , cost = cost, customer =  customer)
    messages.success(request, "Your Reservation Send Succefully wait for call", extra_tags="succc")
    return redirect('/#book-a-table')

def ordernow(request):
    softdrinks=Meal.objects.filter(type="softdrinks") 
    hotdrinks=Meal.objects.filter(type="hotdrinks") 
    Sparklings=Meal.objects.filter(type="Sparklings") 
    IcedDrinks=Meal.objects.filter(type="iced") 
    Drinks=Meal.objects.filter(type="drinks")
    Milkshakes=Meal.objects.filter(type="milkshakes")
    Cocktails=Meal.objects.filter(type="cocktails")
    freshJuice=Meal.objects.filter(type="freshJuice")
    Starters=Meal.objects.filter(type="Starter")
    Salad=Meal.objects.filter(type="salad")
    Main=Meal.objects.filter(type="mainMeals")
    Chinese=Meal.objects.filter(type="Chinese")
    Sandwishes=Meal.objects.filter(type="Sandwishes")
    breakfast=Meal.objects.filter(type="breakfast")
    

    context={
        'almeals': Meal.objects.all(),
        'softdrinks':softdrinks,
        'hotdrinks':hotdrinks,
        'sparklings':Sparklings,
        'IcedDrinks':IcedDrinks,
        'drinks':Drinks,
        'milkshakes':Milkshakes,
        'cocktails':Cocktails,
        'freshJuice':freshJuice,
        'Starter':Starters,
        'salad':Salad,
        'mainMeals':Main,
        'Chinese':Chinese,
        'Sandwishes':Sandwishes,
        'breakfast':breakfast
    }

    if 'price' not in request.session:
        request.session['price'] = 0
    
    customer = Customer.objects.get(id = int(request.session['id_of_user']))
    final_price = int(request.session['price'])
    order = Order.objects.create(customer = customer, final_price = final_price)
    
    request.session['orderId'] = order.id
    return render(request, "ordernow.html",context)

def addToCart(request,id):
    meal1 = Meal.objects.get(id = id)
    quantity = request.POST['quantity']
    print(quantity)
    request.session['price'] = int(quantity) * int(meal1.price) + int(request.session['price'])
    order = Order.objects.get(id = int(request.session['orderId']))
    meal1.count+=int(quantity)
    meal1.save()
    order.final_price = int(quantity) * int(meal1.price)
    order.save()
    print(request.session['price'])
    customer = Customer.objects.get(id = int(request.session['id_of_user']))
    Cart.objects.create(meal = meal1 , quantity = quantity, customer = customer , order = Order.objects.get(id=int(request.session['orderId'])))
    return redirect("/ordernow")

def completeOrder(request):
    if 'orderId' in request.session:
        final_price = request.session['price']
        order = Order.objects.get(id=int(request.session['orderId']))
        order.final_price = final_price
        order.save()
        context ={
            'order': Order.objects.last(),
        }
        customer = Customer.objects.get(id = int(request.session['id_of_user']))
        print("hi")
        customer.count1 +=1
        customer.save()
        print(customer.count1)
        print(customer.name)
        customer.save()
        request.session['price'] = 0
        del request.session['orderId']
        return render(request, 'suc.html',context)
    return redirect('/ordernow')

def showallOrders(request):
    context={
        'orders':Order.objects.all(),
        'customers':Customer.objects.all(),
        'carts':Cart.objects.all()
    }
    return render(request,"showallOrders.html",context)

def processTrue(request,id):
    cart = Cart.objects.get(id=id)
    order = cart.order

    if order.process == False:
        order.process = "True"
    elif order.process == True:
        order.process = "False"
    order.save()
    return redirect("/showallOrders")
def destroyOrder(request,id):
    cart = Cart.objects.get(id=id)
    order = cart.order
    order.delete()
    return redirect("/showallOrders")

def error(request):
    messages.error(request, "please log in to use this feture", extra_tags="wrong")
    return redirect("/")

def sendmessage(request,id):
    message = request.POST['message']
    Review.objects.create(Message=message)
    
    messages.success(request, "Your Message Send Succefully", extra_tags="succ")
    return redirect("/#testimonials")

def deletemessage(request,id):
    mes = Review.objects.get(id=id)
    mes.delete()
    return redirect("/adminDashboard")

def ShowmessageReservation(request,id):
    messid= Reservation.objects.get(id=id)
    context={
        'messid': messid
    }
    return render(request, "showReservationDetails.html",context)

def toEditMenu(request):
    softdrinks=Meal.objects.filter(type="softdrinks") 
    hotdrinks=Meal.objects.filter(type="hotdrinks") 
    Sparklings=Meal.objects.filter(type="Sparklings") 
    IcedDrinks=Meal.objects.filter(type="iced") 
    Drinks=Meal.objects.filter(type="drinks")
    Milkshakes=Meal.objects.filter(type="milkshakes")
    Cocktails=Meal.objects.filter(type="cocktails")
    freshJuice=Meal.objects.filter(type="freshJuice")
    Starters=Meal.objects.filter(type="Starter")
    Salad=Meal.objects.filter(type="salad")
    Main=Meal.objects.filter(type="mainMeals")
    Chinese=Meal.objects.filter(type="Chinese")
    Sandwishes=Meal.objects.filter(type="Sandwishes")
    breakfast=Meal.objects.filter(type="breakfast")
    context={
        'almeals': Meal.objects.all(),
        'softdrinks':softdrinks,
        'hotdrinks':hotdrinks,
        'sparklings':Sparklings,
        'IcedDrinks':IcedDrinks,
        'drinks':Drinks,
        'milkshakes':Milkshakes,
        'cocktails':Cocktails,
        'freshJuice':freshJuice,
        'Starter':Starters,
        'salad':Salad,
        'mainMeals':Main,
        'Chinese':Chinese,
        'Sandwishes':Sandwishes,
        'breakfast':breakfast
    }
    return render(request,"toEditMenu.html",context)

def EditAtMenu(request,id):
    
    # errors = Show.objects.show_form_validator(request.POST)
    # if len(errors) > 0:
    #     for key, value in errors.items():
    #         messages.error(request, value ,extra_tags=key)
    meal = Meal.objects.get(id=id)
    #     return redirect('/edit/'+str(id))
    if request.method == "POST":
        
        meal.name = request.POST['editmeal']
        meal.description = request.POST['editdiscription']
        meal.price = request.POST['editprice']
        
        
        
        meal.save()
        return redirect("/toEditMenu")

def deleteFromMenu(request,id):
    meal = Meal.objects.get(id=id)
    meal.delete()

    return redirect("/toEditMenu")

def AcceptEvent(request,id):
    m = Reservation.objects.get(id=id)
    m.status = "True"
    m.save()
    return redirect("/adminDashboard")
def RefucedEvent(request,id):
    m = Reservation.objects.get(id=id)
    m.status = "False"
    m.save()
    return redirect("/adminDashboard")
def deleteEvent(request,id):
    m = Reservation.objects.get(id=id)
    m.delete()
    return redirect("/adminDashboard")
def EditEstimatedCost(request,id):
    m = Reservation.objects.get(id=id)
    m.change_cost = True
    m.cost = request.POST['editcost']
    m.save()
    return redirect("/adminDashboard")

def showReports(request):
    if request.session['admin'] == "Joseph":
        context={
            'meal': Meal.objects.all().order_by('-count'),
            'customer' : Customer.objects.all().order_by('-count1'),
        }
        return render(request,"reports.html",context)
    return redirect('/')

def pickRandom(request):
    if request.session['admin'] == "Joseph":
        context={
            'customer' : Customer.objects.all().order_by('-count1'),
        }
        randomCustomer = random.randint(0,2)
        win={
            'win': context['customer'][randomCustomer]
        }
        prize=[
            ' Free Dilverey','10% Discount', '30% Discount', 'Dinner for Two', 'Order 1 get 2', 'Free Drink','Free meal', '1 hour event'
        ]
        randomGift = random.randint(0,7)
        request.session['prize'] = prize[randomGift]
        return render(request,"randomWin.html", win)
    return redirect('/')

def ManageAccount(request,id):
    cur_user= Customer.objects.get(id=id)
    context={
        'cur_user':cur_user,
        're':Reservation.objects.all()
    }
    return render(request,"ManageUserAccount.html", context)

def EditUserProfile(request,id):
    user = Customer.objects.get(id=id)
    errors = Customer.objects.editProfile_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            print(errors)
        return redirect("/ManageAccount/"+str(id))
    if request.method == "POST":
        
        user.name = request.POST['EditName']
        user.phone_number = request.POST['EditPhone']
        user.email = request.POST['EditEmail']
        user.address = request.POST['EditAddress']
        if len(request.POST['EditPassword']) > 8:
            pw_hash = bcrypt.hashpw(request.POST['EditPassword'].encode(), bcrypt.gensalt()).decode()
            user.password = pw_hash
        user.save()
        messages.success(request, "Account successfully Edited", extra_tags="succcc")

        return redirect("/ManageAccount/"+str(id))