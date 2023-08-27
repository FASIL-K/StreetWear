from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from cart.models import Cart
from products.models import Product,Size,Variation
from django.http.response import JsonResponse
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

# Create your views here.

def _get_or_create_cart(request):
    cart_id = request.session.get('cart_id')
    if not cart_id:
        cart_id = request.session.create()

        request.session['cart_id'] = cart_id
    return cart_id

def create_guest_cart_items(session_cart_items):
    cart_items = []

    for cart_item in session_cart_items:
        product = Product.objects.get(id=cart_item['prod_id'])
        cart_item_instance = Cart(
            product=product,
            product_qty=cart_item['prod_qty'],
            selected_size=cart_item['selected_size'],
        )
        cart_items.append(cart_item_instance)

    return cart_items



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user_id=user.id).order_by('id')
    else:
        cart_id = request.session.get('session_key')
        if cart_id:
            cart_items = request.session.get('cart_items', [])

            cart = create_guest_cart_items(cart_items)
        else:
            cart = []
    total_price=0
    
    grand_total=0
    
    # Fetch size names based on the IDs in the cart items
    for item in cart:
        try:
            item.selected_size = Size.objects.get(id=item.selected_size).name
        except Size.DoesNotExist:
            item.selected_size = "Unknown Size"  # Handle the case where the size ID does not exist in the Size model

        product_price = item.product.product_price
        product_offer = item.product.offer
        
        if product_offer is None:
            total_price += product_price * item.product_qty
            a=product_price * item.product_qty
        else:
            if product_offer:
                max_discount = product_offer.discount_amount

            discount = (max_discount / 100) * product_price
           
            discounted_price = product_price - discount

            total_price += discounted_price * item.product_qty
         
            a=discounted_price * item.product_qty


    # total_price = sum(item.product.product_price * item.product_qty for item in cart)
    grand_total = total_price 

    context = {
        'cart': cart,
        'total_price': total_price,
        'grand_total': grand_total,
    }
    return render(request, 'user/cart/cart.html', context)

def addtocart(request):
    if request.method == 'POST':
        session_key = request.session.session_key
        prod_id = int(request.POST.get('prod_id'))
        product_check = Product.objects.get(id=prod_id)
        prod_qty = int(request.POST.get('product_qty'))
        selected_size = int(request.POST.get('size'))

        if product_check:
            if request.user.is_authenticated:
                user = request.user
                cart_item = Cart.objects.filter(user_id=user.id, product_id=prod_id, selected_size=selected_size).first()

                if cart_item:
                    return JsonResponse({'status': "Product Already in Cart"})
                else:
                    # Add the product to the authenticated user's cart
                    if product_check.stock >= prod_qty:
                        Cart.objects.create(
                            user_id=user.id,
                            product_id=prod_id,
                            product_qty=prod_qty,
                            selected_size=selected_size,
                        )
                        return JsonResponse({'status': "Product added successfully"})
                    else:
                        return JsonResponse({'status': "Only " + str(product_check.stock) + " quantity available"})
            else:
                session_key = request.session.session_key
                if not session_key:
                    request.session.create()
                    session_key = request.session.session_key
                    print("Session created:", session_key)
                cart_items = request.session.get('cart_items', [])
                existing_item = next((item for item in cart_items if item['prod_id'] == prod_id and item['selected_size'] == selected_size), None)

                if existing_item:
                    return JsonResponse({'status': "Product Already in Cart"})
                else:
                    cart_item = {
                        'prod_id': prod_id,
                        'prod_qty': prod_qty,
                        'selected_size': selected_size,
                    }
                    cart_items.append(cart_item)
                    request.session['cart_items'] = cart_items
                    request.session.save()
                    

                    
                    return JsonResponse({'status': "Product added successfully"})
        else:
            return JsonResponse({'status': "No such product found"})

# Update cart quantity
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        selected_size = request.POST.get('selected_size')
        cart_id = request.POST.get('cart_id')
        max_discount=0
        
        
        if (Cart.objects.get(id=cart_id)):

            prod_qty = request.POST.get('product_qty')
            print(prod_qty,'faxoo')
            cart = Cart.objects.get(id=cart_id)
            cartes = cart.product.stock
            if int(cartes) >= int(prod_qty):
                cart.product_qty = prod_qty
                cart.save()

                carts = Cart.objects.filter(user=request.user).order_by('id')
                total_price =0 
                for item in carts:
                    product_price = item.product.product_price
                    product_offer = item.product.offer

                    if product_offer is None:
                        total_price += product_price * item.product_qty
                    else:
                        if product_offer:
                            max_discount = product_offer.discount_amount
                    discount = (max_discount / 100) * product_price
           
                    discounted_price = product_price - discount

                    total_price += discounted_price * item.product_qty

                
                grand_total = total_price

                return JsonResponse({
                    'status': 'Updated successfully',
                    'sub_total': total_price,
                    'grand_total': grand_total,
                    'product_price': cart.product.product_price,
                    'quantity': prod_qty
                })
            else:
                return JsonResponse({'status': 'Not allowed this Quantity'})
    return HttpResponse('Something went wrong, reload page')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
# @login_required(login_url='signin')
def deletecartitem(request, id):
    cart_id = request.POST.get(id)
    cart_items = Cart.objects.filter(id=id)
    if cart_items.exists():
        cart_items.delete()
    return redirect('cart')

def update_cart_item_size(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cartid')
        selected_size = request.POST.get('size')
        if cart_id:
            cart_item = Cart.objects.get(id=cart_id)
            cart_item.selected_size = selected_size
            cart_item.save()
            size = Size.objects.get(id=cart_item.selected_size)
            return JsonResponse({'status': 'Size updated successfully','sizename':size.name})
        else:
            return JsonResponse({'status': 'Cart item not found'}, status=404)
    else:
        return JsonResponse({'status': 'Invalid request method'}, status=400)