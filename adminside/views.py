from django.shortcuts import render,redirect
from account.models import User
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import csv
import io
from products.models import *
from collections import Counter

from django.db.models import Q,Sum,Count
from django.http import HttpResponse
from django.db.models import DateField
from datetime import date, datetime,timedelta
from checkout.models import OrderItem
from checkout.models import Order
from django.db.models.functions import TruncMonth
from fpdf import FPDF
from django.http import HttpResponse
from datetime import datetime
from django.db.models import Prefetch
from itertools import groupby

# Create your views here.
@login_required(login_url='admin_login')
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    
    total_profit = Order.objects.aggregate(total_profit=Sum('total_price'))['total_profit'] or 0

    # Count total orders
    total_orders = Order.objects.count()

    # Count total users
    total_users = User.objects.count()
    brands = Brand.objects.all()

    # Count total products
    total_products = Product.objects.count()
    categories = Category.objects.all()

    order_status_data = Order.objects.filter(Q(orderitem__status='Cancelled') | Q(orderitem__status='Return')).aggregate(total_price=Sum('total_price'))
    cancelled_return_price = order_status_data['total_price'] or 0

    # Calculate the sum of prices for all other orders
    other_orders_price = Order.objects.exclude(Q(orderitem__status='Cancelled') | Q(orderitem__status='Return')).aggregate(total_price=Sum('total_price'))['total_price'] or 0


    # Initialize lists to store category names and sales data
    category_names = []
    category_sales_data = []  # Renamed to avoid conflicts

    # Loop through each category and calculate the total sales
    for category in categories:
        total_sales = Product.objects.filter(category=category).aggregate(total_sales=Sum('orderitem__price'))['total_sales'] or 0
        category_names.append(category.name)
        category_sales_data.append(total_sales)  # Renamed to avoid conflicts
  
    pro = Product.objects.all()[:5]
    payment_mode_counts = Order.objects.values('payment_mode').annotate(count=Count('id'))

    # Extract the labels and data for the chart
    labels = [pm['payment_mode'] for pm in payment_mode_counts]
    data = [pm['count'] for pm in payment_mode_counts]
    
    order_status_counts = OrderItem.objects.values('status').annotate(count=Count('id'))

    # Extract the labels and data for the pie chart
    status_labels = [status['status'] for status in order_status_counts]
    status_data = [status['count'] for status in order_status_counts]

    sales_data = Order.objects.values('created_at').annotate(total_sales=Sum('total_price'))

    # Separate the dates and total sales into two lists for the chart
    dates = [data['created_at'].strftime('%Y-%m-%d') for data in sales_data]
    total_sales = [data['total_sales'] for data in sales_data]

    today = datetime.today().date()
    last_week_start = today - timedelta(days=7)
    last_week_end = today - timedelta(days=1)
    last_week_profit = Order.objects.filter(created_at__range=(last_week_start, last_week_end)).aggregate(last_week_profit=Sum('total_price'))['last_week_profit'] or 0

     # Calculate monthly income
 
    # Retrieve product names for the graph
    products = Product.objects.all()

    order_items=OrderItem.objects.all()

    product_sales_counter = Counter(item.product for item in order_items)
    top_5_selling_products = product_sales_counter.most_common(5)
    top_selling_products_data = [{
        'product_name': product.product_name,
        'sales_quantity': sales_quantity,
    } for product, sales_quantity in top_5_selling_products]

    context = {
        'total_profit': total_profit,
        'total_orders': total_orders,
        'total_users': total_users,
        'total_products': total_products,
        'last_week_profit': last_week_profit,
        'products': products,
        'brands': brands,
        'pro': pro,
        'labels': labels,
        'data': data,
        'status_labels': status_labels,
        'status_data': status_data,
        'category_names': category_names,
        'category_sales_data': category_sales_data,  # Renamed to avoid conflicts
        'dates': dates,
        'total_sales': total_sales,
        'cancelled_return_price':cancelled_return_price,
        'other_orders_price':other_orders_price,
        'top_selling_products_data': top_selling_products_data,

      
    }

    return render(request, 'adminside/dashboard.html', context)

#---------------------------User management -----------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@staff_member_required(login_url='admin_login')
def user_mangement(request):
    users = User.objects.all().order_by('id')
    return render(request,'adminside/usermanagement/user_management.html',{'users':users})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@staff_member_required(login_url='admin_login')
