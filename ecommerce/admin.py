from django.contrib import admin
from .models import SuperCategory, MainCategory, SubCategory, MiniCategory,Product,ProductRating,Order,OrderDetails,Coupon,Payment,OrderSupplier,OrderDetailsSupplier

# class Inline_MainCategoryAdmin(admin.StackedInline):
#     model = MainCategory
#     extra = 0
#     #readonly_fields = ("name",)
#     list_display = ('id', 'name',)
#     list_filter = ('name',)
#     list_editable = ("name",)
#     list_display_links = ("id", )
#     list_per_page = 10
#     search_fields = ('name', )


# class SuperCategoryAdmin(admin.ModelAdmin):
#     #fields = ("","")
#     inlines = [Inline_MainCategoryAdmin, ]
#     list_display = ('id', 'name',)
#     list_filter = ('name',)
#     #list_editable = ("name",)
#     list_display_links = ("id", )
#     list_per_page = 10
#     search_fields = ('name', )


# class Inline_SubCategoryAdmin(admin.StackedInline):
#     model = SubCategory
#     extra = 0
#     #readonly_fields = ("name",)
#     list_display = ('id', 'name',)
#     list_filter = ('name',)
#     list_editable = ("name",)
#     list_display_links = ("id", )
#     list_per_page = 10
#     search_fields = ('name', )


# class MainCategoryAdmin(admin.ModelAdmin):
#     #fields = ("","")
#     inlines = [Inline_SubCategoryAdmin, ]
#     list_display = ('id', 'name',)
#     list_filter = ('name',)
#     #list_editable = ("name",)
#     list_display_links = ("id", )
#     list_per_page = 10
#     search_fields = ('name', )


# class Inline_MiniCategoryAdmin(admin.StackedInline):
#     model = MiniCategory
#     extra = 0
#     #readonly_fields = ("name",)
#     list_display = ('id', 'name',)
#     list_filter = ('name',)
#     list_editable = ("name",)
#     list_display_links = ("id", )
#     list_per_page = 10
#     search_fields = ('name', )


# class SubCategoryAdmin(admin.ModelAdmin):
#     #fields = ("","")
#     inlines = [Inline_MiniCategoryAdmin, ]
#     list_display = ('id', 'name',)
#     list_filter = ('name',)
#     #list_editable = ("name",)
#     list_display_links = ("id", )
#     list_per_page = 10
#     search_fields = ('name', )


admin.site.register(SuperCategory,)
admin.site.register(MainCategory,)
admin.site.register(SubCategory,)
admin.site.register(MiniCategory,)
admin.site.register(Product,)
admin.site.register(ProductRating,)
admin.site.register(Order,)
admin.site.register(OrderDetails,)
admin.site.register(Coupon,)
admin.site.register(Payment,)
admin.site.register(OrderSupplier,)
admin.site.register(OrderDetailsSupplier,)



