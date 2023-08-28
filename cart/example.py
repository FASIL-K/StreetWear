# # def add_cart(request, product_id):
# #     current_user = request.user
# #     product = Product.objects.get(id=product_id)
    
# #     if current_user.is_authenticated:
# #         product_variation = []
        
# #         if request.method == 'POST':
# #             for item in request.POST:
# #                 key = item
# #                 value = request.POST[key]
                
# #                 try:
# #                     variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
# #                     product_variation.append(variation)
# #                 except Variation.DoesNotExist:
# #                     pass
        
        

# #         is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()

# #         if is_cart_item_exists:
# #             cart_item = CartItem.objects.filter(product=product, user=current_user)
# #             ex_var_list = []
# #             id_list = []

# #             for item in cart_item:
# #                 existing_variation = item.variations.all()
# #                 ex_var_list.append(list(existing_variation))
# #                 id_list.append(item.id)

# #             match_found = False
# #             for ex_vars in ex_var_list:
# #                 if set(ex_vars) == set(product_variation):
# #                     match_found = True
# #                     break

# #             if match_found:
# #                 index = ex_var_list.index(ex_vars)
# #                 item_id = id_list[index]
# #                 item = CartItem.objects.get(product=product, id=item_id)
# #                 item.quantity += 1
# #                 item.save()


                
# #             else:
# #                 item = CartItem.objects.create(product=product, quantity=1, user=current_user)
# #                 if len(product_variation) > 0:
# #                     item.variations.clear()
# #                     item.variations.add(*product_variation)
# #                 item.save()
# #         else:
# #             cart_item = CartItem.objects.create(
# #                 product=product,
# #                 quantity=1,
# #                 user=current_user,
# #             )
# #             if len(product_variation) > 0:
# #                 cart_item.variations.clear()
# #                 cart_item.variations.add(*product_variation)
# #             cart_item.save()

# #         return redirect('cart')


# #     else:
# #         product_variation = []
# #         if request.method == 'POST':
# #             for item in request.POST:
# #                 key = item
# #                 value = request.POST[key]
                
# #                 try:
# #                     variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
# #                     product_variation.append(variation)
# #                 except Variation.DoesNotExist:
# #                     pass
        
# #         try:
# #             cart = Cart.objects.get(cart_id=_cart_id(request))
# #         except Cart.DoesNotExist:
# #             cart = Cart.objects.create(
# #                 cart_id=_cart_id(request)
# #             )
# #             cart.save()
            

# #         is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

# #         if is_cart_item_exists:
# #             cart_item = CartItem.objects.filter(product=product, cart=cart)
# #             ex_var_list = []
# #             id_list = []

# #             for item in cart_item:
# #                 existing_variation = item.variations.all()
# #                 ex_var_list.append(list(existing_variation))
# #                 id_list.append(item.id)

# #             match_found = False
# #             for ex_vars in ex_var_list:
# #                 if set(ex_vars) == set(product_variation):
# #                     match_found = True
# #                     break

# #             if match_found:
# #                 index = ex_var_list.index(ex_vars)
# #                 item_id = id_list[index]
# #                 item = CartItem.objects.get(product=product, id=item_id)
# #                 item.quantity += 1
# #                 item.save()
# #                 # return HttpResponse('true')
# #             else:
# #                 item = CartItem.objects.create(product=product, quantity=1, cart=cart)
# #                 if len(product_variation) > 0:
# #                     item.variations.clear()
# #                     item.variations.add(*product_variation)
# #                 item.save()
      
# #         else:
# #             cart_item = CartItem.objects.create(
# #                 product=product,
# #                 quantity=1,
# #                 cart=cart,
# #             )
# #             if len(product_variation) > 0:
# #                 cart_item.variations.clear()
# #                 cart_item.variations.add(*product_variation)
# #             cart_item.save()

# #         return redirect('cart')

# def update_cart(request):
#     if request.method == 'POST':
#         product_id = request.POST.get('product_id')
#         selected_size = request.POST.get('selected_size')
#         cart_id = request.POST.get('cart_id')
#         print(cart_id, 'cart_id---------------')  # Print cart_id for debugging purposes
#         max_discount = 0

#         try:
#             cart = Cart.objects.get(id=cart_id)
#         except Cart.DoesNotExist:
#             return JsonResponse({'status': 'Cart item not found'}, status=404)

#         prod_qty = request.POST.get('product_qty')
#         cartes = cart.product.stock

