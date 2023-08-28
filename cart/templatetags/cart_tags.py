from django import template
from products.models import Product

register = template.Library()

@register.simple_tag
def guest_cart_items(session_cart_items):
    guest_cart_items = []
    
    for cart_item in session_cart_items:
        product = Product.objects.get(id=cart_item['prod_id'])
        guest_cart_items.append({
            'product': product,
            'product_qty': cart_item['prod_qty'],
            'selected_size': cart_item['selected_size'],
        })
    
    return guest_cart_items
