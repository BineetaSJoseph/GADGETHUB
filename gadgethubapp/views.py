
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from .forms import SignUpForm,ProfileUpdateForm
from .models import Category, Product, Cart, CartItem, Order,Review,Wishlist
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum

# ==========================
# Home Page
# ==========================

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = Category.objects.all()
        context["products"] = Product.objects.all()

        return context


# ==========================
# About Page
# ==========================

class AboutView(TemplateView):
    template_name = "about.html"


# ==========================
# Contact Page
# ==========================

class ContactView(TemplateView):
    template_name = "contact.html"


# ==========================
# Login
# ==========================

class UserLoginView(LoginView):
    template_name = "login.html"


# ==========================
# Logout
# ==========================

class UserLogoutView(LogoutView):
    next_page = "login"


# ==========================
# Signup
# ==========================

class SignUpView(FormView):
    template_name = "signup.html"
    form_class = SignUpForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home")


# ==========================
# Product List
# ==========================

# ==========================
# Product List
# ==========================

class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"

    def get_queryset(self):

        queryset = Product.objects.all()

        # Category Filter
        category_id = self.kwargs.get("pk")

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Search
        search = self.request.GET.get("search")

        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset
# ==========================
# Product Detail
# ==========================

class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"


# ==========================
# Add To Cart
# ==========================

@login_required
def add_to_cart(request, pk):

    product = get_object_or_404(Product, pk=pk)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")


# ==========================
# Remove From Cart
# ==========================

@login_required
def remove_from_cart(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    cart_item.delete()

    return redirect("cart")


# ==========================
# Cart View
# ==========================

@method_decorator(login_required, name="dispatch")
class CartView(TemplateView):

    template_name = "cart.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        cart, created = Cart.objects.get_or_create(
            user=self.request.user
        )

        cart_items = CartItem.objects.filter(cart=cart)

        grand_total = 0

        for item in cart_items:

    

            grand_total += item.total_price

        context["cart_items"] = cart_items
        context["grand_total"] = grand_total

        return context


# ==========================
# Checkout
# ==========================

@login_required
def checkout(request):

    cart = get_object_or_404(Cart, user=request.user)

    cart_items = CartItem.objects.filter(cart=cart)

    grand_total = 0

    for item in cart_items:

       
        grand_total += item.total_price

    if request.method == "POST":

        Order.objects.create(
            user=request.user,
            name=request.POST["name"],
            phone=request.POST["phone"],
            address=request.POST["address"],
            city=request.POST["city"],
            pincode=request.POST["pincode"],
            total_amount=grand_total,
            payment_method="COD",
            payment_status=False,
            order_status="Pending",
        )

        cart_items.delete()

        return redirect("payment")

    context = {
        "cart_items": cart_items,
        "grand_total": grand_total,
    }

    return render(request, "checkout.html", context)


# ==========================
# Payment
# ==========================

@login_required
def payment(request):

    order = Order.objects.filter(
        user=request.user
    ).order_by("-created_at").first()

    if not order:
        return redirect("cart")

    if request.method == "POST":

        method = request.POST.get("payment_method")

        order.payment_method = method

        if method == "COD":
            order.payment_status = False
        else:
            order.payment_status = True

        order.save()
        send_mail(
    subject="Order Confirmation - GadgetHub",
    message=f"""
Dear {request.user.first_name or request.user.username},

Thank you for shopping with GadgetHub.

Your order has been placed successfully.

Order ID : {order.id}
Total Amount : ₹{order.total_amount}
Payment Method : {order.payment_method}
Order Status : {order.order_status}

We will notify you once your order is shipped.

Thank you,
GadgetHub Team
""",
    from_email=settings.EMAIL_HOST_USER,
    recipient_list=[request.user.email],
    fail_silently=False,
)

        return redirect("order-success")

    return render(
        request,
        "payment.html",
        {
            "order": order
        }
    )
# ==========================
# Orders
# ==========================

@login_required
def orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "orders.html",
        {
            "orders": orders
        }
    )


# ==========================
# Add Review
# ==========================

