from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, RegisterForm, NewRestaurantForm, NewItemForm, NewProfileForm, EditProfileForm, EditFoodItemForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from .models import  *
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from django.http import HttpResponse
import uuid


def email_view(request):
    return render(request, 'food_model/email_view.html')

def index(request):
   profile = Profile.objects.filter(terms_and_services = False)
   if profile:
      return render(request, 'food_model/index.html', {'profile': profile})
   else:
      return render(request, 'food_model/index.html')

def login_site(request):
   if request.method == "POST":
      form = LoginForm(request.POST)
      if form.is_valid():
         username = form.cleaned_data['username']
         password = form.cleaned_data['password']

         user = authenticate(request, username=username, password=password)

         if user is not None:
            login(request, user)
            return redirect('/')
         
         else:
            messages.error(request, 'Enter the correct signup details')
   else:
      form = LoginForm()
   return render(request, 'food_model/login.html', {'form': form})

def register(request):
    if request.method == "POST":
      form = RegisterForm(request.POST)
      if form.is_valid():
          username = form.cleaned_data['username']
          email = form.cleaned_data['email']
          password = form.cleaned_data['password']
         #  try:
               # if User.objects.filter(username = username).exist():
               #    messages.success(request, 'Username is taken.')
               #    return redirect('food_model:register')
               # if User.objects.filter(email = email).exist():
               #    messages.success(request, 'Email is taken.')
               #    return redirect('food_model:register')
            
          User.objects.create_user(username=username, email=email, password=password)           
          return redirect('food_model:email_view')
         #  except Exception as e:
            #   print(e)
          # else:
          #    messages.warning(request, 'Password must be contain more than 8 character, and atleast one character like !,@,#,$ ')
    
    else:
         form = RegisterForm()

    return render(request, 'food_model/signup.html', {'form': form})


#Admin
def shopownergroup(request):
   if request.method == 'POST':
        group_ids = request.POST.getlist('groups')

        # Assign the selected groups to the user
        for group_id in group_ids:
            group = Group.objects.get(id=group_id)
            request.user.groups.add(group)

        groups = Group.objects.all()
       
   return render(request, 'admin_site/admin_view.html', {'groups': groups,})


@login_required
def admin_view(request):
   pending =Pending.objects.all()
   if request.user.is_superuser:
      if request.method=="POST":
         action = request.POST.get("action")
         print("Hello")
         #approval
         id_list = request.POST.getlist('boxes')
         pending.update(is_approved=False)
         for x in id_list:
            Pending.objects.filter(pk=int(x)).update(is_approved = True)
         
         if action == 'approve':
            application = Pending.objects.get(id=request.POST.get('id'))
            application.status = 'approved'
            application.save()
         elif action == 'reject':
            application = Pending.objects.get(id=request.POST.get('id'))
            application.status = 'rejected'
            application.delete()
         return redirect('food_model:admin_views')
         
   return render(request, 'admin_site/admin_view.html', {'pending':pending})


#Shop Owner 
@login_required
def shopowner_register(request):
  if request.method == "POST":
      form = NewRestaurantForm(request.POST, request.FILES)
      if form.is_valid():
         restaurant = form.save(commit=False)
         restaurant.created_by = request.user
         restaurant.save()
      
  else:
       form = NewRestaurantForm()
   
  return render(request, 'food_model/owner_form.html', {
      'form': form,
   })

@login_required
def restaurant_view(request):
      restaurants = Pending.objects.filter(created_by=request.user, status="approved")
      if restaurants:
         for restaurant in restaurants:
            if restaurant.status == 'approved':
               return render(request, 'dashboard/dash.html', {'restaurants':restaurants,})
      else:
         return HttpResponse("You are not the shop Owner.")
      
@login_required
def addfood_item(request):
   restaurants = Pending.objects.filter(created_by=request.user)
   food_items = MenuItem.objects.all()
   if request.method == "POST":
      form = NewItemForm(request.POST, request.FILES, request=request)

      if form.is_valid():
         food_item = form.save(commit=False)
         food_item.created_by = request.user
         food_item.save()

         return redirect("food_model:restaurant_view")
   else:
        print("hello")
        form = NewItemForm(request=request)

   return render(request, 'dashboard/addfooditem.html', {
      'form': form,
      "restaurants":restaurants ,
      'food_items': food_items,
   })


class Food_item_list(View):
   def get(self, request, restaurant_id):
         restaurant = Pending.objects.get(id=restaurant_id, created_by = request.user)
         food_items = MenuItem.objects.filter(restaurant=restaurant)
         return render(request, 'dashboard/showfooditem.html', {'restaurant': restaurant, 'food_items': food_items})
   
