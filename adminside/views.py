from django.shortcuts import render,redirect
from account.models import User
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import csv
import io
from django.db.models import Q
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
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@staff_member_required(login_url='admin_login')
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    return render(request,'adminside/dashboard.html')

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
    





def sales_report(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')

    if request.method=='GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
    
        if start_date and end_date:
            # Filter orders based on the selected date range
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            if start_date > end_date:
                messages.error(request, "Start date must be before end date.")
                return redirect('sales_report')
            if end_date > date.today():
                messages.error(request, "End date cannot be in the future.")
                return redirect('sales_report')

            orders = Order.objects.filter(created_at__date__range=(start_date, end_date))
            recent_orders = orders.order_by('-created_at')
        else:
            # If no date range is selected, fetch recent 10 orders
            recent_orders = Order.objects.order_by('-created_at')[:10]
            orders = Order.objects.all()
  
    # Calculate total sales and total orders
    total_sales = sum(order.total_price for order in orders)
    total_orders = orders.count()

    # Calculate sales by status
    sales_by_status = {
        'Pending': orders.filter(order_status= 1).count(),
        'Processing': orders.filter(order_status=2).count(),
        'Shipped': orders.filter(order_status=3).count(),
        'Delivered': orders.filter(order_status=4).count(),
        'Cancelled': orders.filter(order_status=5).count(),
        'Return': orders.filter(order_status=6).count(),
    }
    # Prepare data for rendering the template
    sales_report = {
        'start_date': start_date.strftime('%Y-%m-%d') if start_date else '',
        'end_date': end_date.strftime('%Y-%m-%d') if end_date else '',
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
        order_items = OrderItem.objects.filter(order=order).select_related('variant')  # Use select_related to optimize DB queries
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
                    order_item.variant.product.product_name,  # Replace 'product_name' with the actual attribute in your Product model
                    order_item.price,
                    order_item.quantity,
                ])

    return response


@login_required(login_url='admin_login1')
def generate_pdf(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    
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
        Prefetch('orderitem_set', queryset=OrderItem.objects.select_related('variant'))
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
                order_item.variant.product.product_name,
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
