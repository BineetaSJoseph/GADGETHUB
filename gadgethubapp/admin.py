from django.contrib import admin
from .models import Category, Product,Cart,CartItem,Order,Review,Wishlist


# Category Admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


# Product Admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'discount_price', 'stock', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "total_amount",
        "payment_method",
        "payment_status",
        "order_status",
        "created_at",
    )
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "user",
        "rating",
        "created_at",
    )

class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "total_amount",
        "payment_method",
        "payment_status",
        "order_status",
        "created_at",
    )

    list_filter = (
        "order_status",
        "payment_method",
        "payment_status",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    ordering = ("-created_at",)
admin.site.register(Review, ReviewAdmin)


admin.site.register(Order, OrderAdmin)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Wishlist)