def delete_food_item(request, pk):
   item = MenuItem.objects.get(created_by = request.user, pk=pk)
   item.delete()

   return redirect("food_model:restaurant_view")

def edit_food_item(request, pk):
    item = MenuItem.objects.get(id = pk, created_by = request.user)

    if request.method == "POST":
        form = EditFoodItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()

            return redirect('food_model:restaurant_view')
    else:
        form = EditFoodItemForm(instance=item)

    return render(request, 'dashboard/edit_food_item.html', {
        'form':form,
    })

class ShopOwnerView(View):
    def get(self, request):
        pending = Pending.objects.get(created_by = request.user)
        restaurant = pending.id  # Assuming the shop owner is logged in and associated with a restaurant
        pending_orders = Order.objects.filter(restaurant=restaurant, status='pending')

        return render(request, 'dashboard/ordered_page.html', {'pending_orders': pending_orders})
    
def accept_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.status = 'accepted'
    order.save()
    return redirect('food_model:shop_owner_orders') 

def reject_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.status = 'rejected'
    order.delete()
    return redirect('food_model:shop_owner_orders') 


#User
@login_required
def restaurant(request):
   restaurants = Pending.objects.filter(status = "approved")
   category = RestaurantCategory.objects.all()
   query = request.GET.get('query', '')

   if query:
       restaurants = restaurants.filter(restaurant_name__icontains = query)

   return render(request, 'user_view/user_restaurant_view.html', {
      'restaurants': restaurants,
      'category': category,
      'query': query,
   })
@login_required
def profile_enter(request):
      profile = Profile.objects.filter(created_by=request.user, terms_and_services = False)
      if request.method == "POST":
            form = NewProfileForm(request.POST, request.FILES)
            if form.is_valid():
               profile = form.save(commit=False)
               profile.created_by = request.user
               profile.save()
               return redirect('food_model:index')
      else:
            form = NewProfileForm()

      return render(request, 'user_profile/profile.html', {
            'form':form,
         })

      

@login_required
def profile_view(request):
   profile = Profile.objects.filter(created_by=request.user)

   if profile and request.user.is_authenticated:
         return render(request, 'user_profile/view_profile.html', {
         'profile': profile,
      })
   else:
      prof = Profile.objects.filter(created_by=request.user, terms_and_services = False)
      if request.method == "POST":
            form = NewProfileForm(request.POST, request.FILES)
            if form.is_valid():
               profile = form.save(commit=False)
               profile.created_by = request.user
               profile.save()
               return redirect('food_model:index')
      else:
            form = NewProfileForm()
      return render(request, 'user_profile/profile.html', {'form':form})
   

@login_required
def edit_profile_view(request, pk):
      prof = Profile.objects.get(id = pk, created_by = request.user)

      if request.method == "POST":
         form = EditProfileForm(request.POST, request.FILES, instance=prof)

         if form.is_valid():
             form.save()

             return redirect('food_model:profile_view')
      else:
          form = EditProfileForm(instance=prof,)
      
      return render(request, 'user_profile/edit_profile_view.html', {
          'form': form,
      })


class food_item(View):
   def get(self, request, restaurant_id):
         profile = Profile.objects.filter(created_by=request.user)
         restaurant = Pending.objects.get(id=restaurant_id)
         food_items = MenuItem.objects.filter(restaurant=restaurant, is_sold = False)

         if request.user.is_authenticated:
            if food_items:
                  return render(request, 'user_view/user_fooditem.html', {
                  'restaurant': restaurant, 
                  'food_items': food_items,
                  })
            else:
               return HttpResponse("Sorry restaruant owner didn't add the food")
   def post(self, request, restaurant_id, *args, **kwargs):
        restaurant = Pending.objects.get(id=restaurant_id)
        order_items = {
            'items' : []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk = int(item))
            item_data = {
                'id' : menu_item.pk,
                'name': menu_item.food_name,
                'price': menu_item.price,
            }
            order_items['items'].append(item_data)
        
        price = 0
        item_ids = []

        for item in order_items['items']:
            price = price + item['price']
            item_ids.append(item['id'])


        # Create an Order object
        order = Order.objects.create(
            user=request.user,
            restaurant=restaurant,
            total_price=price,
        )
        order.items.set(item_ids)
     
        context = {
            'items': order_items['items'],
            'price': price,
            'order': order,
        }   
        if price == 0:
         return HttpResponse('You have order atleast one item.')
        else:
            return render(request, 'user_view/order_confirmaiton.html', context)
   
def user_order_detail(request):
    user_orders = Order.objects.filter(user=request.user)
    last = Order.objects.filter(user = request.user).last
    return render(request, 'user_profile/order_detail.html', {'user_orders': user_orders, 'last': last})

