from .models import Cart, Wishlist

def cart_count(request):
    cart_count = 0
    wishlist_count = 0

    if request.user.is_authenticated:

        # Cart Count
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = cart.items.count()
        except Cart.DoesNotExist:
            cart_count = 0

        # Wishlist Count
        wishlist_count = Wishlist.objects.filter(
            user=request.user
        ).count()

    return {
        "cart_count": cart_count,
        "wishlist_count": wishlist_count,
    }