#         if int(cartes) >= int(prod_qty):
#             cart.product_qty = prod_qty
#             cart.save()

#             user = request.user
#             total_price = 0

#             if user.is_authenticated:
#                 carts = Cart.objects.filter(user=user).order_by('id')
#                 for item in carts:
#                     product_price = item.product.product_price
#                     product_offer = item.product.offer

#                     if product_offer is None:
#                         total_price += product_price * item.product_qty
#                     else:
#                         if product_offer:
#                             max_discount = product_offer.discount_amount

#                         discount = (max_discount / 100) * product_price
#                         discounted_price = product_price - discount

#                         total_price += discounted_price * item.product_qty
#             else:
#                 session_key = request.session.session_key
#                 if session_key:
#                     carts = get_guest_cart(request, session_key)
#                     for item in carts:
#                         product_price = item.product.product_price
#                         total_price += product_price * item.product_qty

#             grand_total = total_price

#             print("Updated successfully:", cart_id, "Subtotal:", total_price, "Grand Total:", grand_total)  # Print for debugging
#             return JsonResponse({
#                 'status': 'Updated successfully',
#                 'sub_total': total_price,
#                 'grand_total': grand_total,
#                 'product_price': cart.product.product_price,
#                 'quantity': prod_qty
#             })
#         else:
#             print("Not allowed this Quantity")  # Print for debugging
#             return JsonResponse({'status': 'Not allowed this Quantity'})

#     return HttpResponse('Something went wrong, reload page')
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def deletecartitem(request, id):
#     cart_items = Cart.objects.filter(id=id)
    
#     if cart_items.exists():
#         cart_items.delete()
    
#     return redirect('cart')
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def deletecartitem(request, id):
#     cart_items = Cart.objects.filter(id=id)
    
#     if cart_items.exists():
#         cart_items.delete()
    
#     return redirect('cart')
# <script>
#     function deleteCartItem(link) {
#         var cartId = link.getAttribute("data-cartid");
#         var guestCartId = link.getAttribute("data-guestcartid");

#         $.ajax({
#             method: "POST",
#             url: "{% url 'deletecartitem' %}",
#             data: {
#                 'cart_id': cartId,
#                 'guest_cart_id': guestCartId,
#                 csrfmiddlewaretoken: '{{ csrf_token }}'
#             },
#             success: function(response) {
#                 // Handle success, such as updating the cart display
#             },
#             error: function(xhr, status, error) {
#                 console.log(xhr.responseText);
#                 // Handle error case
#             }
#         });
#     }
# </script>


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def deletecartitem(request):
#     cart_id = request.POST.get('cart_id')
#     guest_cart_id = request.POST.get('guest_cart_id')

#     if cart_id:
#         cart_items = Cart.objects.filter(id=cart_id)
#         if cart_items.exists():
#             cart_items.delete()
#     elif guest_cart_id:
#         session_key = request.session.session_key
#         if session_key:
#             guest_carts = get_guest_cart(request, session_key)
#             cart_item = guest_carts.filter(id=guest_cart_id).first()
#             if cart_item:
#                 cart_item.delete()

#     return HttpResponse(status=200)
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def deletecartitem(request):
#     cart_id = request.POST.get('cart_id')
#     guest_cart_id = request.POST.get('guest_cart_id')

#     if cart_id:
#         cart_items = Cart.objects.filter(id=cart_id)
#         if cart_items.exists():
#             cart_items.delete()
#     elif guest_cart_id:
#         session_key = request.session.session_key
#         if session_key:
#             guest_carts = get_guest_cart(request, session_key)
#             cart_item = guest_carts.filter(id=guest_cart_id).first()
#             if cart_item:
#                 cart_item.delete()

#     return HttpResponse(status=200)
# <td class="cart__close">
#     {% if user.is_authenticated %}
#         <a class="text-danger" href="{% url 'deletecartitem' cart_item.id %}">Remove</a>
#     {% endif %}
# </td>


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def cart(request):
#     if request.user.is_authenticated:
#         user = request.user
#         cart = Cart.objects.filter(user_id=user.id).order_by('id')
#         guest_cart_items = []  # Initialize an empty list for guest cart items
#     else:
#         session_key = request.session.session_key
#         if session_key:
#             cart = get_guest_cart(request, session_key)
#             guest_cart_items = cart  # Guest cart items are the same as the session cart items
#         else:
#             cart = []
#             guest_cart_items = []
#     total_price = 0
#     grand_total = 0