@login_required
def add_review(request, pk):

    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":

        Review.objects.create(
            product=product,
            user=request.user,
            rating=request.POST["rating"],
            comment=request.POST["comment"]
        )

    return redirect("product-detail", pk=pk)


# ==========================
# Add to Wishlist
# ==========================

@login_required
def add_to_wishlist(request, pk):

    product = get_object_or_404(Product, pk=pk)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect("product-detail", pk=pk)


# ==========================
# Remove from Wishlist
# ==========================

@login_required
def remove_from_wishlist(request, pk):

    wishlist_item = get_object_or_404(
        Wishlist,
        id=pk,
        user=request.user
    )

    wishlist_item.delete()

    return redirect("wishlist")


# ==========================
# Wishlist Page
# ==========================

@login_required
def wishlist(request):

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    )

    return render(
        request,
        "wishlist.html",
        {
            "wishlist_items": wishlist_items
        }
    )

# ==========================
# Buy Now
# ==========================

@login_required
def buy_now(request, pk):

    product = get_object_or_404(Product, pk=pk)

    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Remove previous cart items
    CartItem.objects.filter(cart=cart).delete()

    # Add the selected product
    CartItem.objects.create(
        cart=cart,
        product=product,
        quantity=1
    )

    # Go to checkout page
    return redirect("checkout")


# ==========================
# Order Success
# ==========================

@login_required
def order_success(request):

    order = Order.objects.filter(
        user=request.user
    ).order_by("-created_at").first()

    return render(
        request,
        "order_success.html",
        {
            "order": order
        }
    )


@login_required
def profile(request):

    orders = Order.objects.filter(user=request.user)
    wishlist = Wishlist.objects.filter(user=request.user)
    cart = Cart.objects.filter(user=request.user).first()

    cart_count = 0

    if cart:
        cart_count = CartItem.objects.filter(cart=cart).count()

    context = {
        "orders_count": orders.count(),
        "wishlist_count": wishlist.count(),
        "cart_count": cart_count,
    }

    return render(request, "profile.html", context)
# ==========================
# My Profile
# ==========================

@login_required
def profile(request):

    user = request.user

    orders = Order.objects.filter(user=user)
    wishlist = Wishlist.objects.filter(user=user)

    cart = Cart.objects.filter(user=user).first()

    cart_count = 0

    if cart:
        cart_count = CartItem.objects.filter(cart=cart).count()

    context = {

        # User Information
        "user": user,

        # Statistics
        "orders_count": orders.count(),
        "wishlist_count": wishlist.count(),
        "cart_count": cart_count,

    }

    return render(
        request,
        "profile.html",
        context
    )


@login_required
def edit_profile(request):

    if request.method == "POST":

        form = ProfileUpdateForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()
            return redirect("profile")

    else:

        form = ProfileUpdateForm(
            instance=request.user
        )

    return render(
        request,
        "edit_profile.html",
        {
            "form": form
        }
    )
# ==========================
# Invoice
# ==========================

@login_required
def invoice(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "invoice.html",
        {
            "order": order
        }
    )
@login_required
def invoice(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )
    return render(request, "invoice.html", {"order": order})
# ==========================
# Admin Dashboard
# ==========================

@staff_member_required
def admin_dashboard(request):

    total_products = Product.objects.count()

    total_categories = Category.objects.count()

    total_orders = Order.objects.count()

    total_users = User.objects.count()

    total_reviews = Review.objects.count()

    total_wishlist = Wishlist.objects.count()

    total_revenue = Order.objects.filter(
        payment_status=True
    ).aggregate(
        Sum("total_amount")
    )["total_amount__sum"] or 0

    pending_orders = Order.objects.filter(
        order_status="Pending"
    ).count()

    delivered_orders = Order.objects.filter(
        order_status="Delivered"
    ).count()

    context = {
        "total_products": total_products,
        "total_categories": total_categories,
        "total_orders": total_orders,
        "total_users": total_users,
        "total_reviews": total_reviews,
        "total_wishlist": total_wishlist,
        "total_revenue": total_revenue,
        "pending_orders": pending_orders,
        "delivered_orders": delivered_orders,
    }

    return render(request, "admin_dashboard.html", context)