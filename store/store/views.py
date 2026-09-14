from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Home Page
def home(request):
    return render(request, 'store/home.html')


# Product List
def product_list(request):
    products = Product.objects.all()

    return render(request, 'store/product_list.html', {
        'products': products
    })


# Product Details
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    return render(request, 'store/product_detail.html', {
        'product': product
    })


# Add Product to Cart
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    cart = request.session.get('cart', {})

    product_id = str(product.id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


# Cart Page
@login_required(login_url='/login/')
def cart(request):
    cart_data = request.session.get('cart', {})

    products = []
    total = 0

    for product_id, quantity in cart_data.items():

        product = get_object_or_404(Product, id=product_id)

        subtotal = product.price * quantity
        total += subtotal

        products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'store/cart.html', {
        'products': products,
        'total': total
    })


# Checkout
@login_required(login_url='/login/')
def checkout(request):

    if request.method == 'POST':

        customer_name = request.POST.get('customer_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        cart_data = request.session.get('cart', {})

        total = 0

        for product_id, quantity in cart_data.items():

            product = get_object_or_404(Product, id=product_id)

            if quantity > product.stock:
                return render(request, 'store/checkout.html', {
            'error': f'Sorry, only {product.stock} items of {product.name} are available.'
        })

        total += product.price * quantity

        product.stock -= quantity
        product.save()

        order = Order.objects.create(
            user=request.user,
            customer_name=customer_name,
            email=email,
            phone=phone,
            address=address,
            payment_method=payment_method,
            total_amount=total
        )

        # Empty cart after order
        request.session['cart'] = {}
        request.session.modified = True

        return render(request, 'store/order_success.html', {
            'order': order
        })

    return render(request, 'store/checkout.html')


# My Orders
@login_required(login_url='/login/')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')

    return render(request, 'store/my_orders.html', {
        'orders': orders
    })


# Increase Quantity
def increase_quantity(request, id):

    cart_data = request.session.get('cart', {})

    product_id = str(id)

    if product_id in cart_data:
        cart_data[product_id] += 1

    request.session['cart'] = cart_data
    request.session.modified = True

    return redirect('cart')


# Decrease Quantity
def decrease_quantity(request, id):

    cart_data = request.session.get('cart', {})

    product_id = str(id)

    if product_id in cart_data:

        if cart_data[product_id] > 1:
            cart_data[product_id] -= 1
        else:
            del cart_data[product_id]

    request.session['cart'] = cart_data
    request.session.modified = True

    return redirect('cart')


# Remove Product from Cart
def remove_from_cart(request, id):

    cart_data = request.session.get('cart', {})

    product_id = str(id)

    if product_id in cart_data:
        del cart_data[product_id]

    request.session['cart'] = cart_data
    request.session.modified = True

    return redirect('cart')


# ==========================
# USER REGISTRATION
# ==========================

def register(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check password
        if password != confirm_password:

            messages.error(
                request,
                'Passwords do not match.'
            )

            return redirect('register')

        # Check username
        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                'Username already exists.'
            )

            return redirect('register')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        messages.success(
            request,
            'Registration successful. Please login.'
        )

        return redirect('login')

    return render(request, 'store/register.html')


# ==========================
# USER LOGIN
# ==========================

def user_login(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                'Login successful.'
            )

            return redirect('home')

        else:

            messages.error(
                request,
                'Invalid username or password.'
            )

            return redirect('login')

    return render(request, 'store/login.html')


# ==========================
# USER LOGOUT
# ==========================

def user_logout(request):

    logout(request)

    messages.success(
        request,
        'You have been logged out.'
    )

    return redirect('home')