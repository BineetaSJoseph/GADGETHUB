from django.urls import path
from .views import (
    HomeView,
    AboutView,
    ContactView,
    UserLoginView,
    UserLogoutView,
    SignUpView,
    ProductListView,
    ProductDetailView,
    add_to_cart,
    CartView,
    remove_from_cart,
    checkout,
    payment,
    orders,
    add_review,
    add_to_wishlist,
    remove_from_wishlist,
    wishlist,
    buy_now,
    order_success,
    profile,
    edit_profile,invoice,
    admin_dashboard,
)

urlpatterns = [

    # ==========================
    # Home
    # ==========================
    path("", HomeView.as_view(), name="home"),

    # ==========================
    # Static Pages
    # ==========================
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),

    # ==========================
    # Authentication
    # ==========================
    path("login/", UserLoginView.as_view(), name="login"),
    
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),

    # ==========================
    # Products
    # ==========================
    path(
        "products/",
        ProductListView.as_view(),
        name="product-list",
    ),

    path(
        "products/category/<int:pk>/",
        ProductListView.as_view(),
        name="category-products",
    ),

    path(
        "product/<int:pk>/",
        ProductDetailView.as_view(),
        name="product-detail",
    ),

    # ==========================
    # Buy Now
    # ==========================
    path(
        "buy-now/<int:pk>/",
        buy_now,
        name="buy-now",
    ),

    # ==========================
    # Cart
    # ==========================
    path(
        "add-to-cart/<int:pk>/",
        add_to_cart,
        name="add-to-cart",
    ),

    path(
        "cart/",
        CartView.as_view(),
        name="cart",
    ),

    path(
        "remove-from-cart/<int:item_id>/",
        remove_from_cart,
        name="remove-from-cart",
    ),

    # ==========================
    # Checkout
    # ==========================
    path(
        "checkout/",
        checkout,
        name="checkout",
    ),

    # ==========================
    # Payment
    # ==========================
    path(
        "payment/",
        payment,
        name="payment",
    ),

    # ==========================
    # Order Success
    # ==========================
    path(
        "order-success/",
        order_success,
        name="order-success",
    ),

    # ==========================
    # Orders
    # ==========================
    path(
        "orders/",
        orders,
        name="orders",
    ),

    # ==========================
    # Reviews
    # ==========================
    path(
        "product/<int:pk>/review/",
        add_review,
        name="add-review",
    ),

    # ==========================
    # Wishlist
    # ==========================
    path(
        "wishlist/",
        wishlist,
        name="wishlist",
    ),

    path(
        "wishlist/add/<int:pk>/",
        add_to_wishlist,
        name="add-to-wishlist",
    ),

    path(
        "wishlist/remove/<int:pk>/",
        remove_from_wishlist,
        name="remove-from-wishlist",
    ),
    path(
    "profile/",
    profile,
    name="profile",
),
path(
    "profile/edit/",
    edit_profile,
    name="edit-profile",
),
path(
    "invoice/<int:order_id>/",
    invoice,
    name="invoice",
),
path(
    "admin-dashboard/",
    admin_dashboard,
    name="admin-dashboard",
),

]