#     # Fetch size names based on the IDs in the cart items
#     for item in cart:
#         # ... your existing code ...

#     context = {
#         'cart': cart,
#         'total_price': total_price,
#         'grand_total': grand_total,
#         'guest_cart_items': guest_cart_items,  # Include guest cart items in the context
#     }
#     return render(request, 'user/cart/cart.html', context)



# def get_guest_cart(request, session_key):
#     cart_items = request.session.get('cart_items', [])
#     cart = create_guest_cart_items(cart_items)
#     return cart

# def create_guest_cart_items(session_cart_items):
#     cart_items = []
#     for cart_item in session_cart_items:
#         product = Product.objects.get(id=cart_item['prod_id'])
#         cart_item_instance = Cart(
#             product=product,
#             product_qty=cart_item['prod_qty'],
#             selected_size=cart_item['selected_size'],
#         )
#         cart_items.append(cart_item_instance)
#     return cart_items
# 





from django.contrib.auth import login  # Import the login function

# ... Other imports ...

# def transfer_guest_cart_to_authenticated_user(request, user):
#     session_key = request.session.session_key
#     if session_key:
#         cart_items = request.session.get('cart_items', [])
        
#         for cart_item in cart_items:
#             product_id = cart_item['prod_id']
#             product_qty = cart_item['prod_qty']
#             selected_size = cart_item['selected_size']
            
#             # Create Cart instance for the authenticated user
#             Cart.objects.create(
#                 user=user,
#                 product_id=product_id,
#                 product_qty=product_qty,
#                 selected_size=selected_size,
#             )
        
#         # Clear guest cart data from session
#         del request.session['cart_items']
#         request.session.save()

# def login_view(request):
#     if request.method == 'POST':
#         # Handle user login form submission
#         # ...
        
#         # After successful login
#         user = request.user
#         transfer_guest_cart_to_authenticated_user(request, user)
        
#         # Continue with user login process
#         login(request, user)
        
#         # Redirect to the appropriate page
#         return redirect('dashboard')
    
#     # ...
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_control
from cart.views import transfer_guest_cart_to_authenticated_user

User = get_user_model()  # Get the user model

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                # Check if the user is a guest before transferring cart items
                if user.is_anonymous:  # Guest user
                    transfer_guest_cart_to_authenticated_user(request, user)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
                return render(request, 'user/accounts/registration.html')

    return render(request, 'user/accounts/registration.html')



from django.contrib.auth import get_user_model
from django.shortcuts import render
from social_core.backends.google import GoogleOAuth2
from cart.views import transfer_guest_cart_to_authenticated_user

User = get_user_model()  # Get the user model

def custom_login(request):
    user = request.user  # Get the authenticated user
    if user.is_authenticated:
        transfer_guest_cart_to_authenticated_user(request, user)
        return render(request, 'user/accounts/registration.html')
    else:
        # Handle case where user is not authenticated (optional)
        # For example, redirect them to the login page
        return redirect('login')




from cart.models import Cart

def transfer_guest_cart_to_authenticated_user(request, user):
    session_key = request.session.session_key
    if session_key:
        cart_items = request.session.get('cart_items', [])

        for cart_item in cart_items:
            product_id = cart_item['prod_id']
            product_qty = cart_item['prod_qty']
            selected_size = cart_item['selected_size']

            # Create Cart instance for the authenticated user
            Cart.objects.create(
                user=user,
                product_id=product_id,
                product_qty=product_qty,
                selected_size=selected_size,
            )

        # Clear guest cart data from session
        del request.session['cart_items']
        request.session.save()



from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from social_core.backends.google import GoogleOAuth2
from cart.views import transfer_guest_cart_to_authenticated_user

User = get_user_model()  # Get the user model

def custom_login(request):
    user = request.user  # Get the authenticated user
    if user.is_authenticated:
        transfer_guest_cart_to_authenticated_user(request, user)
        return redirect('home')  # Redirect to the home page after successful login
    else:
        # Handle case where user is not authenticated (optional)
        # For example, redirect them to the login page
        return redirect('login')




from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from account import views  # Import the custom_login view
from Home import views as home_views  # Import the home view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.urls')),
    path('', include('account.urls')),
    # ... other URL patterns ...
    
    path('login/', views.custom_login, name='custom_login'),  # Custom login view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('', home_views.home, name='home'),  # Home view
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
