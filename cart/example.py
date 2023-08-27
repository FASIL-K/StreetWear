# def add_cart(request, product_id):
#     current_user = request.user
#     product = Product.objects.get(id=product_id)
    
#     if current_user.is_authenticated:
#         product_variation = []
        
#         if request.method == 'POST':
#             for item in request.POST:
#                 key = item
#                 value = request.POST[key]
                
#                 try:
#                     variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
#                     product_variation.append(variation)
#                 except Variation.DoesNotExist:
#                     pass
        
        

#         is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()

#         if is_cart_item_exists:
#             cart_item = CartItem.objects.filter(product=product, user=current_user)
#             ex_var_list = []
#             id_list = []

#             for item in cart_item:
#                 existing_variation = item.variations.all()
#                 ex_var_list.append(list(existing_variation))
#                 id_list.append(item.id)

#             match_found = False
#             for ex_vars in ex_var_list:
#                 if set(ex_vars) == set(product_variation):
#                     match_found = True
#                     break

#             if match_found:
#                 index = ex_var_list.index(ex_vars)
#                 item_id = id_list[index]
#                 item = CartItem.objects.get(product=product, id=item_id)
#                 item.quantity += 1
#                 item.save()


                
#             else:
#                 item = CartItem.objects.create(product=product, quantity=1, user=current_user)
#                 if len(product_variation) > 0:
#                     item.variations.clear()
#                     item.variations.add(*product_variation)
#                 item.save()
#         else:
#             cart_item = CartItem.objects.create(
#                 product=product,
#                 quantity=1,
#                 user=current_user,
#             )
#             if len(product_variation) > 0:
#                 cart_item.variations.clear()
#                 cart_item.variations.add(*product_variation)
#             cart_item.save()

#         return redirect('cart')


#     else:
#         product_variation = []
#         if request.method == 'POST':
#             for item in request.POST:
#                 key = item
#                 value = request.POST[key]
                
#                 try:
#                     variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
#                     product_variation.append(variation)
#                 except Variation.DoesNotExist:
#                     pass
        
#         try:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#         except Cart.DoesNotExist:
#             cart = Cart.objects.create(
#                 cart_id=_cart_id(request)
#             )
#             cart.save()
            

#         is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

#         if is_cart_item_exists:
#             cart_item = CartItem.objects.filter(product=product, cart=cart)
#             ex_var_list = []
#             id_list = []

#             for item in cart_item:
#                 existing_variation = item.variations.all()
#                 ex_var_list.append(list(existing_variation))
#                 id_list.append(item.id)

#             match_found = False
#             for ex_vars in ex_var_list:
#                 if set(ex_vars) == set(product_variation):
#                     match_found = True
#                     break

#             if match_found:
#                 index = ex_var_list.index(ex_vars)
#                 item_id = id_list[index]
#                 item = CartItem.objects.get(product=product, id=item_id)
#                 item.quantity += 1
#                 item.save()
#                 # return HttpResponse('true')
#             else:
#                 item = CartItem.objects.create(product=product, quantity=1, cart=cart)
#                 if len(product_variation) > 0:
#                     item.variations.clear()
#                     item.variations.add(*product_variation)
#                 item.save()
      
#         else:
#             cart_item = CartItem.objects.create(
#                 product=product,
#                 quantity=1,
#                 cart=cart,
#             )
#             if len(product_variation) > 0:
#                 cart_item.variations.clear()
#                 cart_item.variations.add(*product_variation)
#             cart_item.save()

#         return redirect('cart')