def user_block(request,user_id):
    users = User.objects.get(id=user_id)
    if users.is_superuser:
        messages.error(request,"Cannot block superuser")
        return redirect(user_mangement)
    if users.is_active is True:
        users.is_active = False
        messages.success(request,"Un blocked successfully")
    else:
        users.is_active = True
        messages.success(request,"Blocked Successfully")
    users.save()
    return redirect(user_mangement)
    





@login_required(login_url='admin_login1')
def sales_report(request):
    if not request.user.is_superuser:
        return redirect('admin_login')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    orders = Order.objects.all()

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            if start_date > end_date:
                messages.error(request, "Start date must be before end date.")
                return redirect('sales_report')
            if end_date > date.today():
                messages.error(request, "End date cannot be in the future.")
                return redirect('sales_report')
            orders = Order.objects.filter(created_at__date__range=(start_date, end_date))
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect('sales_report')

    recent_orders = orders.order_by('-created_at')[:15]
    total_sales = sum(order.total_price for order in orders)
    total_orders = orders.count()

    order_items = OrderItem.objects.all()
    sales_by_status = {
        'Pending': order_items.filter(status='Pending').count(),
        'Processing': order_items.filter(status='Processing').count(),
        'Shipped': order_items.filter(status='Shipped').count(),
        'Delivered': order_items.filter(status='Delivered').count(),
        'Cancelled': order_items.filter(status='Cancelled').count(),
        'Return': order_items.filter(status='Return').count(),
    }

    sales_report = {
        'start_date': start_date,
        'end_date': end_date,
        'total_sales': total_sales,
        'total_orders': total_orders,
        'sales_by_status': sales_by_status,
        'recent_orders': recent_orders,
    }

    return render(request, 'adminside/salesreport/salesreport.html', {'sales_report': sales_report})


@login_required(login_url='admin_login1')
def export_csv(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
        str(datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['user', 'total_price', 'payment_mode', 'tracking_no', 'Orderd at', 'product_name', 'product_price', 'product_quantity'])

    orders = Order.objects.all()
    for order in orders:
        order_items = OrderItem.objects.filter(order=order).select_related('product')  # Use select_related to optimize DB queries
        grouped_order_items = groupby(order_items, key=lambda x: x.order_id)
        for order_id, items_group in grouped_order_items:
            items_list = list(items_group)
            for order_item in items_list:
                writer.writerow([
                    order.user.first_name if order_item == items_list[0] else "",
                    order.total_price if order_item == items_list[0] else "",
                    order.payment_mode if order_item == items_list[0] else "",
                    order.tracking_no if order_item == items_list[0] else "",
                    order.created_at if order_item == items_list[0] else "",  # Only include date in the first row
                    order_item.product.product_name,  # Replace 'product_name' with the actual attribute in your Product model
                    order_item.price,
                    order_item.quantity,
                ])

    return response


from django.db.models import Prefetch

@login_required(login_url='admin_login1')
def generate_pdf(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
        str(datetime.now()) + '.pdf'
    w_pt = 8.5 * 40  # 8.5 inches width
    h_pt = 11 * 20   # 11 inches height   

    pdf = FPDF(format=(w_pt, h_pt))
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)  # Enable auto page break with 15mm margin

    # Set font styles
    pdf.set_font('Arial', 'B', 12)  # Reduce font size for better readability

    # Header Information
    pdf.cell(0, 10, 'Order Details Report', 0, 1, 'C')
    pdf.cell(0, 10, str(datetime.now()), 0, 1, 'C')
    # Table Data
    data = [['User', 'Total Price', 'Payment Mode', 'Tracking No', 'Ordered At', 'Product Name', 'Product Price', 'Product Quantity']]
    orders = Order.objects.all().prefetch_related(
        Prefetch('orderitem_set', queryset=OrderItem.objects.select_related('product'))
    )
    for order in orders:
        order_items = order.orderitem_set.all()
        for index, order_item in enumerate(order_items):
            data.append([
                order.user.first_name if index == 0 else "",
                order.total_price if index == 0 else "",
                order.payment_mode if index == 0 else "",
                order.tracking_no if index == 0 else "",
                str(order.created_at.date()) if index == 0 else "",
                order_item.product.product_name,
                order_item.price,
                order_item.quantity,
            ])
    # Create Table
    col_width = 40  
    row_height = 10
    for row in data:
        for item in row:
            pdf.cell(col_width, row_height, str(item), border=1)
        pdf.ln()
    response.write(pdf.output(dest='S').encode('latin1'))  
    return response
