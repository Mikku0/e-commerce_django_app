from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Order, Item, OrderItem, Coupon
from decimal import Decimal


@login_required(login_url='login')
def cart(request):

    original_cart_value = 0

    user_order = Order.objects.filter(user=request.user).first()
    if user_order:
        order_items = user_order.items.all()
        user_order.total_price = 0
        for order_item in order_items:
            order_item.total_price = order_item.quantity * order_item.item.price
            user_order.total_price += order_item.total_price
        original_cart_value = user_order.total_price

        if user_order.coupon:
            discount_amount = (user_order.coupon.discount / Decimal(100)) * user_order.total_price
            user_order.final_price = user_order.total_price - round(discount_amount, 2)
        else:
            user_order.final_price = user_order.total_price
    else:
        order_items = []

    user_order.save()

    context = {
        'order_items': order_items,
        'final_price': user_order.final_price,
        'original_cart_value': original_cart_value,
        'discount_price_value': abs(user_order.final_price - original_cart_value),
        'coupon': user_order.coupon if user_order else None
    }
    return render(request, 'base/cart.html', context)


@login_required(login_url='login')
def update_cart(request):
    if request.method == 'POST':
        user_order = Order.objects.filter(user=request.user).first()
        if user_order:
            if 'remove_item' in request.POST:
                order_item_id = request.POST.get('remove_item')
                order_item = user_order.items.filter(id=order_item_id).first()
                if order_item:
                    order_item.delete()
            else:
                for order_item in user_order.items.all():
                    quantity_field = f'quantity_{order_item.id}'
                    if quantity_field in request.POST:
                        new_quantity = int(request.POST[quantity_field])
                        if new_quantity > 0:
                            order_item.quantity = new_quantity
                            order_item.save()

        return redirect('cart')


@login_required(login_url='login')
def add_coupon_in_cart(request):
    if request.method == 'POST':
        user_order = Order.objects.filter(user=request.user, status='pending').first()
        if user_order:
            coupon_code = request.POST.get('coupon_code', '').strip()
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                user_order.coupon = coupon
                messages.success(request, 'Coupon applied successfully!')
            except Coupon.DoesNotExist:
                messages.error(request, 'Invalid coupon code')

            user_order.save()

    return redirect('cart')


@login_required(login_url='login')
def add_item_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    order, created = Order.objects.get_or_create(user=request.user, status='pending')

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        order_item, order_item_created = OrderItem.objects.get_or_create(order=order, item=item)

        if not order_item_created:
            order_item.quantity += quantity
        else:
            order_item.quantity = quantity

        order_item.total_price = order_item.quantity * item.price
        order_item.save()
        order.save()
        return redirect('cart')


@login_required(login_url='login')
def remove_item_from_cart(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id, order__user=request.user)
    order_item.delete()
    return redirect('cart')

