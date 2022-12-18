from django.shortcuts import redirect, render,get_object_or_404
from management.models import User,Profile
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from .forms import *
from django.contrib import messages
from .models import OrderDetailsSupplier, SubCategory,MainCategory,MiniCategory,SuperCategory,VendorPayments
# from django.views.generic import View
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from .models import Product,ProductRating,Order,OrderDetails,Coupon,Payment,Country,OrderSupplier,BankAccount
from django.db.models import Sum
from django.conf import settings
from django.views import View
from django.views.decorators.http import require_POST
import requests
from bs4 import BeautifulSoup
import datetime
from django_countries import countries as allcountries
import razorpay
from .utils import code_generator
import stripe
from django.core.mail import send_mail
from decimal import Context, Decimal
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage







# Create your views here

def listing_product(request):
    products=list(Product.objects.all().filter(product_vendor=request.user.profile))
    return render(request,'ecommerce/listing-product.html',{'products':products})


def add_product(request):
    if request.method=='POST':
        form=Product_forms(request.POST,request.FILES)
        if form.is_valid():
            product=form.save(commit=False)
            product.product_vendor=request.user.profile
            product.save()
            messages.success(request,'Product added succesfully !')
            form=Product_forms()
            return redirect('/add-product')
    form=Product_forms()  
    return render(request,'ecommerce/add-product.html',{'form':form})


def edit_product(request,slug):
    if request.method=='POST':
        product=Product.objects.get(PRDSlug=slug)
        form=Product_forms(request.POST,request.FILES,instance=product)
        if form.is_valid():
            prod=form.save(commit=False)
            prod.product_vendor=request.user.profile
            prod.save()
            messages.success(request,'Product edited successfully !')
    product=Product.objects.get(PRDSlug=slug)
    print(product)
    form=Product_forms(instance=product)
    return render(request,'ecommerce/edit-product.html',{'form':form})    


def home(request):
    products=Product.objects.all()
    return render(request,'ecommerce/shop.html',{'products':products})    

def shop(request):

    return render(request, "ecommerce/shop-grid-left.html")


def super_category(request, slug):

    super_category_obj = SuperCategory.objects.get(slug=slug)
    main_category_obj = MainCategory.objects.all().filter(
        super_category=super_category_obj)

    context = {
        "main_category_obj": main_category_obj,
        "super_category_obj": super_category_obj,
        "slug": slug,

    }
    return render(request, "ecommerce/shop-super-category.html", context)


def main_category(request, slug):

    main_category_obj = MainCategory.objects.get(slug=slug)
    sub_category_obj = SubCategory.objects.all().filter(
        main_category=main_category_obj)

    context = {
        "sub_category_obj": sub_category_obj,
        "main_category_obj": main_category_obj,
        "slug": slug,
    }
    return render(request, "ecommerce/shop-main-category.html", context)


def sub_category(request, slug):

    sub_category_obj = SubCategory.objects.get(slug=slug)
    mini_category_obj = MiniCategory.objects.all().filter(
        sub_category=sub_category_obj)

    context = {
        "mini_category_obj": mini_category_obj,
        "sub_category_obj": sub_category_obj,
        "slug": slug,
    }
    return render(request, "ecommerce/shop-sub-category.html", context)


def category_list(request):
    supercategory = SuperCategory.objects.all()
    maincategory = MainCategory.objects.all()
    subcategory = SubCategory.objects.all()
    minicategory = MiniCategory.objects.all()
    context = {
        'supercategory': supercategory,
        'maincategory': maincategory,
        'subcategory': subcategory,
        'minicategory': minicategory,
    }

    return render(request, "ecommerce/category-list.html", context)


class CategoryJsonListView(View):
    def get(self, *args, **kwargs):

        upper = int(self.request.GET.get("num_products"))
        orderd_by = self.request.GET.get("order_by")
        CAT_id = self.request.GET.get("CAT_id")
        CAT_type = self.request.GET.get("cat_type")

        if CAT_type == "all":
            lower = upper - 10
            # print(lower, upper)
            products = list(
                Product.objects.all().filter(PRDISDeleted = False , PRDISactive = True ).values().order_by(orderd_by)[lower:upper])
            products_size = len(Product.objects.all().filter(PRDISDeleted = False , PRDISactive = True ))
            max_size = True if upper >= products_size else False
            return JsonResponse({"data": products,  "max": max_size, "products_size": products_size, }, safe=False)

        else:      # 3
            lower = upper - 10
            # print(lower, upper)
            if CAT_type == "super":

                products = list(
                    Product.objects.all().filter(product_supercategory=int(CAT_id), PRDISDeleted = False , PRDISactive = True ).values().order_by(orderd_by)[lower:upper])
                products_size = len(
                    Product.objects.all().filter(product_supercategory=int(CAT_id), PRDISDeleted = False , PRDISactive = True ))
            elif CAT_type == "main":
                products = list(
                    Product.objects.all().filter(product_maincategory=int(CAT_id), PRDISDeleted = False , PRDISactive = True ).values().order_by(orderd_by)[lower:upper])
                products_size = len(
                    Product.objects.all().filter(product_maincategory=int(CAT_id), PRDISDeleted = False , PRDISactive = True ))
            elif CAT_type == "sub":
                products = list(
                    Product.objects.all().filter(product_subcategory=int(CAT_id), PRDISDeleted = False , PRDISactive = True ).values().order_by(orderd_by)[lower:upper])
                products_size = len(
                    Product.objects.all().filter(product_subcategory=int(CAT_id), PRDISDeleted = False , PRDISactive = True ))

            else:
                products = list(
                    Product.objects.all().filter(product_minicategor=int(CAT_id), PRDISDeleted = False , PRDISactive = True ).values().order_by(orderd_by)[lower:upper])
                products_size = len(
                    Product.objects.all().filter(product_minicategor=int(CAT_id), PRDISDeleted = False , PRDISactive = True ))

            max_size = True if upper >= products_size else False
            return JsonResponse({"data": products, "max": max_size, "products_size": products_size, }, safe=False)


def product_details(request, slug):
    # if not request.session.has_key('currency'):
    #     request.session['currency'] = settings.DEFAULT_CURRENCY

    product_detail = get_object_or_404(Product, PRDSlug=slug, PRDISactive=True)
    # product_image = ProductImage.objects.all().filter(PRDIProduct=product_detail)
    related_products_minicategor = product_detail.product_minicategor
    related_products = Product.objects.all().filter(
        product_minicategor=related_products_minicategor, PRDISactive=True)
    supplier_Products = Product.objects.all().filter(product_vendor=product_detail.product_vendor,
                                                     product_minicategor=related_products_minicategor, PRDISactive=True)

    # related = ProductAlternative.objects.all().filter(PALNProduct=product_detail)
    # related_products = product_detail.alternative_products.all()

    product_feedback = ProductRating.objects.all().filter(
        PRDIProduct=product_detail, active=True)
    feedback_sum = ProductRating.objects.all().filter(
        PRDIProduct=product_detail, active=True).aggregate(Sum('rate'))
    feedbak_number = product_feedback.count()
    
    try:

        average_rating = int(feedback_sum["rate__sum"]) / feedbak_number

        start_1_sum =  ProductRating.objects.all().filter(
            PRDIProduct=product_detail, active=True , rate = 1).count()

        start_2_sum =  ProductRating.objects.all().filter(
            PRDIProduct=product_detail, active=True , rate = 2).count()

        start_3_sum =  ProductRating.objects.all().filter(
            PRDIProduct=product_detail, active=True , rate = 3).count()

        start_4_sum =  ProductRating.objects.all().filter(
            PRDIProduct=product_detail, active=True , rate = 4).count()
            
        start_5_sum =  ProductRating.objects.all().filter(
            PRDIProduct=product_detail, active=True , rate = 5).count()
        
        

        start_1 = (start_1_sum/ feedbak_number) * 100
        start_2 = (start_2_sum / feedbak_number) * 100
        start_3 = (start_3_sum / feedbak_number) * 100
        start_4 = (start_4_sum / feedbak_number) * 100
        start_5 = (start_5_sum / feedbak_number) * 100

    except:
        average_rating = 0
        start_1 = 0
        start_2 = 0
        start_3 = 0
        start_4 = 0
        start_5 = 0

    context = {
        'product_detail': product_detail,
        # 'product_image': product_image,
        'related_products': related_products,
        'supplier_Products': supplier_Products,
        # 'related_products': related_products,
        'product_feedback': product_feedback,
        'average_rating': average_rating,
        'feedbak_number': feedbak_number,
        "start_1":start_1,
        "start_2":start_2,
        "start_3":start_3,
        "start_4":start_4,
        "start_5":start_5,

    }
    return render(request, 'ecommerce/shop-product-details.html', context)




def product_rating(request):
    if request.method == "POST" and request.user.is_authenticated and not request.user.is_anonymous:
        product_id = request.POST.get("product_id")
        product_rate = request.POST.get("product_rate")
        print(product_rate)
        #print(type(product_rate))
        message = request.POST.get("client_message")
        client = Profile.objects.get(user = request.user)
        if request.is_ajax():
            product = Product.objects.get(id=product_id)

            if ProductRating.objects.all().filter(PRDIProduct=product, client_name__user=request.user).exists():
                old_rating = ProductRating.objects.get(
                    PRDIProduct=product, client_name__user=request.user)
                old_rating.vendor = product.product_vendor    
                # old_rating.rate = product_rate
                old_rating.client_name=client
                old_rating.client_comment = message
                old_rating.save()

                product_feedback = ProductRating.objects.all().filter(
                    PRDIProduct=product, active=True)
                feedback_sum = ProductRating.objects.all().filter(
                    PRDIProduct=product, active=True).aggregate(Sum('rate'))
                feedbak_number = product_feedback.count()
                try:
                    if feedback_sum != None or feedback_sum != 0:
                        average_rating =round(( int(feedback_sum["rate__sum"]) / feedbak_number) * 20)
                        product.feedbak_average = average_rating
                        product.feedbak_number  = feedbak_number
                        product.save()

                except:
                    pass

            else:
                ProductRating.objects.create(
                    PRDIProduct=product,
                    vendor = product.product_vendor ,
                    rate=product_rate,
                    client_name=client,

                    client_comment=message,
                )

                product_feedback = ProductRating.objects.all().filter(
                    PRDIProduct=product, active=True)
                feedback_sum = ProductRating.objects.all().filter(
                    PRDIProduct=product, active=True).aggregate(Sum('rate'))
                feedbak_number = product_feedback.count()
                try:
                    if feedback_sum != None or feedback_sum != 0:
                        average_rating = round(( int(feedback_sum["rate__sum"]) / feedbak_number * 20))
                        product.feedbak_average = average_rating
                        product.feedbak_number  = feedbak_number
                        product.save() 

                except:
                    product.feedbak_average = int(product_rate) * 20
                    product.feedbak_number  = 1
                    product.save()    
                
            return JsonResponse({"succes": True, "product_id": product_id, "product_rate": product_rate, }, safe=False)
        return JsonResponse({"succes": False, }, safe=False)         


###-----------------------------------------------order-------------------------------------------###
ts = datetime.datetime.now().timestamp()
time = round(ts * 1000)


def add_to_cart(request):
    if not request.session.has_key('currency'):
        request.session['currency'] = settings.DEFAULT_CURRENCY

    if "qyt" in request.POST and "product_id" in request.POST and "product_Price" in request.POST:

        product_id = request.POST['product_id']
        qyt = int(request.POST['qyt'])
        print(qyt)
        size = None
        if "size" in request.POST:
            size = request.POST['size']
            # print(request.POST['size'])
        product = Product.objects.get(id=product_id)

        if qyt <= 0 and product.available == 0:
            messages.warning(request, 'This product is out of stock !')
            return redirect('/cart')

        if product.available < qyt and product.available == 0:
            messages.warning(request, 'This product is out of stock !')
            return redirect('/cart')

        if qyt <= 0 and product.available != 0:
            qyt = 1

        if product.available < qyt and product.available != 0:
            qyt = product.available

        try:
            if request.user.is_authenticated and not request.user.is_anonymous:
                order = Order.objects.filter(
                    user=request.user, is_finished=False).first()
                print("order: ", order)
            else:
                cart_id = request.session.get('cart_id')
                order = Order.objects.all().filter(id=cart_id, is_finished=False)

        except:
            order = False

        if not Product.objects.all().filter(id=product_id).exists():
            return HttpResponse(f"this product not found !")

        if order:
            if request.user.is_authenticated and not request.user.is_anonymous:
                old_orde = Order.objects.filter(
                    user=request.user, is_finished=False).first()
            else:
                old_orde = Order.objects.get(id=cart_id, is_finished=False)
            # old_orde_supplier = OrderSupplier.objects.get(
            #     user=request.user, is_finished=False, order=old_orde)
            # print("old_orde_supplier:", old_orde_supplier)
            if OrderDetails.objects.all().filter(order=old_orde, product=product).exists() and OrderDetailsSupplier.objects.all().filter(order=old_orde, product=product).exists():
                item = OrderDetails.objects.get(
                    order=old_orde, product=product)
                item_supplier = OrderDetailsSupplier.objects.get(
                    order=old_orde, product=product)
                # for i in items:
                if item.quantity >= product.available:
                    qyt = item.quantity
                    # i.quantity = int(qyt)
                    # i.save()
                    messages.warning(
                        request, f"You can't add more from this product, available only : {qyt}")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

                elif qyt < product.available:
                    qyt = qyt + item.quantity
                    if qyt > product.available:
                        qyt = product.available

                    item.quantity = int(qyt)
                    item_supplier.quantity = int(qyt)
                    item.save()
                    item_supplier.save()

                    # code for total amount main order
                    order_details_main = OrderDetails.objects.all().filter(order=old_orde)
                    f_total = 0
                    w_total = 0
                    weight = 0
                    for sub in order_details_main:
                        f_total += sub.price * sub.quantity
                        w_total += sub.weight * sub.quantity
                        total = f_total
                        weight = w_total

                    old_orde.sub_total = f_total
                    old_orde.weight = weight
                    old_orde.amount = total
                    old_orde.save()

                    # code for total amount supplier order
                    old_order_supplier = OrderSupplier.objects.get(
                        is_finished=False, order=old_orde, vendor=product.product_vendor)
                    order_supplier = OrderDetailsSupplier.objects.all().filter(
                        order_supplier=old_order_supplier)
                    weight = 0
                    f_total = 0
                    w_total = 0
                    for sub in order_supplier:
                        f_total += sub.price * sub.quantity
                        w_total += sub.weight * sub.quantity
                        total = f_total
                        weight = w_total
                    old_order_supplier.weight = weight
                    old_order_supplier.amount = total
                    old_order_supplier.save()

                # if i.size != size:
                #     order_details = OrderDetails.objects.create(
                #         supplier=product.product_vendor.user,
                #         product=product,
                #         order=old_orde,
                #         price=product.PRDPrice,
                #         quantity=qyt,
                #         size=size,
                #         weight=product.PRDWeight

                #     )
                #     break

                else:
                    item.quantity = int(qyt)
                    item_supplier.quantity = int(qyt)
                    # i.supplier = product.product_vendor.user
                    item.save()
                    item_supplier.save()

                    # code for total amount main order
                    order_details_main = OrderDetails.objects.all().filter(order=old_orde)
                    f_total = 0
                    w_total = 0
                    weight = 0
                    for sub in order_details_main:
                        f_total += sub.price * sub.quantity
                        w_total += sub.weight * sub.quantity
                        total = f_total
                        weight = w_total

                    old_orde.sub_total = f_total
                    old_orde.weight = weight
                    old_orde.amount = total
                    old_orde.save()

                    # code for total amount supplier order
                    old_order_supplier = OrderSupplier.objects.get(
                        is_finished=False, order=old_orde, vendor=product.product_vendor)
                    order_supplier = OrderDetailsSupplier.objects.all().filter(
                        order_supplier=old_order_supplier)

                    f_total = 0
                    w_total = 0
                    weight = 0
                    for sub in order_supplier:
                        f_total += sub.price * sub.quantity
                        w_total += sub.weight * sub.quantity
                        total = f_total
                        weight = w_total
                    old_order_supplier.weight = weight
                    old_order_supplier.amount = total
                    old_order_supplier.save()

            else:
                order_details = OrderDetails.objects.create(
                    supplier=product.product_vendor.user,
                    product=product,
                    order=old_orde,
                    price=product.PRDPrice,
                    quantity=qyt,
                    size=size,
                    weight=product.PRDWeight
                )
                # code for total amount main order

                order_details_main = OrderDetails.objects.all().filter(order=old_orde)
                weight = 0
                f_total = 0
                w_total = 0
                for sub in order_details_main:
                    f_total += sub.price * sub.quantity
                    w_total += sub.weight * sub.quantity
                    total = f_total
                    weight = w_total

                old_orde.sub_total = f_total
                old_orde.weight = weight
                old_orde.amount = total
                old_orde.save()
                # add product for old order supplier
                if OrderSupplier.objects.all().filter(
                        order=old_orde, is_finished=False, vendor=product.product_vendor).exists():
                    old_order_supplier = OrderSupplier.objects.get(
                        is_finished=False, order=old_orde, vendor=product.product_vendor)
                    order_details_supplier = OrderDetailsSupplier.objects.create(
                        supplier=product.product_vendor.user,
                        product=product,
                        order=old_orde,
                        order_supplier=old_order_supplier,
                        order_details=order_details,
                        price=product.PRDPrice,
                        quantity=qyt,
                        size=size,
                        weight=product.PRDWeight
                    )

                    # code for total amount supplier order
                    order__supplier = OrderDetailsSupplier.objects.all().filter(
                        order_supplier=old_order_supplier)
                    f_total = 0
                    w_total = 0
                    weight = 0
                    for sub in order__supplier:
                        f_total += sub.price * sub.quantity
                        w_total += sub.weight * sub.quantity
                        total = f_total
                        weight = w_total
                    old_order_supplier.weight = weight
                    old_order_supplier.amount = total
                    old_order_supplier.save()

                else:
                    # order for  new supllier
                    new_order_supplier = OrderSupplier()
                    if request.user.is_authenticated and not request.user.is_anonymous:
                        new_order_supplier.user = request.user
                        new_order_supplier.email_client = request.user.email

                    new_order_supplier.vendor = product.product_vendor
                    new_order_supplier.order = old_orde
                    new_order_supplier.save()
                    order_details_supplier = OrderDetailsSupplier.objects.create(
                        supplier=product.product_vendor.user,
                        product=product,
                        order=old_orde,
                        order_supplier=new_order_supplier,
                        order_details=order_details,
                        price=product.PRDPrice,
                        quantity=qyt,
                        size=size,
                        weight=product.PRDWeight
                    )

                    order_supplier = OrderDetailsSupplier.objects.all().filter(
                        order_supplier=new_order_supplier)
                    weight = 0
                    f_total = 0
                    w_total = 0
                    for sub in order_supplier:
                        f_total += sub.price * sub.quantity
                        w_total += sub.weight * sub.quantity
                        total = f_total
                        weight = w_total
                    new_order_supplier.weight = weight
                    new_order_supplier.amount = total
                    new_order_supplier.save()

            messages.success(request, 'product has been added to cart !')
            # return redirect('orders:cart')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:
            # order for all
            new_order = Order()
            if request.user.is_authenticated and not request.user.is_anonymous:
                new_order.user = request.user
                new_order.email_client = request.user.email

            new_order.save()
            # will edite
            # new_order.supplier = product.product_vendor.user
            # new_order.vendors.add(product.product_vendor)

            # order for supllier
            new_order_supplier = OrderSupplier()
            if request.user.is_authenticated and not request.user.is_anonymous:
                new_order_supplier.user = request.user
                new_order_supplier.email_client = request.user.email

            new_order_supplier.vendor = product.product_vendor
            new_order_supplier.order = new_order
            new_order_supplier.save()

            order_details = OrderDetails.objects.create(
                supplier=product.product_vendor.user,
                product=product,
                order=new_order,
                price=product.PRDPrice,
                quantity=qyt,
                size=size,
                weight=product.PRDWeight
            )

            order_details_supplier = OrderDetailsSupplier.objects.create(
                supplier=product.product_vendor.user,
                product=product,
                order=new_order,
                order_supplier=new_order_supplier,
                order_details=order_details,
                price=product.PRDPrice,
                quantity=qyt,
                size=size,
                weight=product.PRDWeight
            )
            # code for total amount main order

            order_details_main = OrderDetails.objects.all().filter(order=new_order)
            f_total = 0
            w_total = 0
            weight = 0
            for sub in order_details_main:
                f_total += sub.price * sub.quantity
                w_total += sub.weight * sub.quantity
                total = f_total
                weight = w_total

            new_order.sub_total = f_total
            new_order.weight = weight
            new_order.amount = total
            new_order.save()
            # code for total amount supplier order
            order_details__supplier = OrderDetailsSupplier.objects.all().filter(
                order_supplier=new_order_supplier)
            f_total = 0
            w_total = 0
            weight = 0
            for sub in order_details__supplier:
                f_total += sub.price * sub.quantity
                w_total += sub.weight * sub.quantity
                total = f_total
                weight = w_total
            new_order_supplier.weight = weight
            new_order_supplier.amount = total
            new_order_supplier.save()
            request.session['cart_id'] = new_order.id
            messages.success(request, 'product has been added to cart !')
            # return redirect('orders:cart')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.warning(
            request, 'You must first log in to your account to purchase the product')
        return redirect('/login')


def cart(request):
    if not request.session.has_key('currency'):
        request.session['currency'] = settings.DEFAULT_CURRENCY

    if "code" in request.POST:
        now = timezone.now()
        code = request.POST['code']
        request.session['code'] = code
        coupon = None
        if Coupon.objects.all().filter(code=code, active=True):
            coupon = Coupon.objects.get(code=code, active=True)
            request.session['coupon_id'] = coupon.id
            messages.success(
                request, 'Discount code has been added successfully ')

        else:
            messages.warning(
                request, 'The discount code is not available or has expired ')
            request.session['coupon_id'] = None
            # request.session['code'] = None
        return redirect('/cart')

    context = None
    PUBLIC_KEY = settings.STRIPE_PUBLIC_KEY
    # if request.user.is_authenticated and not request.user.is_anonymous:
    # countries = Country.objects.all().filter().order_by('-name_country')
    countries = allcountries
    first_country = Country.objects.all(
    ).filter().order_by('-name_country')[0:1]
    # states = State.objects.filter(country=first_country)

    try:
        if request.user.is_authenticated and not request.user.is_anonymous:
            order_view = Order.objects.all().filter(
                user=request.user, is_finished=False).first()
            request.session['cart_id'] = order_view.id
        else:
            cart_id = request.session.get('cart_id')
            order_view = Order.objects.all().filter(id=cart_id, is_finished=False)

    except:
        order_view = False

    if order_view:
        try:
            blance = Profile.objects.get(user=request.user).blance

        except:
            blance = 0

        if request.user.is_authenticated and not request.user.is_anonymous:
            order = Order.objects.filter(
                user=request.user, is_finished=False).first()
        else:
            order = Order.objects.get(id=cart_id, is_finished=False)

        order_details = OrderDetails.objects.all().filter(order=order)

        coupon_id = None
        value = None
        total = None
        weight = None
        code = None
        f_total = 0
        w_total = 0
        for sub in order_details:
            f_total += sub.price * sub.quantity
            w_total += sub.weight * sub.quantity
            total = f_total
            weight = w_total

        if request.session.get("coupon_id"):
            coupon_id = request.session.get("coupon_id")
            code = request.session.get("code")
            if Coupon.objects.all().filter(id=coupon_id):
                discount = Coupon.objects.get(id=coupon_id).discount
                value = (discount / Decimal("100")) * f_total
                total = f_total-value
                # print(total)

                # order = Order.objects.all().filter(user=request.user, is_finished=False)
                if order:
                    if request.user.is_authenticated and not request.user.is_anonymous:
                        old_orde = Order.objects.get(
                            user=request.user, is_finished=False)
                    else:
                        old_orde = Order.objects.get(
                            id=cart_id, is_finished=False)

                    old_orde.amount = total
                    old_orde.discount = value
                    old_orde.sub_total = f_total
                    # old_orde = weight
                    old_orde.coupon = Coupon.objects.get(id=coupon_id)
                    old_orde.save()

            # else:
            #     total = f_total
            #     coupon_id = None
        else:
            # total = f_total
            # coupon_id = None
            if request.user.is_authenticated and not request.user.is_anonymous:
                old_orde = Order.objects.get(
                    user=request.user, is_finished=False)
            else:
                old_orde = Order.objects.get(
                    id=cart_id, is_finished=False)
            old_orde.amount = total
            old_orde.discount = 0
            old_orde.sub_total = f_total
            old_orde.weight = weight
            old_orde.coupon = None
            # if request.user.is_authenticated and not request.user.is_anonymous:
            #     old_orde.user = request.user
            #     old_orde.email_client = request.user.email
            old_orde.save()

            # print(total)

        # if "coupon_id" in request.session.keys():
        #     del request.session["coupon_id"]

        context = {
            "order": order,
            "order_details": order_details,
            "total": total,
            "f_total": f_total,
            "coupon_id": coupon_id,
            "value": value,
            "code": code,
            "blance": blance,
            "PUBLIC_KEY": PUBLIC_KEY,
            "countries": countries,
            # "states": states,
            "weight": weight,
        }
    return render(request, "ecommerce/shop-cart.html", context)


class StatesJsonListView(View):
    def get(self, *args, **kwargs):
        country = kwargs.get('country')

        states = None
        # country_id = Country.objects.get(country_code=country)

        # qs = list(State.objects.all().filter(country=country_id).values())
        if settings.ARAMEX_USERNAME != "":
            print("true")
            data = {
                'ClientInfo': {
                    "UserName": f"{settings.ARAMEX_USERNAME}",
                    "Password": f"{settings.ARAMEX_PASSWORD}",
                    "Version": f"{settings.ARAMEX_VERSION}",
                    "AccountNumber": f"{settings.ARAMEX_ACCOUNTNUMBER}",
                    "AccountPin": f"{settings.ARAMEX_ACCOUNTPIN}",
                    "AccountEntity": f"{settings.ARAMEX_ACCOUNTENTITY}",
                    "AccountCountryCode": f"{settings.ARAMEX_ACCOUNTCOUNTRYCODE}",
                    "Source": f"{settings.ARAMEX_SOURCE}"


                },
                "Transaction": None,

                "CountryCode": f"{country}"
            }

            url = 'https://ws.aramex.net/ShippingAPI.V2/Location/Service_1_0.svc/xml/FetchStates'
            r = requests.post(url, json=data)
            content = r.text
            soup = BeautifulSoup(content, 'html.parser')
            # print(soup)
            cities_list = []
            cities_tags = soup.find_all("name")
            for city in cities_tags:
                cities_list.append(city.text)
                # print(city.text)
            # print(len(cities_list))

            if len(cities_list) > 0 and len(country) > 0:
                states = cities_list
            else:
                url = 'https://ws.aramex.net/ShippingAPI.V2/Location/Service_1_0.svc/xml/FetchCities'
                r = requests.post(url, json=data)
                # print(r.text)
                content = r.text
                soup = BeautifulSoup(content, 'html.parser')
                cities_tags = soup.find_all("a:string")
                for city in cities_tags:
                    cities_list.append(city.text)
                states = cities_list[0:1000]
                # print(len(cities_list))
        else:
            print("false")
            states = False

        return JsonResponse({"success": True, "data": states}, safe=False)
        # return JsonResponse({"success": False, }, safe=False)


def remove_item(request, productdeatails_id):
    if not request.session.has_key('currency'):
        request.session['currency'] = settings.DEFAULT_CURRENCY

    # if request.user.is_authenticated and not request.user.is_anonymous and productdeatails_id:
    item_id = OrderDetails.objects.get(id=productdeatails_id)
    try:
        cart_id = request.session.get('cart_id')
        if item_id.order.id == request.session.get('cart_id'):
            # if item_id.order.user.id == request.user.id:
            item = OrderDetails.objects.all().filter(order_id=item_id.order_id).count()
            if item-1 == 0:
                # order = Order.objects.all().filter(user=request.user, is_finished=False)
                try:

                    old_orde = Order.objects.get(
                        id=cart_id, is_finished=False)
                    old_orde.delete()
                    messages.warning(request, ' Product has been deleted ')
                    return redirect('/cart')
                except:
                    order_view = False
                if "coupon_id" in request.session.keys():
                    del request.session["coupon_id"]
                messages.warning(request, ' Order has been deleted ')
                return redirect('/cart')
            else:

                all_orders = Order.objects.all().filter(id=cart_id, is_finished=False)
                for x in all_orders:

                    order = Order.objects.get(id=x.id)

                    # if OrderDetails.objects.all().filter(order=order) == item_id.id and OrderDetails.objects.all().filter(order=order).exists():
                    if OrderDetails.objects.all().filter(order=order).exists():
                        old_orde = Order.objects.get(
                            id=cart_id, is_finished=False)

                        item_supplier = OrderDetailsSupplier.objects.get(
                            order_details=item_id)

                        obj_order_supplier = OrderSupplier.objects.get(
                            is_finished=False, order=old_orde, vendor=item_supplier.product.product_vendor)

                        item_supplier = OrderDetailsSupplier.objects.all().filter(
                            order_supplier=obj_order_supplier).count()

                        if item_supplier-1 == 0:

                            obj_order_supplier.delete()
                            item_id.delete()

                            messages.warning(
                                request, ' Order has been deleted ')
                            return redirect('/cart')

                        else:
                            item_id.delete()
                            # code for total order supplier
                            order_details__supplier = OrderDetailsSupplier.objects.all().filter(
                                order_supplier=obj_order_supplier)
                            f_total = 0
                            w_total = 0
                            weight = 0
                            for sub in order_details__supplier:
                                f_total += sub.price * sub.quantity
                                w_total += sub.weight * sub.quantity
                                total = f_total
                                weight = w_total
                            obj_order_supplier.weight = weight
                            obj_order_supplier.amount = total
                            obj_order_supplier.save()
                            messages.warning(
                                request, ' product has been deleted ')
                            # Logically the product is already deleted because of the relationship
                            # item_supplier = OrderDetailsSupplier.objects.get(
                            #     order_details=item_id)
                            # item_supplier.delete()
                            return redirect('orders:cart')
                    else:
                        messages.warning(
                            request, "product You can't delete it !")
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        messages.warning(request, "product You can't delete it !")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def payment(request):
    if not request.session.has_key('currency'):
        request.session['currency'] = settings.DEFAULT_CURRENCY

    context = None
    try:
        shipping = SiteSetting.objects.all().first().shipping
    except:
        shipping = 0

    if settings.STRIPE_PUBLIC_KEY == "" or settings.STRIPE_PUBLIC_KEY == None:
        PUBLIC_KEY = False
    else:
        PUBLIC_KEY = settings.STRIPE_PUBLIC_KEY

    if settings.RAZORPAY_KEY_ID == "" or settings.RAZORPAY_KEY_ID == None:
        RAZORPAY_KEY_ID = False
    else:
        RAZORPAY_KEY_ID = settings.RAZORPAY_KEY_ID

    if settings.API_KEY == "" or settings.API_KEY == None:
        api_key_paymob = False
    else:
        api_key_paymob = settings.API_KEY

    try:
        logo = SiteSetting.objects.first().login_image.url
        # host = request.META.get("HTTP_HOST")
        image = request.scheme+settings.YOUR_DOMAIN+logo
    except:
        image = ""

    # if "vodafone_cash" in request.POST and "pubg_username" in request.POST and "pubg_id" in request.POST and "notes" in request.POST and request.user.is_authenticated and not request.user.is_anonymous:
    if request.method == 'POST':

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        country = request.POST['country']
        try:
            state = request.POST['state']
        except:
            messages.warning(
                request, 'Please contact us because this country is not in our shipping list')
            return redirect(request.META.get('HTTP_REFERER'))

        street_address = request.POST['street']

        ZIP = request.POST['ZIP']
        city = request.POST['city']
        email_address = request.POST['email_address']
        phone = request.POST['phone']

        # return HttpResponse(f"your info is request")
        state_obj = state
        country_obj = dict(allcountries)[str(country)]
        country_code = country
        if country_code == settings.ARAMEX_ACCOUNTCOUNTRYCODE:
            product_group = "DOM"
            product_type = "OND"
        else:
            product_group = "EXP"
            product_type = "PPX"
        # country_obj = Country.objects.get(
        #     country_code=country)
        # country_code = country_obj.country_code
        cart_id = request.session.get('cart_id')
        order_weight = Order.objects.get(
            id=cart_id, is_finished=False).weight
        # print(order_weight)
        if settings.ARAMEX_USERNAME != "":
            data = {
                'ClientInfo': {
                    "UserName": f"{settings.ARAMEX_USERNAME}",
                    "Password": f"{settings.ARAMEX_PASSWORD}",
                    "Version": f"{settings.ARAMEX_VERSION}",
                    "AccountNumber": f"{settings.ARAMEX_ACCOUNTNUMBER}",
                    "AccountPin": f"{settings.ARAMEX_ACCOUNTPIN}",
                    "AccountEntity": f"{settings.ARAMEX_ACCOUNTENTITY}",
                    "AccountCountryCode": f"{settings.ARAMEX_ACCOUNTCOUNTRYCODE}",
                    "Source": f"{settings.ARAMEX_SOURCE}"


                },
                "Transaction": None,
                "DestinationAddress": {
                    "Line1": "",
                    "Line2": "",
                    "Line3": "",
                    "PostCode": ZIP,
                    "City": state,
                    "CountryCode": country_code
                },
                "OriginAddress": {
                    "Line1": "",
                    "Line2": "",
                    "Line3": "",
                    "PostCode": "",
                    "City": "Amman",
                    "CountryCode": "JO"
                },
                "ShipmentDetails": {
                    "Dimensions": None,
                    "DescriptionOfGoods": "",
                    "GoodsOriginCountry": "",
                    "PaymentOptions": "",
                    "PaymentType": "P",
                    "ProductGroup": product_group,
                    "ProductType": product_type,
                    "ActualWeight": {
                        "Value": float(order_weight),
                        "Unit": "KG"
                    },
                    "ChargeableWeight": None,
                    "NumberOfPieces": "1"

                }
            }

            url = 'https://ws.aramex.net/ShippingAPI.V2/RateCalculator/Service_1_0.svc/json/CalculateRate'
            r = requests.post(url, json=data)
            soup = BeautifulSoup(r.content, 'html.parser')
            try:
                if soup.code.string == "ERR01" or soup.code.string == "ERR52" or soup.code.string == "ERR61" or soup.code.string == "ERR04":
                    messages.warning(request, f'{soup.message.string}')
                    return redirect('/cart')
            except:
                pass
            shipping = float(soup.value.string)*1.41
            # print(shipping)
            currency_code = soup.currencycode.string

        order = Order.objects.all().filter(id=cart_id, is_finished=False)

        if order:
            old_orde = Order.objects.get(id=cart_id, is_finished=False)
            # if settings.ARAMEX_USERNAME != "" :
            old_orde.amount = float(old_orde.amount)+shipping
            old_orde.shipping = shipping
            old_orde.save()
            request.session['order_id'] = old_orde.id
            order_details = OrderDetails.objects.all().filter(order=old_orde)
            try:
                if Payment.objects.all().filter(order=old_orde):
                    payment_info = Payment.objects.get(order=old_orde)
                    payment_info.delete()
            except:
                pass
            order_payment = Payment.objects.create(

                order=old_orde,
                first_name=first_name,
                last_name=last_name,
                country=country_obj,
                country_code=country_code,
                state=state_obj,
                street_address=street_address,
                post_code=ZIP,
                # by_blance=notes,
                City=city,
                Email_Address=email_address,
                phone=phone,
            )
            
            if "coupon_id" in request.session.keys():
                del request.session["coupon_id"]

            try:
                blance = float(Profile.objects.get(user=request.user).blance)
            except:
                blance = 0
            order_amount = float(old_orde.amount)
            if Payment.objects.all().filter(order=old_orde):
                payment_info = Payment.objects.get(order=old_orde)
            payment = None
            if RAZORPAY_KEY_ID:
                client = razorpay.Client(
                    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                data = {
                    "amount": float(old_orde.amount) * 7828,
                    "currency": "INR",
                    "receipt": "order_rcptid_11",
                }
                payment = client.order.create(data=data)['id']

            context = {
                "order": old_orde,
                "payment_info": payment_info,
                "order_details": order_details,
                "PUBLIC_KEY": PUBLIC_KEY,
                "blance": blance,
                "order_amount": order_amount,
                "RAZORPAY_KEY_ID": RAZORPAY_KEY_ID,
                'RAZORPAY_order_id': payment,
                "image": image,
                "api_key_paymob": api_key_paymob,

            }
            messages.success(
                request, ' Your Billing Details information has been saved')
            return render(request, "ecommerce/shop-checkout.html", context)

    if request.user.is_authenticated and not request.user.is_anonymous:
        # if Order.objects.all().filter(user=request.user, is_finished=False):
        #     order = Order.objects.get(user=request.user, is_finished=False)

        #     order_details = OrderDetails.objects.all().filter(order=order)
        #     blance = Profile.objects.get(user=request.user).blance
        #     context = {
        #         "order": order,
        #         "order_details": order_details,
        #         "PUBLIC_KEY": PUBLIC_KEY,
        #         "blance": blance,

        #     }
        #     return render(request, "orders/payment.html", context)
        return redirect('/cart')

    messages.success(request, ' There is no order for you to buy it ')
    return redirect('/cart')


def payment_blance(request):
    if not request.user.is_authenticated and request.user.is_anonymous:
        return redirect('/login')

    order = Order.objects.all().filter(user=request.user, is_finished=False)

    if order:
        old_orde = Order.objects.get(user=request.user, is_finished=False)
        try:
            Consignee_id = old_orde.user.id
            Consignee_email = old_orde.user.email
        except:
            pass

        profile = Profile.objects.get(user=request.user)
        if float(old_orde.amount) <= float(profile.blance):
            # print(f"{old_orde.amount} - {profile.blance}")

            # order_payment = Payment.objects.create(

            #     order=old_orde,
            #     by_blance=True
            # )
            payment_method = Payment.objects.get(order=old_orde)
            payment_method.payment_method = "Blance"
            payment_method.save()

            if settings.ARAMEX_USERNAME != "":
                if payment_method.country_code == settings.ARAMEX_ACCOUNTCOUNTRYCODE:
                    product_group = "DOM"
                    product_type = "OND"
                else:
                    product_group = "EXP"
                    product_type = "PPX"
                data = {
                    "ClientInfo": {
                        "UserName": f"{settings.ARAMEX_USERNAME}",
                        "Password": f"{settings.ARAMEX_PASSWORD}",
                        "Version": f"{settings.ARAMEX_VERSION}",
                        "AccountNumber": f"{settings.ARAMEX_ACCOUNTNUMBER}",
                        "AccountPin": f"{settings.ARAMEX_ACCOUNTPIN}",
                        "AccountEntity": f"{settings.ARAMEX_ACCOUNTENTITY}",
                        "AccountCountryCode": f"{settings.ARAMEX_ACCOUNTCOUNTRYCODE}",
                        "Source": f"{settings.ARAMEX_SOURCE}"


                    },

                    "LabelInfo": {
                        "ReportID": 9201,
                        "ReportType": "URL"
                    },
                    "Shipments": [
                        {
                            "Reference1": f"{old_orde}",
                            "Reference2": "",
                            "Reference3": "",
                            "Shipper": {
                                "Reference1": f"{old_orde}",
                                "Reference2": "",
                                "AccountNumber": f"{settings.ARAMEX_ACCOUNTNUMBER}",
                                "PartyAddress": {
                                    "Line1": "Oman",
                                    "Line2": "",
                                    "Line3": "",
                                    "City": "Oman",
                                    "StateOrProvinceCode": "",
                                    "PostCode": "",
                                    "CountryCode": f"{settings.ARAMEX_ACCOUNTCOUNTRYCODE}",
                                    "Longitude": 0,
                                    "Latitude": 0,
                                    "BuildingNumber": None,
                                    "BuildingName": None,
                                    "Floor": None,
                                    "Apartment": None,
                                    "POBox": None,
                                    "Description": "alithemes.com product"
                                },
                                "Contact": {
                                    "Department": "",
                                    "PersonName": "alithemes.com store",
                                    "Title": "",
                                    "CompanyName": "alithemes.com",
                                    "PhoneNumber1": "1111111111",
                                    "PhoneNumber1Ext": "",
                                    "PhoneNumber2": "",
                                    "PhoneNumber2Ext": "",
                                    "FaxNumber": "",
                                    "CellPhone": "1111111111111",
                                    "EmailAddress": "mail@alithemes.com",
                                    "Type": ""
                                }
                            },
                            "Consignee": {
                                "Reference1": f"{Consignee_id}",
                                "Reference2": f"{Consignee_email}",
                                "AccountNumber": f"{Consignee_id}",
                                "PartyAddress": {
                                    "Line1": f"{payment_method.street_address}",
                                    "Line2": "",
                                    "Line3": "",
                                    "City": f"{payment_method.City}",
                                    "StateOrProvinceCode": f"{payment_method.state}",
                                    "PostCode": f"{payment_method.post_code}",
                                    "CountryCode": f"{payment_method.country_code}",
                                    "Longitude": 0,
                                    "Latitude": 0,
                                    "BuildingNumber": "",
                                    "BuildingName": "",
                                    "Floor": "",
                                    "Apartment": "",
                                    "POBox": None,
                                    "Description": "Please contact me when the shipment arrives"
                                },
                                "Contact": {
                                    "Department": "",
                                    "PersonName": f"{payment_method.first_name} {payment_method.last_name}",
                                    "Title": f"{payment_method.last_name}",
                                    "CompanyName": "",
                                    "PhoneNumber1": f"{payment_method.phone}",
                                    "PhoneNumber1Ext": "",
                                    "PhoneNumber2": "",
                                    "PhoneNumber2Ext": "",
                                    "FaxNumber": "",
                                    "CellPhone": f"{payment_method.phone}",
                                    "EmailAddress": f"{payment_method.Email_Address}",
                                    "Type": ""
                                }
                            },
                            "ThirdParty": {
                                "Reference1": "",
                                "Reference2": "",
                                "AccountNumber": "",
                                "PartyAddress": {
                                    "Line1": "",
                                    "Line2": "",
                                    "Line3": "",
                                    "City": "",
                                    "StateOrProvinceCode": "",
                                    "PostCode": "",
                                    "CountryCode": "",
                                    "Longitude": 0,
                                    "Latitude": 0,
                                    "BuildingNumber": None,
                                    "BuildingName": None,
                                    "Floor": None,
                                    "Apartment": None,
                                    "POBox": None,
                                    "Description": None
                                },
                                "Contact": {
                                    "Department": "",
                                    "PersonName": "",
                                    "Title": "",
                                    "CompanyName": "",
                                    "PhoneNumber1": "",
                                    "PhoneNumber1Ext": "",
                                    "PhoneNumber2": "",
                                    "PhoneNumber2Ext": "",
                                    "FaxNumber": "",
                                    "CellPhone": "",
                                    "EmailAddress": "",
                                    "Type": ""
                                }
                            },
                            "ShippingDateTime": str('/Date(' + str(time) + ')/'),
                            "DueDate": str('/Date(' + str(time) + ')/'),
                            "Comments": "",
                            "PickupLocation": "",
                            "OperationsInstructions": "",
                            "AccountingInstrcutions": "",
                            "Details": {
                                "Dimensions": None,
                                "ActualWeight": {
                                        "Unit": "KG",
                                        "Value": float(old_orde.weight)
                                },
                                "ChargeableWeight": None,
                                "DescriptionOfGoods": None,
                                "GoodsOriginCountry": "IN",
                                "NumberOfPieces": 1,
                                "ProductGroup": product_group,
                                "ProductType": product_type,
                                "PaymentType": "P",
                                "PaymentOptions": "",
                                "CustomsValueAmount": None,
                                "CashOnDeliveryAmount": None,
                                "InsuranceAmount": None,
                                "CashAdditionalAmount": None,
                                "CashAdditionalAmountDescription": "",
                                "CollectAmount": None,
                                "Services": "",
                                "Items": []
                            },
                            "Attachments": [],
                            "ForeignHAWB": "",
                            "TransportType ": 0,
                            "PickupGUID": "",
                            "Number": None,
                            "ScheduledDelivery": None
                        }
                    ],
                    "Transaction": None

                }

                url = 'https://ws.aramex.net/ShippingAPI.V2/Shipping/Service_1_0.svc/json/CreateShipments'
                r = requests.post(url, json=data)
                soup = BeautifulSoup(r.content, 'html.parser')
                # print(soup)
                old_orde.tracking_no = soup.id.string
                old_orde.rpt_cache = soup.labelurl.string

            old_orde.is_finished = True
            old_orde.status = "Underway"
            old_orde.save()
            profile.blance = float(profile.blance) - float(old_orde.amount)
            profile.save()

            obj_order_suppliers = OrderSupplier.objects.all().filter(
                user=request.user,  order=old_orde)
            for obj_order_supplier in obj_order_suppliers:
                # order_details__supplier = OrderDetailsSupplier.objects.all().filter(
                #     order_supplier=obj_order_supplier, order=old_orde)
                # f_total = 0
                # w_total = 0
                # weight = 0
                # for sub in order_details__supplier:
                #     f_total += sub.price * sub.quantity
                #     w_total += sub.weight * sub.quantity
                #     total = f_total
                #     weight = w_total
                supplier = Profile.objects.get(id=obj_order_supplier.vendor.id)
                supplier.blance = float(
                    supplier.blance) + float(obj_order_supplier.amount)
                supplier.save()

            if "coupon_id" in request.session.keys():
                del request.session["coupon_id"]
            # messages.success(
            #     request, ' Great, you have completed your purchase, we will work to complete your order from our side')

            return redirect("/order/success")
        else:
            messages.warning(
                request, 'You do not have enough credit to purchase this product')
            return redirect("/payment")
    messages.warning(request, ' There is no order for you to buy it')
    return redirect("/home")


def payment_cash(request):

    cart_id = request.session.get('cart_id')
    order = Order.objects.all().filter(id=cart_id, is_finished=False)

    if order:
        old_orde = Order.objects.get(id=cart_id, is_finished=False)
        try:
            Consignee_id = old_orde.user.id
            Consignee_email = old_orde.user.email
        except:
            pass
        # profile = Profile.objects.get(user=request.user)

        payment_method = Payment.objects.get(order=old_orde)
        payment_method.payment_method = "Cash"
        payment_method.save()

        if settings.ARAMEX_USERNAME != "":
            if payment_method.country_code == settings.ARAMEX_ACCOUNTCOUNTRYCODE:
                product_group = "DOM"
                product_type = "OND"
            else:
                product_group = "EXP"
                product_type = "PPX"
            data = {
                "ClientInfo": {
                    "UserName": f"{settings.ARAMEX_USERNAME}",
                    "Password": f"{settings.ARAMEX_PASSWORD}",
                    "Version": f"{settings.ARAMEX_VERSION}",
                    "AccountNumber": f"{settings.ARAMEX_ACCOUNTNUMBER}",
                    "AccountPin": f"{settings.ARAMEX_ACCOUNTPIN}",
                    "AccountEntity": f"{settings.ARAMEX_ACCOUNTENTITY}",
                    "AccountCountryCode": f"{settings.ARAMEX_ACCOUNTCOUNTRYCODE}",
                    "Source": f"{settings.ARAMEX_SOURCE}"


                },

                "LabelInfo": {
                    "ReportID": 9201,
                    "ReportType": "URL"
                },
                "Shipments": [
                    {
                        "Reference1": f"{old_orde}",
                        "Reference2": "",
                        "Reference3": "",
                        "Shipper": {
                            "Reference1": f"{old_orde}",
                            "Reference2": "",
                            "AccountNumber": f"{settings.ARAMEX_ACCOUNTNUMBER}",
                            "PartyAddress": {
                                "Line1": "Oman",
                                "Line2": "",
                                "Line3": "",
                                "City": "Oman",
                                "StateOrProvinceCode": "",
                                "PostCode": "",
                                "CountryCode": f"{settings.ARAMEX_ACCOUNTCOUNTRYCODE}",
                                "Longitude": 0,
                                "Latitude": 0,
                                "BuildingNumber": None,
                                "BuildingName": None,
                                "Floor": None,
                                "Apartment": None,
                                "POBox": None,
                                "Description": "alithemes.com product"
                            },
                            "Contact": {
                                "Department": "",
                                "PersonName": "alithemes.com store",
                                "Title": "",
                                "CompanyName": "alithemes.com",
                                "PhoneNumber1": "1111111111",
                                "PhoneNumber1Ext": "",
                                "PhoneNumber2": "",
                                "PhoneNumber2Ext": "",
                                "FaxNumber": "",
                                "CellPhone": "1111111111111",
                                "EmailAddress": "mail@alithemes.com",
                                "Type": ""
                            }
                        },
                        "Consignee": {
                            "Reference1": f"{Consignee_id}",
                            "Reference2": f"{Consignee_email}",
                            "AccountNumber": f"{Consignee_id}",
                            "PartyAddress": {
                                "Line1": f"{payment_method.street_address}",
                                "Line2": "",
                                "Line3": "",
                                "City": f"{payment_method.City}",
                                "StateOrProvinceCode": f"{payment_method.state}",
                                "PostCode": f"{payment_method.post_code}",
                                "CountryCode": f"{payment_method.country_code}",
                                "Longitude": 0,
                                "Latitude": 0,
                                "BuildingNumber": "",
                                "BuildingName": "",
                                "Floor": "",
                                "Apartment": "",
                                "POBox": None,
                                "Description": "Please contact me when the shipment arrives"
                            },
                            "Contact": {
                                "Department": "",
                                "PersonName": f"{payment_method.first_name} {payment_method.last_name}",
                                "Title": f"{payment_method.last_name}",
                                "CompanyName": "",
                                "PhoneNumber1": f"{payment_method.phone}",
                                "PhoneNumber1Ext": "",
                                "PhoneNumber2": "",
                                "PhoneNumber2Ext": "",
                                "FaxNumber": "",
                                "CellPhone": f"{payment_method.phone}",
                                "EmailAddress": f"{payment_method.Email_Address}",
                                "Type": ""
                            }
                        },
                        "ThirdParty": {
                            "Reference1": "",
                            "Reference2": "",
                            "AccountNumber": "",
                            "PartyAddress": {
                                "Line1": "",
                                "Line2": "",
                                "Line3": "",
                                "City": "",
                                "StateOrProvinceCode": "",
                                "PostCode": "",
                                "CountryCode": "",
                                "Longitude": 0,
                                "Latitude": 0,
                                "BuildingNumber": None,
                                "BuildingName": None,
                                "Floor": None,
                                "Apartment": None,
                                "POBox": None,
                                "Description": None
                            },
                            "Contact": {
                                "Department": "",
                                "PersonName": "",
                                "Title": "",
                                "CompanyName": "",
                                "PhoneNumber1": "",
                                "PhoneNumber1Ext": "",
                                "PhoneNumber2": "",
                                "PhoneNumber2Ext": "",
                                "FaxNumber": "",
                                "CellPhone": "",
                                "EmailAddress": "",
                                "Type": ""
                            }
                        },
                        "ShippingDateTime": str('/Date(' + str(time) + ')/'),
                        "DueDate": str('/Date(' + str(time) + ')/'),
                        "Comments": "",
                        "PickupLocation": "",
                        "OperationsInstructions": "",
                        "AccountingInstrcutions": "",
                        "Details": {
                            "Dimensions": None,
                            "ActualWeight": {
                                    "Unit": "KG",
                                    "Value": float(old_orde.weight)
                            },
                            "ChargeableWeight": None,
                            "DescriptionOfGoods": None,
                            "GoodsOriginCountry": "IN",
                            "NumberOfPieces": 1,
                            "ProductGroup": product_group,
                            "ProductType": product_type,
                            "PaymentType": "P",
                            "PaymentOptions": "",
                            "CustomsValueAmount": None,
                            "CashOnDeliveryAmount": None,
                            "InsuranceAmount": None,
                            "CashAdditionalAmount": None,
                            "CashAdditionalAmountDescription": "",
                            "CollectAmount": None,
                            "Services": "",
                            "Items": []
                        },
                        "Attachments": [],
                        "ForeignHAWB": "",
                        "TransportType ": 0,
                        "PickupGUID": "",
                        "Number": None,
                        "ScheduledDelivery": None
                    }
                ],
                "Transaction": None

            }

            url = 'https://ws.aramex.net/ShippingAPI.V2/Shipping/Service_1_0.svc/json/CreateShipments'
            r = requests.post(url, json=data)
            soup = BeautifulSoup(r.content, 'html.parser')
            old_orde.tracking_no = soup.id.string
            old_orde.rpt_cache = soup.labelurl.string

        old_orde.is_finished = True
        old_orde.status = "Underway"
        old_orde.save()
        # code for set supplier's balance
        # order_details = OrderDetails.objects.all().filter(order=old_orde)
        # for order_detail in order_details:
        # item_supplier_details = OrderDetailsSupplier.objects.all().filter(
        #     order=old_orde)
        # for item_supplier in item_supplier_details:
        obj_order_suppliers = OrderSupplier.objects.all().filter(order=old_orde)
        for obj_order_supplier in obj_order_suppliers:
            # order_details__supplier = OrderDetailsSupplier.objects.all().filter(
            #     order_supplier=obj_order_supplier, order=old_orde)
            # f_total = 0
            # w_total = 0
            # weight = 0
            # for sub in order_details__supplier:
            #     f_total += sub.price * sub.quantity
            #     w_total += sub.weight * sub.quantity
            #     total = f_total
            #     weight = w_total
            supplier = Profile.objects.get(id=obj_order_supplier.vendor.id)
            supplier.blance = float(
                supplier.blance) + float(obj_order_supplier.amount)
            supplier.save()

        if "coupon_id" in request.session.keys():
            del request.session["coupon_id"]

        try:
            send_mail(
                'Great! Order ID{}. has been successfully purchased'.format(
                    old_orde.id),
                ' Congratulations, you have made your order, This order will be delivered to you soon.',
                f'{settings.EMAIL_SENDGRID}',
                [f'{payment_method.Email_Address}'],
                fail_silently=False,
            )
        except:
            pass
        return redirect("/order/success")

    # return redirect("orders:payment")
    messages.warning(request, ' There is no order for you to buy it ')
    # return redirect("products:homepage")
    return redirect('/home')


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(request):
    # product_id = self.kwargs["pk"]
    #     product = Product.objects.get(id=product_id)
    domain = f"https://{settings.YOUR_DOMAIN}/"
    cart_id = request.session.get('cart_id')

    order = Order.objects.get(id=cart_id, is_finished=False)
    try:
        stripe_logo = SiteSetting.objects.first().login_image.url
        # host = request.META.get("HTTP_HOST")
        stripe_image = "https://"+settings.YOUR_DOMAIN+stripe_logo
    except:
        stripe_image = ""

    print("stripe_image : ", stripe_image)
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(float(order.amount)*100),
                        'product_data': {
                            'name': f"Order Number :{order.id}",
                            'images': [stripe_image],
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "order_id": order.id,

            },
            mode='payment',
            success_url=domain + 'order/success/',
            cancel_url=domain + 'orders/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })
    except Exception as e:
        send_mail(
            'Order  has not been completed , ',
            ' {}'.format(e),
            f'{settings.EMAIL_SENDGRID}',
            [f'{settings.DEBUG_EMAIL}'],
            fail_silently=False,
        )
        return HttpResponse(str(e))


@require_POST
@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # print(" Invalid payload")
        send_mail(
            'Order  has not been completed , Invalid payload',
            ' {}'.format(e),
            f'{settings.EMAIL_SENDGRID}',
            [f'{settings.DEBUG_EMAIL}'],
            fail_silently=False,
        )
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError as e:
        # print("Invalid signature")
        send_mail(
            'Order  has not been completed , Invalid signature',
            ' {}'.format(e),
            f'{settings.EMAIL_SENDGRID}',
            [f'{settings.DEBUG_EMAIL}'],
            fail_silently=False,
        )
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        if session.payment_status == "paid":
            customer_email = session["customer_details"]["email"]
            order_id = session["metadata"]["order_id"]
            request.session['order_id'] = order_id

            order = Order.objects.all().filter(id=order_id, is_finished=False)

            if order:
                old_orde = Order.objects.get(id=order_id, is_finished=False)
                try:
                    Consignee_id = old_orde.user.id
                    Consignee_email = old_orde.user.email
                except:
                    pass
                payment_method = Payment.objects.get(order=old_orde)
                payment_method.payment_method = "Stripe"
                payment_method.save()

                if settings.ARAMEX_USERNAME != "":
                    if payment_method.country_code == settings.ARAMEX_ACCOUNTCOUNTRYCODE:
                        product_group = "DOM"
                        product_type = "OND"
                    else:
                        product_group = "EXP"
                        product_type = "PPX"
                    data = {
                        "ClientInfo": {
                            "UserName": f"{settings.ARAMEX_USERNAME}",
                            "Password": f"{settings.ARAMEX_PASSWORD}",
                            "Version": f"{settings.ARAMEX_VERSION}",
                            "AccountNumber": f"{settings.ARAMEX_ACCOUNTNUMBER}",
                            "AccountPin": f"{settings.ARAMEX_ACCOUNTPIN}",
                            "AccountEntity": f"{settings.ARAMEX_ACCOUNTENTITY}",
                            "AccountCountryCode": f"{settings.ARAMEX_ACCOUNTCOUNTRYCODE}",
                            "Source": f"{settings.ARAMEX_SOURCE}"


                        },

                        "LabelInfo": {
                            "ReportID": 9201,
                            "ReportType": "URL"
                        },
                        "Shipments": [
                            {
                                "Reference1": f"{old_orde}",
                                "Reference2": "",
                                "Reference3": "",
                                "Shipper": {
                                    "Reference1": f"{old_orde}",
                                    "Reference2": "",
                                    "AccountNumber": f"{settings.ARAMEX_ACCOUNTNUMBER}",
                                    "PartyAddress": {
                                        "Line1": "Oman",
                                        "Line2": "",
                                        "Line3": "",
                                        "City": "Oman",
                                        "StateOrProvinceCode": "",
                                        "PostCode": "",
                                        "CountryCode": f"{settings.ARAMEX_ACCOUNTCOUNTRYCODE}",
                                        "Longitude": 0,
                                        "Latitude": 0,
                                        "BuildingNumber": None,
                                        "BuildingName": None,
                                        "Floor": None,
                                        "Apartment": None,
                                        "POBox": None,
                                        "Description": "alithemes.com product"
                                    },
                                    "Contact": {
                                        "Department": "",
                                        "PersonName": "alithemes.com store",
                                        "Title": "",
                                        "CompanyName": "alithemes.com",
                                        "PhoneNumber1": "1111111111",
                                        "PhoneNumber1Ext": "",
                                        "PhoneNumber2": "",
                                        "PhoneNumber2Ext": "",
                                        "FaxNumber": "",
                                        "CellPhone": "1111111111111",
                                        "EmailAddress": "mail@alithemes.com",
                                        "Type": ""
                                    }
                                },
                                "Consignee": {
                                    "Reference1": f"{Consignee_id}",
                                    "Reference2": f"{Consignee_email}",
                                    "AccountNumber": f"{Consignee_id}",
                                    "PartyAddress": {
                                        "Line1": f"{payment_method.street_address}",
                                        "Line2": "",
                                        "Line3": "",
                                        "City": f"{payment_method.City}",
                                        "StateOrProvinceCode": f"{payment_method.state}",
                                        "PostCode": f"{payment_method.post_code}",
                                        "CountryCode": f"{payment_method.country_code}",
                                        "Longitude": 0,
                                        "Latitude": 0,
                                        "BuildingNumber": "",
                                        "BuildingName": "",
                                        "Floor": "",
                                        "Apartment": "",
                                        "POBox": None,
                                        "Description": "Please contact me when the shipment arrives"
                                    },
                                    "Contact": {
                                        "Department": "",
                                        "PersonName": f"{payment_method.first_name} {payment_method.last_name}",
                                        "Title": f"{payment_method.last_name}",
                                        "CompanyName": "",
                                        "PhoneNumber1": f"{payment_method.phone}",
                                        "PhoneNumber1Ext": "",
                                        "PhoneNumber2": "",
                                        "PhoneNumber2Ext": "",
                                        "FaxNumber": "",
                                        "CellPhone": f"{payment_method.phone}",
                                        "EmailAddress": f"{payment_method.Email_Address}",
                                        "Type": ""
                                    }
                                },
                                "ThirdParty": {
                                    "Reference1": "",
                                    "Reference2": "",
                                    "AccountNumber": "",
                                    "PartyAddress": {
                                        "Line1": "",
                                        "Line2": "",
                                        "Line3": "",
                                        "City": "",
                                        "StateOrProvinceCode": "",
                                        "PostCode": "",
                                        "CountryCode": "",
                                        "Longitude": 0,
                                        "Latitude": 0,
                                        "BuildingNumber": None,
                                        "BuildingName": None,
                                        "Floor": None,
                                        "Apartment": None,
                                        "POBox": None,
                                        "Description": None
                                    },
                                    "Contact": {
                                        "Department": "",
                                        "PersonName": "",
                                        "Title": "",
                                        "CompanyName": "",
                                        "PhoneNumber1": "",
                                        "PhoneNumber1Ext": "",
                                        "PhoneNumber2": "",
                                        "PhoneNumber2Ext": "",
                                        "FaxNumber": "",
                                        "CellPhone": "",
                                        "EmailAddress": "",
                                        "Type": ""
                                    }
                                },
                                "ShippingDateTime": str('/Date(' + str(time) + ')/'),
                                "DueDate": str('/Date(' + str(time) + ')/'),
                                "Comments": "",
                                "PickupLocation": "",
                                "OperationsInstructions": "",
                                "AccountingInstrcutions": "",
                                "Details": {
                                    "Dimensions": None,
                                    "ActualWeight": {
                                        "Unit": "KG",
                                        "Value": float(old_orde.weight)
                                    },
                                    "ChargeableWeight": None,
                                    "DescriptionOfGoods": None,
                                    "GoodsOriginCountry": "IN",
                                    "NumberOfPieces": 1,
                                    "ProductGroup": product_group,
                                    "ProductType": product_type,
                                    "PaymentType": "P",
                                    "PaymentOptions": "",
                                    "CustomsValueAmount": None,
                                    "CashOnDeliveryAmount": None,
                                    "InsuranceAmount": None,
                                    "CashAdditionalAmount": None,
                                    "CashAdditionalAmountDescription": "",
                                    "CollectAmount": None,
                                    "Services": "",
                                    "Items": []
                                },
                                "Attachments": [],
                                "ForeignHAWB": "",
                                "TransportType ": 0,
                                "PickupGUID": "",
                                "Number": None,
                                "ScheduledDelivery": None
                            }
                        ],
                        "Transaction": None

                    }

                    url = 'https://ws.aramex.net/ShippingAPI.V2/Shipping/Service_1_0.svc/json/CreateShipments'
                    r = requests.post(url, json=data)
                    # print(type(r.content) )
                    soup = BeautifulSoup(r.content, 'html.parser')
                    # print(soup)
                    old_orde.tracking_no = soup.id.string
                    old_orde.rpt_cache = soup.labelurl.string

                # delete available
                products_details = OrderDetails.objects.all().filter(order=old_orde)
                for pro in products_details:
                    product_order = Product.objects.get(
                        id=pro.product.id)
                    if product_order.available > 0:
                        product_order.available = product_order.available - pro.quantity
                        product_order.save()

                old_orde.is_finished = True
                old_orde.status = "Underway"
                old_orde.save()

                # code for set supplier's balance
                obj_order_suppliers = OrderSupplier.objects.all().filter(order=old_orde)
                for obj_order_supplier in obj_order_suppliers:
                    supplier = Profile.objects.get(
                        id=obj_order_supplier.vendor.id)
                    supplier.blance = float(
                        supplier.blance) + float(obj_order_supplier.amount)
                    supplier.save()
                try:

                    send_mail(
                        'Great! Order ID{}. has been successfully purchased'.format(
                            order_id),
                        ' Congratulations, you have made your order, This order will be delivered to you soon.',
                        f'{settings.EMAIL_SENDGRID}',
                        [f'{customer_email}'],
                        fail_silently=False,
                    )
                except:
                    pass
                if "coupon_id" in request.session.keys():
                    del request.session["coupon_id"]

    elif event['type'] == 'checkout.session.async_payment_succeeded':
        session = event['data']['object']
        customer_email = session["customer_details"]["email"]
        order_id = session["metadata"]["order_id"]
        order = Order.objects.all().filter(id=order_id, is_finished=False)
        request.session['order_id'] = order_id
        if order:
            old_orde = Order.objects.get(id=order_id, is_finished=False)
            try:
                Consignee_id = old_orde.user.id
                Consignee_email = old_orde.user.email
            except:
                pass
            payment_method = Payment.objects.get(order=old_orde)
            payment_method.payment_method = "Stripe"
            payment_method.save()

            if settings.ARAMEX_USERNAME != "":
                if payment_method.country_code == settings.ARAMEX_ACCOUNTCOUNTRYCODE:
                    product_group = "DOM"
                    product_type = "OND"
                else:
                    product_group = "EXP"
                    product_type = "PPX"
                data = {
                    "ClientInfo": {
                        "UserName": f"{settings.ARAMEX_USERNAME}",
                        "Password": f"{settings.ARAMEX_PASSWORD}",
                        "Version": f"{settings.ARAMEX_VERSION}",
                        "AccountNumber": f"{settings.ARAMEX_ACCOUNTNUMBER}",
                        "AccountPin": f"{settings.ARAMEX_ACCOUNTPIN}",
                        "AccountEntity": f"{settings.ARAMEX_ACCOUNTENTITY}",
                        "AccountCountryCode": f"{settings.ARAMEX_ACCOUNTCOUNTRYCODE}",
                        "Source": f"{settings.ARAMEX_SOURCE}"


                    },

                    "LabelInfo": {
                        "ReportID": 9201,
                        "ReportType": "URL"
                    },
                    "Shipments": [
                        {
                            "Reference1": f"{old_orde}",
                            "Reference2": "",
                            "Reference3": "",
                            "Shipper": {
                                "Reference1": f"{old_orde}",
                                "Reference2": "",
                                "AccountNumber": f"{settings.ARAMEX_ACCOUNTNUMBER}",
                                "PartyAddress": {
                                    "Line1": "Oman",
                                    "Line2": "",
                                    "Line3": "",
                                    "City": "Oman",
                                    "StateOrProvinceCode": "",
                                    "PostCode": "",
                                    "CountryCode": f"{settings.ARAMEX_ACCOUNTCOUNTRYCODE}",
                                    "Longitude": 0,
                                    "Latitude": 0,
                                    "BuildingNumber": None,
                                    "BuildingName": None,
                                    "Floor": None,
                                    "Apartment": None,
                                    "POBox": None,
                                    "Description": "alithemes.com product"
                                },
                                "Contact": {
                                    "Department": "",
                                    "PersonName": "alithemes.com store",
                                    "Title": "",
                                    "CompanyName": "alithemes.com",
                                    "PhoneNumber1": "1111111111",
                                    "PhoneNumber1Ext": "",
                                    "PhoneNumber2": "",
                                    "PhoneNumber2Ext": "",
                                    "FaxNumber": "",
                                    "CellPhone": "1111111111111",
                                    "EmailAddress": "mail@alithemes.com",
                                    "Type": ""
                                }
                            },
                            "Consignee": {
                                "Reference1": f"{Consignee_id}",
                                "Reference2": f"{Consignee_email}",
                                "AccountNumber": f"{Consignee_id}",
                                "PartyAddress": {
                                    "Line1": f"{payment_method.street_address}",
                                    "Line2": "",
                                    "Line3": "",
                                    "City": f"{payment_method.City}",
                                    "StateOrProvinceCode": f"{payment_method.state}",
                                    "PostCode": f"{payment_method.post_code}",
                                    "CountryCode": f"{payment_method.country_code}",
                                    "Longitude": 0,
                                    "Latitude": 0,
                                    "BuildingNumber": "",
                                    "BuildingName": "",
                                    "Floor": "",
                                    "Apartment": "",
                                    "POBox": None,
                                    "Description": "Please contact me when the shipment arrives"
                                },
                                "Contact": {
                                    "Department": "",
                                    "PersonName": f"{payment_method.first_name} {payment_method.last_name}",
                                    "Title": f"{payment_method.last_name}",
                                    "CompanyName": "",
                                    "PhoneNumber1": f"{payment_method.phone}",
                                    "PhoneNumber1Ext": "",
                                    "PhoneNumber2": "",
                                    "PhoneNumber2Ext": "",
                                    "FaxNumber": "",
                                    "CellPhone": f"{payment_method.phone}",
                                    "EmailAddress": f"{payment_method.Email_Address}",
                                    "Type": ""
                                }
                            },
                            "ThirdParty": {
                                "Reference1": "",
                                "Reference2": "",
                                "AccountNumber": "",
                                "PartyAddress": {
                                    "Line1": "",
                                    "Line2": "",
                                    "Line3": "",
                                    "City": "",
                                    "StateOrProvinceCode": "",
                                    "PostCode": "",
                                    "CountryCode": "",
                                    "Longitude": 0,
                                    "Latitude": 0,
                                    "BuildingNumber": None,
                                    "BuildingName": None,
                                    "Floor": None,
                                    "Apartment": None,
                                    "POBox": None,
                                    "Description": None
                                },
                                "Contact": {
                                    "Department": "",
                                    "PersonName": "",
                                    "Title": "",
                                    "CompanyName": "",
                                    "PhoneNumber1": "",
                                    "PhoneNumber1Ext": "",
                                    "PhoneNumber2": "",
                                    "PhoneNumber2Ext": "",
                                    "FaxNumber": "",
                                    "CellPhone": "",
                                    "EmailAddress": "",
                                    "Type": ""
                                }
                            },
                            "ShippingDateTime": str('/Date(' + str(time) + ')/'),
                            "DueDate": str('/Date(' + str(time) + ')/'),
                            "Comments": "",
                            "PickupLocation": "",
                            "OperationsInstructions": "",
                            "AccountingInstrcutions": "",
                            "Details": {
                                "Dimensions": None,
                                "ActualWeight": {
                                        "Unit": "KG",
                                        "Value": float(old_orde.weight)
                                },
                                "ChargeableWeight": None,
                                "DescriptionOfGoods": None,
                                "GoodsOriginCountry": "IN",
                                "NumberOfPieces": 1,
                                "ProductGroup": product_group,
                                "ProductType": product_type,
                                "PaymentType": "P",
                                "PaymentOptions": "",
                                "CustomsValueAmount": None,
                                "CashOnDeliveryAmount": None,
                                "InsuranceAmount": None,
                                "CashAdditionalAmount": None,
                                "CashAdditionalAmountDescription": "",
                                "CollectAmount": None,
                                "Services": "",
                                "Items": []
                            },
                            "Attachments": [],
                            "ForeignHAWB": "",
                            "TransportType ": 0,
                            "PickupGUID": "",
                            "Number": None,
                            "ScheduledDelivery": None
                        }
                    ],
                    "Transaction": None

                }

                url = 'https://ws.aramex.net/ShippingAPI.V2/Shipping/Service_1_0.svc/json/CreateShipments'
                r = requests.post(url, json=data)
                # print(type(r.content) )
                soup = BeautifulSoup(r.content, 'html.parser')
                # print(soup)
                old_orde.tracking_no = soup.id.string
                old_orde.rpt_cache = soup.labelurl.string

            # delete available
            products_details = OrderDetails.objects.all().filter(order=old_orde)
            for pro in products_details:
                product_order = Product.objects.get(
                    id=pro.product.id)
                if product_order.available > 0:
                    product_order.available = product_order.available - pro.quantity
                    product_order.save()

            old_orde.is_finished = True
            old_orde.status = "Underway"
            old_orde.save()

            # code for set supplier's balance
            obj_order_suppliers = OrderSupplier.objects.all().filter(order=old_orde)
            for obj_order_supplier in obj_order_suppliers:
                supplier = Profile.objects.get(
                    id=obj_order_supplier.vendor.id)
                supplier.blance = float(
                    supplier.blance) + float(obj_order_supplier.amount)
                supplier.save()
            try:
                send_mail(
                    'Order ID {}. has been successfully purchased'.format(
                        order_id),
                    ' Congratulations, you have made your order, This order will be delivered to you soon.',
                    f'{settings.EMAIL_SENDGRID}',
                    [f'{customer_email}'],
                    fail_silently=False,
                )
            except:
                pass
            if "coupon_id" in request.session.keys():
                del request.session["coupon_id"]

    elif event['type'] == 'checkout.session.async_payment_failed':
        session = event['data']['object']
        customer_email = session["customer_details"]["email"]
        order_id = session["metadata"]["order_id"]
        request.session['order_id'] = order_id
        try:
            send_mail(
                'Order NO. {}. has not been completed , payment_failed'.format(
                    order_id),
                f'{settings.EMAIL_SENDGRID}',
                [f'{customer_email}'],
                fail_silently=False,
            )
        except:
            pass
    # Send an email to the customer asking them to retry their order

    return HttpResponse(status=200)


def checkout_payment_paymob(request, id):
    context = None
    # if request.method == "POST":
    order_id = id
    if Order.objects.all().filter(id=order_id, is_finished=False).exists():
        old_orde = Order.objects.get(id=order_id, is_finished=False)
        payment_method = Payment.objects.get(order=old_orde)
        order_details = OrderDetails.objects.filter(
            order=old_orde).last()
        # endpoint for get account token "Authentication Request"
        url_authentication = "https://accept.paymob.com/api/auth/tokens"
        data_authentication = {
            "api_key": settings.API_KEY
        }
        request_api_token = requests.post(
            url_authentication, json=data_authentication).json()
        account_token = request_api_token["token"]

        merchant_order_id = f'{order_id}-{code_generator()}'

        total = int(float(old_orde.amount) * 18.9 * 100)

        url_order_registration = "https://accept.paymob.com/api/ecommerce/orders"
        data_order_registration = {
            "auth_token": account_token,
            "delivery_needed": "false",
            "amount_cents": f"{total}",
            "currency": "EGP",
            "merchant_order_id": merchant_order_id,
            "items": [
                {
                    "name": f"{order_details.product.product_name}",
                    "amount_cents": f"{total}",
                    "description": f"{order_details.product.product_name}",
                    "quantity": "1"
                }
            ],
            "shipping_data": {},
            "shipping_details": {}
        }
        request_order_registration = requests.post(
            url_order_registration, json=data_order_registration).json()

        order_registration_id = request_order_registration["id"]
        # Payment Key Request
        url_payment_key = "https://accept.paymob.com/api/acceptance/payment_keys"
        data_payment_key = {
            "auth_token": account_token,
            "amount_cents": f"{total}",
            "expiration": 3600,
            "order_id": f"{order_registration_id}",
            "billing_data": {
                "apartment": "None",
                "email": payment_method.Email_Address,
                "floor": "None",
                "first_name": payment_method.first_name,
                "street": payment_method.street_address,
                "building": "None",
                "phone_number": payment_method.phone,
                "shipping_method": "PKG",
                "postal_code": "None",
                "city": "None",
                "country": "eg",
                "last_name": payment_method.last_name,
                "state": payment_method.state
            },
            "currency": "EGP",
            "integration_id": settings.PAYMENT_INTEGRATIONS_ID,
            "lock_order_when_paid": "false"
        }
        request_payment_key = requests.post(
            url_payment_key, json=data_payment_key).json()

        payment_key_token = request_payment_key["token"]
        # merchant_order_id and order_registration_id will used to get booking order
        old_orde.auth_token_order = account_token
        old_orde.merchant_order_id = merchant_order_id
        old_orde.order_id_paymob = order_registration_id
        old_orde.save()

        # car_booking.

        return HttpResponseRedirect(f"https://accept.paymob.com/api/acceptance/iframes/430703?payment_token={payment_key_token}")
    else:
        messages.warning(request, 'Please enter your information correctly.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def my_webhook_view_paymob(request, *args, **kwargs):
    if request.method == 'GET':
        order_id_paymob = request.GET['order']
        merchant_order_id = request.GET['merchant_order_id']
        trnx_id = int(request.GET['id'])
        if Order.objects.all().filter(order_id_paymob=order_id_paymob, merchant_order_id=merchant_order_id).exists():
            old_orde = Order.objects.get(
                order_id_paymob=order_id_paymob, merchant_order_id=merchant_order_id)
            auth_token_order = old_orde.auth_token_order
            # Retrieve A Transaction
            url_retrieve_transaction = f"https://accept.paymob.com/api/acceptance/transactions/{trnx_id}"
            data_retrieve_transaction = {
                "auth_token": f"{old_orde.auth_token_order}"
            }
            request_order_registration = requests.get(
                url_retrieve_transaction, json=data_retrieve_transaction).json()

            transaction_id = int(request_order_registration["id"])
            if transaction_id == trnx_id:
                old_orde.trnx_id = trnx_id
                if request_order_registration["success"] == True:
                    # checkout success

                    try:
                        Consignee_id = old_orde.user.id
                        Consignee_email = old_orde.user.email
                    except:
                        pass
                    payment_method = Payment.objects.get(order=old_orde)
                    payment_method.payment_method = "PayMob"
                    payment_method.save()

                    if settings.ARAMEX_USERNAME != "":
                        if payment_method.country_code == settings.ARAMEX_ACCOUNTCOUNTRYCODE:
                            product_group = "DOM"
                            product_type = "OND"
                        else:
                            product_group = "EXP"
                            product_type = "PPX"
                        data = {
                            "ClientInfo": {
                                "UserName": f"{settings.ARAMEX_USERNAME}",
                                "Password": f"{settings.ARAMEX_PASSWORD}",
                                "Version": f"{settings.ARAMEX_VERSION}",
                                "AccountNumber": f"{settings.ARAMEX_ACCOUNTNUMBER}",
                                "AccountPin": f"{settings.ARAMEX_ACCOUNTPIN}",
                                "AccountEntity": f"{settings.ARAMEX_ACCOUNTENTITY}",
                                "AccountCountryCode": f"{settings.ARAMEX_ACCOUNTCOUNTRYCODE}",
                                "Source": f"{settings.ARAMEX_SOURCE}"

                            },

                            "LabelInfo": {
                                "ReportID": 9201,
                                "ReportType": "URL"
                            },
                            "Shipments": [
                                {
                                    "Reference1": f"{old_orde}",
                                    "Reference2": "",
                                    "Reference3": "",
                                    "Shipper": {
                                        "Reference1": f"{old_orde}",
                                        "Reference2": "",
                                        "AccountNumber": f"{settings.ARAMEX_ACCOUNTNUMBER}",
                                        "PartyAddress": {
                                            "Line1": "Oman",
                                            "Line2": "",
                                            "Line3": "",
                                            "City": "Oman",
                                            "StateOrProvinceCode": "",
                                            "PostCode": "",
                                            "CountryCode": f"{settings.ARAMEX_ACCOUNTCOUNTRYCODE}",
                                            "Longitude": 0,
                                            "Latitude": 0,
                                            "BuildingNumber": None,
                                            "BuildingName": None,
                                            "Floor": None,
                                            "Apartment": None,
                                            "POBox": None,
                                            "Description": "alithemes.com product"
                                        },
                                        "Contact": {
                                            "Department": "",
                                            "PersonName": "alithemes.com store",
                                            "Title": "",
                                            "CompanyName": "alithemes.com",
                                            "PhoneNumber1": "1111111111",
                                            "PhoneNumber1Ext": "",
                                            "PhoneNumber2": "",
                                            "PhoneNumber2Ext": "",
                                            "FaxNumber": "",
                                            "CellPhone": "1111111111111",
                                            "EmailAddress": "mail@alithemes.com",
                                            "Type": ""
                                        }
                                    },
                                    "Consignee": {
                                        "Reference1": f"{Consignee_id}",
                                        "Reference2": f"{Consignee_email}",
                                        "AccountNumber": f"{Consignee_id}",
                                        "PartyAddress": {
                                            "Line1": f"{payment_method.street_address}",
                                            "Line2": "",
                                            "Line3": "",
                                            "City": f"{payment_method.City}",
                                            "StateOrProvinceCode": f"{payment_method.state}",
                                            "PostCode": f"{payment_method.post_code}",
                                            "CountryCode": f"{payment_method.country_code}",
                                            "Longitude": 0,
                                            "Latitude": 0,
                                            "BuildingNumber": "",
                                            "BuildingName": "",
                                            "Floor": "",
                                            "Apartment": "",
                                            "POBox": None,
                                            "Description": "Please contact me when the shipment arrives"
                                        },
                                        "Contact": {
                                            "Department": "",
                                            "PersonName": f"{payment_method.first_name} {payment_method.last_name}",
                                            "Title": f"{payment_method.last_name}",
                                            "CompanyName": "",
                                            "PhoneNumber1": f"{payment_method.phone}",
                                            "PhoneNumber1Ext": "",
                                            "PhoneNumber2": "",
                                            "PhoneNumber2Ext": "",
                                            "FaxNumber": "",
                                            "CellPhone": f"{payment_method.phone}",
                                            "EmailAddress": f"{payment_method.Email_Address}",
                                            "Type": ""
                                        }
                                    },
                                    "ThirdParty": {
                                        "Reference1": "",
                                        "Reference2": "",
                                        "AccountNumber": "",
                                        "PartyAddress": {
                                            "Line1": "",
                                            "Line2": "",
                                            "Line3": "",
                                            "City": "",
                                            "StateOrProvinceCode": "",
                                            "PostCode": "",
                                            "CountryCode": "",
                                            "Longitude": 0,
                                            "Latitude": 0,
                                            "BuildingNumber": None,
                                            "BuildingName": None,
                                            "Floor": None,
                                            "Apartment": None,
                                            "POBox": None,
                                            "Description": None
                                        },
                                        "Contact": {
                                            "Department": "",
                                            "PersonName": "",
                                            "Title": "",
                                            "CompanyName": "",
                                            "PhoneNumber1": "",
                                            "PhoneNumber1Ext": "",
                                            "PhoneNumber2": "",
                                            "PhoneNumber2Ext": "",
                                            "FaxNumber": "",
                                            "CellPhone": "",
                                            "EmailAddress": "",
                                            "Type": ""
                                        }
                                    },
                                    "ShippingDateTime": str('/Date(' + str(time) + ')/'),
                                    "DueDate": str('/Date(' + str(time) + ')/'),
                                    "Comments": "",
                                    "PickupLocation": "",
                                    "OperationsInstructions": "",
                                    "AccountingInstrcutions": "",
                                    "Details": {
                                        "Dimensions": None,
                                        "ActualWeight": {
                                            "Unit": "KG",
                                            "Value": float(old_orde.weight)
                                        },
                                        "ChargeableWeight": None,
                                        "DescriptionOfGoods": None,
                                        "GoodsOriginCountry": "IN",
                                        "NumberOfPieces": 1,
                                        "ProductGroup": product_group,
                                        "ProductType": product_type,
                                        "PaymentType": "P",
                                        "PaymentOptions": "",
                                        "CustomsValueAmount": None,
                                        "CashOnDeliveryAmount": None,
                                        "InsuranceAmount": None,
                                        "CashAdditionalAmount": None,
                                        "CashAdditionalAmountDescription": "",
                                        "CollectAmount": None,
                                        "Services": "",
                                        "Items": []
                                    },
                                    "Attachments": [],
                                    "ForeignHAWB": "",
                                    "TransportType ": 0,
                                    "PickupGUID": "",
                                    "Number": None,
                                    "ScheduledDelivery": None
                                }
                            ],
                            "Transaction": None

                        }

                        url = 'https://ws.aramex.net/ShippingAPI.V2/Shipping/Service_1_0.svc/json/CreateShipments'
                        r = requests.post(url, json=data)
                        # print(type(r.content) )
                        soup = BeautifulSoup(r.content, 'html.parser')
                        # print(soup)
                        old_orde.tracking_no = soup.id.string
                        old_orde.rpt_cache = soup.labelurl.string

                    # delete available
                    products_details = OrderDetails.objects.all().filter(order=old_orde)
                    for pro in products_details:
                        product_order = Product.objects.get(
                            id=pro.product.id)
                        if product_order.available > 0:
                            product_order.available = product_order.available - pro.quantity
                            product_order.save()

                    old_orde.is_finished = True
                    old_orde.status = "Underway"
                    old_orde.save()

                    # code for set supplier's balance
                    obj_order_suppliers = OrderSupplier.objects.all().filter(order=old_orde)
                    for obj_order_supplier in obj_order_suppliers:
                        supplier = Profile.objects.get(
                            id=obj_order_supplier.vendor.id)
                        supplier.blance = float(
                            supplier.blance) + float(obj_order_supplier.amount)
                        supplier.save()
                    try:

                        send_mail(
                            'Great! Order ID{}. has been successfully purchased'.format(
                                old_orde.id),
                            ' Congratulations, you have made your order, This order will be delivered to you soon.',
                            f'{settings.EMAIL_SENDGRID}',
                            [f'{payment_method.Email_Address}'],
                            fail_silently=False,
                        )
                    except:
                        pass
                    if "coupon_id" in request.session.keys():
                        del request.session["coupon_id"]

                    return redirect('orders:success')

                else:
                    messages.warning(
                        request, f"A technical problem has occurred, please contact technical support")
                    return redirect('orders:cancel')
        else:
            messages.warning(
                request, f"A technical problem has occurred, please contact technical support")
            return redirect('home:index')


def verify_payment_razorpay(request):
    if request.is_ajax():
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        order_id = request.POST.get('order_id')
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        signature = client.utility.verify_payment_signature(params_dict)
        if signature == True:
            # checkout success
            order = Order.objects.all().filter(id=order_id, is_finished=False)

            if order:
                old_orde = Order.objects.get(id=order_id, is_finished=False)
                try:
                    Consignee_id = old_orde.user.id
                    Consignee_email = old_orde.user.email
                except:
                    pass
                payment_method = Payment.objects.get(order=old_orde)
                payment_method.payment_method = "RazorPay"
                payment_method.save()

                if settings.ARAMEX_USERNAME != "":
                    if payment_method.country_code == settings.ARAMEX_ACCOUNTCOUNTRYCODE:
                        product_group = "DOM"
                        product_type = "OND"
                    else:
                        product_group = "EXP"
                        product_type = "PPX"
                    data = {
                        "ClientInfo": {
                            "UserName": f"{settings.ARAMEX_USERNAME}",
                            "Password": f"{settings.ARAMEX_PASSWORD}",
                            "Version": f"{settings.ARAMEX_VERSION}",
                            "AccountNumber": f"{settings.ARAMEX_ACCOUNTNUMBER}",
                            "AccountPin": f"{settings.ARAMEX_ACCOUNTPIN}",
                            "AccountEntity": f"{settings.ARAMEX_ACCOUNTENTITY}",
                            "AccountCountryCode": f"{settings.ARAMEX_ACCOUNTCOUNTRYCODE}",
                            "Source": f"{settings.ARAMEX_SOURCE}"


                        },

                        "LabelInfo": {
                            "ReportID": 9201,
                            "ReportType": "URL"
                        },
                        "Shipments": [
                            {
                                "Reference1": f"{old_orde}",
                                "Reference2": "",
                                "Reference3": "",
                                "Shipper": {
                                    "Reference1": f"{old_orde}",
                                    "Reference2": "",
                                    "AccountNumber": f"{settings.ARAMEX_ACCOUNTNUMBER}",
                                    "PartyAddress": {
                                        "Line1": "Oman",
                                        "Line2": "",
                                        "Line3": "",
                                        "City": "Oman",
                                        "StateOrProvinceCode": "",
                                        "PostCode": "",
                                        "CountryCode": f"{settings.ARAMEX_ACCOUNTCOUNTRYCODE}",
                                        "Longitude": 0,
                                        "Latitude": 0,
                                        "BuildingNumber": None,
                                        "BuildingName": None,
                                        "Floor": None,
                                        "Apartment": None,
                                        "POBox": None,
                                        "Description": "alithemes.com product"
                                    },
                                    "Contact": {
                                        "Department": "",
                                        "PersonName": "alithemes.com store",
                                        "Title": "",
                                        "CompanyName": "alithemes.com",
                                        "PhoneNumber1": "1111111111",
                                        "PhoneNumber1Ext": "",
                                        "PhoneNumber2": "",
                                        "PhoneNumber2Ext": "",
                                        "FaxNumber": "",
                                        "CellPhone": "1111111111111",
                                        "EmailAddress": "mail@alithemes.com",
                                        "Type": ""
                                    }
                                },
                                "Consignee": {
                                    "Reference1": f"{Consignee_id}",
                                    "Reference2": f"{Consignee_email}",
                                    "AccountNumber": f"{Consignee_id}",
                                    "PartyAddress": {
                                        "Line1": f"{payment_method.street_address}",
                                        "Line2": "",
                                        "Line3": "",
                                        "City": f"{payment_method.City}",
                                        "StateOrProvinceCode": f"{payment_method.state}",
                                        "PostCode": f"{payment_method.post_code}",
                                        "CountryCode": f"{payment_method.country_code}",
                                        "Longitude": 0,
                                        "Latitude": 0,
                                        "BuildingNumber": "",
                                        "BuildingName": "",
                                        "Floor": "",
                                        "Apartment": "",
                                        "POBox": None,
                                        "Description": "Please contact me when the shipment arrives"
                                    },
                                    "Contact": {
                                        "Department": "",
                                        "PersonName": f"{payment_method.first_name} {payment_method.last_name}",
                                        "Title": f"{payment_method.last_name}",
                                        "CompanyName": "",
                                        "PhoneNumber1": f"{payment_method.phone}",
                                        "PhoneNumber1Ext": "",
                                        "PhoneNumber2": "",
                                        "PhoneNumber2Ext": "",
                                        "FaxNumber": "",
                                        "CellPhone": f"{payment_method.phone}",
                                        "EmailAddress": f"{payment_method.Email_Address}",
                                        "Type": ""
                                    }
                                },
                                "ThirdParty": {
                                    "Reference1": "",
                                    "Reference2": "",
                                    "AccountNumber": "",
                                    "PartyAddress": {
                                        "Line1": "",
                                        "Line2": "",
                                        "Line3": "",
                                        "City": "",
                                        "StateOrProvinceCode": "",
                                        "PostCode": "",
                                        "CountryCode": "",
                                        "Longitude": 0,
                                        "Latitude": 0,
                                        "BuildingNumber": None,
                                        "BuildingName": None,
                                        "Floor": None,
                                        "Apartment": None,
                                        "POBox": None,
                                        "Description": None
                                    },
                                    "Contact": {
                                        "Department": "",
                                        "PersonName": "",
                                        "Title": "",
                                        "CompanyName": "",
                                        "PhoneNumber1": "",
                                        "PhoneNumber1Ext": "",
                                        "PhoneNumber2": "",
                                        "PhoneNumber2Ext": "",
                                        "FaxNumber": "",
                                        "CellPhone": "",
                                        "EmailAddress": "",
                                        "Type": ""
                                    }
                                },
                                "ShippingDateTime": str('/Date(' + str(time) + ')/'),
                                "DueDate": str('/Date(' + str(time) + ')/'),
                                "Comments": "",
                                "PickupLocation": "",
                                "OperationsInstructions": "",
                                "AccountingInstrcutions": "",
                                "Details": {
                                    "Dimensions": None,
                                    "ActualWeight": {
                                        "Unit": "KG",
                                        "Value": float(old_orde.weight)
                                    },
                                    "ChargeableWeight": None,
                                    "DescriptionOfGoods": None,
                                    "GoodsOriginCountry": "IN",
                                    "NumberOfPieces": 1,
                                    "ProductGroup": product_group,
                                    "ProductType": product_type,
                                    "PaymentType": "P",
                                    "PaymentOptions": "",
                                    "CustomsValueAmount": None,
                                    "CashOnDeliveryAmount": None,
                                    "InsuranceAmount": None,
                                    "CashAdditionalAmount": None,
                                    "CashAdditionalAmountDescription": "",
                                    "CollectAmount": None,
                                    "Services": "",
                                    "Items": []
                                },
                                "Attachments": [],
                                "ForeignHAWB": "",
                                "TransportType ": 0,
                                "PickupGUID": "",
                                "Number": None,
                                "ScheduledDelivery": None
                            }
                        ],
                        "Transaction": None

                    }

                    url = 'https://ws.aramex.net/ShippingAPI.V2/Shipping/Service_1_0.svc/json/CreateShipments'
                    r = requests.post(url, json=data)
                    # print(type(r.content) )
                    soup = BeautifulSoup(r.content, 'html.parser')
                    # print(soup)
                    old_orde.tracking_no = soup.id.string
                    old_orde.rpt_cache = soup.labelurl.string

                # delete available
                products_details = OrderDetails.objects.all().filter(order=old_orde)
                for pro in products_details:
                    product_order = Product.objects.get(
                        id=pro.product.id)
                    if product_order.available > 0:
                        product_order.available = product_order.available - pro.quantity
                        product_order.save()

                old_orde.is_finished = True
                old_orde.status = "Underway"
                old_orde.save()

                # code for set supplier's balance
                obj_order_suppliers = OrderSupplier.objects.all().filter(order=old_orde)
                for obj_order_supplier in obj_order_suppliers:
                    supplier = Profile.objects.get(
                        id=obj_order_supplier.vendor.id)
                    supplier.blance = float(
                        supplier.blance) + float(obj_order_supplier.amount)
                    supplier.save()
                try:

                    send_mail(
                        'Great! Order ID{}. has been successfully purchased'.format(
                            order_id),
                        ' Congratulations, you have made your order, This order will be delivered to you soon.',
                        f'{settings.EMAIL_SENDGRID}',
                        [f'{payment_method.Email_Address}'],
                        fail_silently=False,
                    )
                except:
                    pass
                if "coupon_id" in request.session.keys():
                    del request.session["coupon_id"]
        # return HttpResponse(json.dumps(signature))
        return JsonResponse({"success": True, "data": signature}, safe=False)

    else:
        return JsonResponse({"success": False, "data": "None"}, safe=False)


# def success(request):
#     if not request.session.has_key('currency'):
#         request.session['currency'] = settings.DEFAULT_CURRENCY

#     try:
#         try:
#             order_id = request.session['cart_id']

#         except:
#             order_id = request.session.get("order_id")
#     except:
#         pass

#     order = Order.objects.all().filter(id=order_id, is_finished=True)

#     if order:
#         order_success = Order.objects.get(
#             id=order_id, is_finished=True)
#         order_details_success = OrderDetails.objects.filter(
#             order=order_success)
#         payment_info = Payment.objects.get(order=order_success)

#         context = {
#             "order_success": order_success,
#             "order_details_success": order_details_success,
#             "payment_info": payment_info,
#         }
#         # send_mail(
#         #     'Order No {}. has been successfully purchased'.format(
#         #         order_id),
#         #     ' we will work to complete your order from our side.',
#         #     f'{settings.EMAIL_SENDGRID}',
#         #     [f'{payment_info.Email_Address}', ],
#         #     fail_silently=False,
#         # )
#         messages.success(
#             request, ' Congratulations, you have made your order, This order will be delivered to you soon')
#         return render(request, "ecommerce/success.html", context)
#     else:

#         messages.success(
#             request, 'Congratulations, you have made your order, This order will be delivered to you soon')
#         return render(request, "ecommerce/success-x.html")

def success(request):
    if not request.session.has_key('currency'):
        request.session['currency']=settings.DEFAULT_CURRENCY
    try:
        try:
            order_id=request.session['cart_id']    
        except:
            order_id=request.session.get['order_id']    
    except:
        pass
    order=Order.objects.all().filter(id=order_id,is_finished=True)        
    if order:
        order_success=Order.objects.get(id=order_id,is_finished=True)
        order_details_success=OrderDetails.objects.filter(order=order_success)
        payment_info=Payment.objects.get(order=order_success)

        context={
            'order_success':order_success,
            'order_details_success':order_details_success,
            'payment_info':payment_info
        }
        messages.success(request,'Congratulations you have made your order it will delevered soon')
        return render(request,'ecommerce/success.html',context)
    else:    
        messages.success(request,'Congratulations you have made your orders it will delevered soon')    
        return render(request,'ecommerce/success-x.html')    

class CancelView(TemplateView):
    template_name = "orders/cancel.html"


def cart_add(request):
    return render(request,'ecommerce/add-cart.html')


def set_currency(request):
    lasturl = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        request.session["currency"] = request.POST["currency"]
        print(request.POST["currency"])

    return HttpResponseRedirect(lasturl)


def product_add(request):
    return render(request,'ecommerce/product-edit.html')
###----------------------------------------------------------------------------------------------
from PIL import Image
from .models import ProductImage


def supplier_add_product(request):
    if not request.user.is_authenticated and request.user.is_anonymous:
        return redirect('/login')

    if request.method == 'POST':
        product_name = request.POST['product_name']
        introduction = request.POST['introduction']
        price = request.POST['price']
        discount = request.POST['discount']
        content = request.POST['content']
        super_category_value = request.POST['super_category_value']
        main_category_value = request.POST['main_category_value']
        sub_category_value = request.POST['sub_category_value']
        mini_category_value = request.POST['mini_category_value']
        # checkbox = request.POST['checkbox']
        # if checkbox:
        #     print("checkbox: ", checkbox)
        available = request.POST['available']
        pieces = request.POST['pieces']
        promotional = request.POST['promotional']
        product_status = int(request.POST['product_status'])
        width = request.POST['width']
        if not width:
            width = None
        product_SKU = request.POST['SKU']
        if not product_SKU:
            product_SKU = None
        height = request.POST['height']
        if not height:
            height = None
        weight = request.POST['weight']
        tags = request.POST['tags']
        if product_status == 1:
            product_status = True
        else:
            product_status = False
        # print(f"product_status: {product_status}", type(product_status))
        try:
            price = float(request.POST["price"])
        except (ValueError, TypeError):
            messages.warning(
                request, '-Please Enter A Valid Pricing number')
            return redirect("/supplier-add-product")

        try:
            discount = float(request.POST["discount"])
        except (ValueError, TypeError):
            discount = 0

        try:
            main_image = request.FILES["main_image"]
        except:
            main_image = None
        if main_image:
            try:
                Image.open(main_image)

            except:
                messages.warning(request, 'sorry, your image is invalid')
                return redirect("/supplier-add-product")

        try:
            name_image_1 = request.FILES["name_image_1"]
        except:
            name_image_1 = None
        if name_image_1:
            try:
                Image.open(name_image_1)

            except:
                messages.warning(request, 'sorry, your image is invalid')
                return redirect("/supplier-add-product")

        try:
            name_image_2 = request.FILES["name_image_2"]
        except:
            name_image_2 = None
        if name_image_2:
            try:
                Image.open(name_image_2)

            except:
                messages.warning(request, 'sorry, your image is invalid')
                return redirect("/supplier-add-product")

        try:
            name_image_3 = request.FILES["name_image_3"]
        except:
            name_image_3 = None
        if name_image_3:
            try:
                Image.open(name_image_3)

            except:
                messages.warning(request, 'sorry, your image is invalid')
                return redirect("/supplier-add-product")

        try:
            name_image_4 = request.FILES["name_image_4"]
        except:
            name_image_4 = None
        if name_image_4:
            try:
                Image.open(name_image_4)

            except:
                messages.warning(request, 'sorry, your image is invalid')
                return redirect("/supplier-add-product")

        try:
            digital_file = request.FILES["digital_file"]
        except:
            digital_file = None

        super_category_obj = SuperCategory.objects.get(id=super_category_value)
        main_category_obj = MainCategory.objects.get(id=main_category_value)
        sub_category_obj = SubCategory.objects.get(id=sub_category_value)
        mini_category_obj = MiniCategory.objects.get(id=mini_category_value)

        product_vendor = Profile.objects.get(user__username=request.user)
        new_product_obj = Product.objects.create(
            product_name=product_name,
            product_description=introduction,
            content=content,
            PRDPrice=price,
            PRDDiscountPrice=discount,
            product_image=main_image,
            digital_file=digital_file,
            additional_image_1=name_image_1,
            additional_image_2=name_image_2,
            additional_image_3=name_image_3,
            additional_image_4=name_image_4,

            # content=description,
            product_vendor=product_vendor,
            product_supercategory=super_category_obj,
            product_maincategory=main_category_obj,
            product_subcategory=sub_category_obj,
            product_minicategor=mini_category_obj,
            available=available,
            pieces=pieces,
            promotional=promotional,
            PRDISactive=product_status,
            width=width,
            height=height,
            PRDWeight=weight,
            PRDSKU=product_SKU,
            PRDtags=tags,
        )
        # print(new_product_obj)
        image_list = [name_image_1, name_image_2, name_image_3, name_image_4]
        for image in image_list:
            if image:
                ProductImage.objects.create(
                    PRDIProduct=new_product_obj,
                    PRDIImage=image
                )
        messages.success(
            request, 'Your Products Has Been Saved !')
        return redirect('/supplier-products-list')

    super_category = SuperCategory.objects.all()
    super_category_first = SuperCategory.objects.all().first()
    main_category = MainCategory.objects.all().filter(
        super_category=super_category_first)
    main_category_first = MainCategory.objects.all().first()
    sub_category = SubCategory.objects.all().filter(
        main_category=main_category_first)
    sub_category_first = SubCategory.objects.all().first()
    mini_category = MiniCategory.objects.all().filter(
        sub_category=sub_category_first
    )
    # print(sub_category)
    context = {
        "super_category": super_category,
        "main_category": main_category,
        "sub_category": sub_category,
        "mini_category": mini_category,
    }
    return render(request, 'ecommerce/product-add.html', context)


class CategoriesJsonListView(View):
    def get(self, *args, **kwargs):
        super_category = list(SuperCategory.objects.all().values())
        super_category_ajax = self.request.GET.get('super_category_ajax')
        main_category_ajax = self.request.GET.get('main_category_ajax')
        sub_category_ajax = self.request.GET.get('sub_category_ajax')

        main_category = list(MainCategory.objects.all().filter(
            super_category__id=super_category_ajax).values())

        sub_category = list(SubCategory.objects.all().filter(
            main_category__id=main_category_ajax).values())
        mini_category = list(MiniCategory.objects.all().filter(
            sub_category__id=sub_category_ajax).values())

        return JsonResponse({"super_category": super_category, "main_category": main_category, "sub_category": sub_category, "mini_category": mini_category, }, safe=False)
###---------------------------------------------------

def supplier_edit_product(request, id):
    product = None
    if not request.user.is_authenticated and request.user.is_anonymous:
        return redirect('/login')

    product_obj = Product.objects.get(id=id)
    if product_obj.product_vendor.user.id == request.user.id:
        if request.method == 'POST':
            product_name = request.POST['product_name']
            introduction = request.POST['introduction']
            content = request.POST['content']
            price = request.POST['price']
            discount = request.POST['discount']
            # description = request.POST['description']
            super_category_value = request.POST['super_category_value']
            main_category_value = request.POST['main_category_value']
            sub_category_value = request.POST['sub_category_value']
            mini_category_value = request.POST['mini_category_value']
            # checkbox = request.POST['checkbox']
            # if checkbox:
            #     print("checkbox: ", checkbox)
            available = request.POST['available']
            pieces = request.POST['pieces']
            promotional = request.POST['promotional']
            product_status = int(request.POST['product_status'])
            width = request.POST['width']
            if not width:
                width = None
            height = request.POST['height']
            if not height:
                height = None
            weight = request.POST['weight']
            product_SKU = request.POST['SKU']
            if not product_SKU:
                product_SKU = None
            tags = request.POST['tags']
            if product_status == 1:
                product_status = True
            else:
                product_status = False
            # print(f"product_status: {product_status}", type(product_status))
            try:
                price = float(request.POST["price"])
            except (ValueError, TypeError):
                messages.warning(
                    request, '-Please Enter A Valid Pricing number')
                return redirect("/supplier-add-product")

            try:
                discount = float(request.POST["discount"])
            except (ValueError, TypeError):
                discount = 0

            try:
                main_image = request.FILES["main_image"]
            except:
                main_image = None
            if main_image:
                try:
                    Image.open(main_image)

                except:
                    messages.warning(request, 'sorry, your image is invalid')
                    return redirect("/supplier-add-product")

            try:
                name_image_1 = request.FILES["name_image_1"]
            except:
                name_image_1 = None
            if name_image_1:
                try:
                    Image.open(name_image_1)

                except:
                    messages.warning(request, 'sorry, your image is invalid')
                    return redirect("/supplier-add-product")

            try:
                name_image_2 = request.FILES["name_image_2"]
            except:
                name_image_2 = None
            if name_image_2:
                try:
                    Image.open(name_image_2)

                except:
                    messages.warning(request, 'sorry, your image is invalid')
                    return redirect("/supplier-add-product")

            try:
                name_image_3 = request.FILES["name_image_3"]
            except:
                name_image_3 = None
            if name_image_3:
                try:
                    Image.open(name_image_3)

                except:
                    messages.warning(request, 'sorry, your image is invalid')
                    return redirect("/supplier-add-product")

            try:
                name_image_4 = request.FILES["name_image_4"]
            except:
                name_image_4 = None
            if name_image_4:
                try:
                    Image.open(name_image_4)

                except:
                    messages.warning(request, 'sorry, your image is invalid')
                    return redirect("/supplier-add-product")

            try:
                digital_file = request.FILES["digital_file"]
            except:
                digital_file = None

            super_category_obj = SuperCategory.objects.get(
                id=super_category_value)
            main_category_obj = MainCategory.objects.get(
                id=main_category_value)
            sub_category_obj = SubCategory.objects.get(id=sub_category_value)
            mini_category_obj = MiniCategory.objects.get(
                id=mini_category_value)

            product_vendor = Profile.objects.get(user__username=request.user)

            new_product_obj = Product.objects.get(id=id)
            new_product_obj.product_name = product_name
            new_product_obj.product_description = introduction
            new_product_obj.content = content
            new_product_obj.PRDPrice = price
            new_product_obj.PRDDiscountPrice = discount
            if main_image:
                new_product_obj.product_image = main_image

            if name_image_1:
                new_product_obj.additional_image_1 = name_image_1

            if name_image_2:
                new_product_obj.additional_image_2 = name_image_2

            if name_image_3:
                new_product_obj.additional_image_3 = name_image_3

            if name_image_4:
                new_product_obj.additional_image_4 = name_image_4

            if digital_file:
                new_product_obj.digital_file = digital_file
            # new_product_obj.content=description,
            new_product_obj.product_vendor = product_vendor
            new_product_obj.product_supercategory = super_category_obj
            new_product_obj.product_maincategory = main_category_obj
            new_product_obj.product_subcategory = sub_category_obj
            new_product_obj.product_minicategor = mini_category_obj
            new_product_obj.available = available
            new_product_obj. pieces = pieces
            new_product_obj.promotional = promotional
            new_product_obj.PRDISactive = product_status
            new_product_obj.width = width
            new_product_obj.height = height
            new_product_obj.PRDWeight = weight
            new_product_obj.PRDSKU = product_SKU
            new_product_obj.PRDtags = tags
            try:
                new_product_obj.save()
            except Exception as e:
                messages.warning(request, "You can't Edit This Product ")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            messages.success(
                request, 'Your Products Has Been Updated !')
            return redirect('/supplier-products-list')

    # product_obj = Product.objects.get(id=id)
    if product_obj.product_vendor.user.id == request.user.id:
        product = Product.objects.all().filter(
            product_vendor__user=request.user, id=id).exists()
        if product:
            product = Product.objects.get(
                product_vendor__user=request.user, id=id)
            product_images = ProductImage.objects.all().filter(PRDIProduct=product)
    super_category = SuperCategory.objects.all()
    super_category_first = SuperCategory.objects.get(
        name=product.product_supercategory)
    main_category = MainCategory.objects.all().filter(
        super_category=super_category_first)
    main_category_first = MainCategory.objects.get(
        name=product.product_maincategory)
    sub_category = SubCategory.objects.all().filter(
        main_category=main_category_first)
    sub_category_first = SubCategory.objects.get(
        name=product.product_subcategory)
    mini_category = MiniCategory.objects.all().filter(
        sub_category=sub_category_first
    )
    # print(sub_category)
    context = {
        "product": product,
        "product_images": product_images,
        "super_category": super_category,
        "main_category": main_category,
        "sub_category": sub_category,
        "mini_category": mini_category,
    }
    return render(request, 'ecommerce/product-edit.html', context)


####---------------------------------------------------    

def supplier_products_list(request):
    return render(request, "ecommerce/product-list.html")


class SupplierProductsJsonListView(View):
    def get(self, *args, **kwargs):
        user = Profile.objects.get(user=self.request.user)
        upper = int(self.request.GET.get('num_products'))
        order_by = self.request.GET.get('order_by')
        order_by_status = self.request.GET.get('order_by_status')

        lower = upper - 5
        if order_by_status == "All":
            products_list = list(Product.objects.all().filter(
                product_vendor=user, PRDISDeleted=False).values().order_by(order_by)[lower:upper])

            products_size = len(Product.objects.all().filter(
                product_vendor=user, PRDISDeleted=False))

            max_size = True if upper >= products_size else False
        elif order_by_status == "Active":
            products_list = list(Product.objects.all().filter(
                product_vendor=user, PRDISactive=True, PRDISDeleted=False).values().order_by(order_by)[lower:upper])

            products_size = len(Product.objects.all().filter(
                product_vendor=user, PRDISactive=True, PRDISDeleted=False))

            max_size = True if upper >= products_size else False
        else:
            products_list = list(Product.objects.all().filter(
                product_vendor=user, PRDISactive=False, PRDISDeleted=False).values().order_by(order_by)[lower:upper])

            products_size = len(Product.objects.all().filter(
                product_vendor=user, PRDISactive=False, PRDISDeleted=False))

            max_size = True if upper >= products_size else False

        return JsonResponse({"data": products_list,  "max": max_size, "products_size": products_size, }, safe=False)


def remove_product(request, id):
    if request.user.is_authenticated and not request.user.is_anonymous and id:
        product_obj = Product.objects.get(id=id)

        if product_obj.product_vendor.user.id == request.user.id:
            product = Product.objects.all().filter(
                product_vendor__user=request.user, id=id).exists()
            if product:
                product = Product.objects.get(
                    product_vendor__user=request.user, id=id)
                product.PRDISDeleted = True
                product.PRDISactive = False
                try:
                    product.save()
                except Exception as e:
                    messages.warning(request, "product You can't delete it !")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

                messages.warning(request, ' Your Product has been deleted ')
                return redirect('/supplier-products-list')
            else:
                messages.warning(
                    request, "product You can't delete it !")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    messages.warning(request, "product You can't delete it !")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def supplier_dashboard(request):
    vendor=Profile.objects.get(user=request.user)
    order_supplier=OrderSupplier.objects.all().filter(vendor=vendor).exclude(status='PENDING')
    products_supplier=Product.objects.all().filter(product_vendor=vendor,PRDISactive=True).order_by('-date')
    orders_underway=OrderSupplier.objects.all().filter(vendor=vendor,status='Underway')
    context={
        'vendor':vendor,
        'order_supplier':order_supplier,
        'products_supplier':products_supplier,
        'orders_underway':orders_underway
    }
    return render(request,'ecommerce/supplier-dashboard.html',context)


# class SupplierOrderJsonListView(View):
#     def get(self,*args,**kwargs):
#         user=Profile.objects.get(user=self.request.user)    
#         upper=int(self.request.GET.get("num_products"))
#         order_by=self.request.GET.get('order_by')
#         order_by_status=self.request.GET.get('oreder_by_status')
#         lower=upper - 5
#         if order_by_status == 'All':
#             order_list=list(OrderSupplier.objects.all().filter(vendor=user,is_finished=True).values().order_by(order_by)[lower:upper])
#             order_size=len(OrderSupplier.objects.all().filter(vendor=user,is_finished=True))
#             max_size=True if upper >=order_size else False
#         elif order_by_status == 'Underway':
#             order_list=list(OrderSupplier.objects.all().filter(vendor=user,status='Underway',is_finished=True).values().order_by(order_by)[lower:upper])    
#             order_size=len(OrderSupplier.objects.all().filter(vendor=user,status='Underway',is_finished=True))
#             max_size=True if upper >=order_size else False
#         elif order_by_status == 'COMPLETE':
#             order_list=list(OrderSupplier.objects.all().filter(vendor=user,status='COMPLETE',is_finished=True).values().order_by(order_by)[lower:upper])    
#             order_size=len(OrderSupplier.objects.all().filter(vendor=user,status='COMPLETE',is_finished=True))
#             max_size=True if upper >=order_size else False
#         else:
#             order_list=list(OrderSupplier.objects.all().filter(vendor=user,status='Refunded',is_finished=True).values().order_by(order_by)[lower:upper])    
#             order_size=len(OrderSupplier.objects.all().filter(vendor=user,status='Refunded',is_finished=True))
#             max_size=True if upper >=order_size else False
#         return JsonResponse({'data':order_list,'max_size':max_size,'orders_size':order_size},safe=False)    





class SupplierOrdersJsonListView(View):
    def get(self, *args, **kwargs):
        user = Profile.objects.get(user=self.request.user)
        upper = int(self.request.GET.get('num_products'))
        order_by = self.request.GET.get('order_by')
        order_by_status = self.request.GET.get('order_by_status')

        lower = upper - 5
        if order_by_status == "All":
            orders_list = list(OrderSupplier.objects.all().filter(
                vendor=user, is_finished=True).values().order_by(order_by)[lower:upper])

            orders_size = len(OrderSupplier.objects.all().filter(
                vendor=user, is_finished=True))

            max_size = True if upper >= orders_size else False

        elif order_by_status == "Underway":
            orders_list = list(OrderSupplier.objects.all().filter(
                vendor=user, status="Underway", is_finished=True).values().order_by(order_by)[lower:upper])

            orders_size = len(OrderSupplier.objects.all().filter(
                vendor=user, status="Underway", is_finished=True))

            max_size = True if upper >= orders_size else False

        elif order_by_status == "COMPLETE":
            orders_list = list(OrderSupplier.objects.all().filter(
                vendor=user, status="COMPLETE", is_finished=True).values().order_by(order_by)[lower:upper])

            orders_size = len(OrderSupplier.objects.all().filter(
                vendor=user, status="COMPLETE", is_finished=True))

            max_size = True if upper >= orders_size else False

        else:
            orders_list = list(OrderSupplier.objects.all().filter(
                vendor=user, status="Refunded", is_finished=True).values().order_by(order_by)[lower:upper])

            orders_size = len(OrderSupplier.objects.all().filter(
                vendor=user, status="Refunded", is_finished=True))

            max_size = True if upper >= orders_size else False

        return JsonResponse({"data": orders_list,  "max": max_size, "orders_size": orders_size, }, safe=False)



def supplier_order_details(request,id):
    user=Profile.objects.get(user=request.user)
    order_supplier=get_object_or_404(OrderSupplier,id=id,is_finished=True,vendor=user)
    payment_info=Payment.objects.get(order=order_supplier.order)
    order_details_supplier=OrderDetailsSupplier.objects.all().filter(order_supplier=order_supplier,supplier=request.user)
    context={
        'order_supplier':order_supplier,
        'payment_info':payment_info,
        'order_details_supplier':order_details_supplier
    }
    return render(request,'ecommerce/supplier-order-detail.html',context)


def supplier_bank_info(request):
    context=None
    if request.user.is_authenticated and not request.user.is_anonymous:
        if request.method == 'POST':
            bank_name=request.POST["bank_name"]
            account_number=request.POST["account_number"]
            account_name=request.POST["account_name"]
            ifsc=request.POST["ifsc"]
            swift_code=request.POST["swift_code"]
            country=request.POST["country"]
            paypal_email=request.POST["paypal_email"]
            description=request.POST['description']
            profile=Profile.objects.get(user=request.user)
            if BankAccount.objects.all().filter(vendor_profile=profile,).exists():
                old_bank_info=BankAccount.objects.get(vendor_profile=profile,)
                old_bank_info.bank_name=bank_name
                old_bank_info.account_number=account_number
                old_bank_info.account_name=account_name
                old_bank_info.ifsc=ifsc
                old_bank_info.swift_code=swift_code
                old_bank_info.country=country
                old_bank_info.paypal_email=paypal_email
                old_bank_info.description=description
                old_bank_info.save()
                messages.success(request,'your bank info has been saved !')
            else:
                new_bank_info=BankAccount.objects.create(
                    vendor_profile=profile,
                    bank_name=bank_name,
                    account_name=account_name,
                    account_number=account_number,
                    ifsc=ifsc,
                    swift_code=swift_code,
                    country=country,
                    paypal_email=paypal_email,
                    description=description
                )   
                messages.success(request,'your bank details has been saved !') 
                # return render(request,'ecommerce/vendor-bank-info.html')
        if BankAccount.objects.all().filter(vendor_profile__user=request.user,).exists():
            bank_info_object=BankAccount.objects.get(vendor_profile__user=request.user,)
            context={
                "bank_info_obj":bank_info_object
            }
        return render(request,'ecommerce/vendor-bank-info.html',context)
    else:
        messages.warning(request,'please login first !') 
        return redirect('/login')  


def payments(request):
    if request.user.is_authenticated and not request.user.is_anonymous:
        vendor=Profile.objects.get(user=request.user)
        payments=VendorPayments.objects.all().filter(vendor_profile__username=request.user)
        bank_info_object=BankAccount.objects.all().filter(vendor_profile__user=request.user).first()
        paginator=Paginator(payments,10)
        page=request.GET.get('page')
        try:
            payments=paginator.page(page)
        except PageNotAnInteger:
            payments=paginator.page(1)    
        except EmptyPage:
            payments=paginator.page(paginator.num_page)    
        context={
            'vendor':vendor,
            'payments':payments,
            'bank_info_obj':bank_info_object,
            'paginator':paginator,
            'page':page
        }  
        return render(request,'ecommerce/payment-request.html',context)  
    else:
        messages.warning(request,'Please login first')    
        return redirect('/login')


def request_payment(request):
    if request.user.is_authenticated and not request.user.is_anonymous:
        if request.method == 'POST':
            try:
                request_amount=float(request.POST['request_amount'])
                description=request.POST['description']
                profile=Profile.objects.get(user=request.user)
                method=request.POST['method']
                if profile.blance >= request_amount:
                    profile.requested=request_amount
                    profile.blance=profile.blance - request_amount
                    if method == 'Paypal' or method == 'Bank':
                        VendorPayments.objects.create(
                            vendor_profile=request.user,
                            request_amount=request_amount,
                            method=method,
                            description=description,
                        )
                        print(profile)

                        profile.save()
                        messages.success(request,'Your request has been recived')
                        return redirect('/payments')
                else:
                    messages.warning(request,'You have not enough balance')        
                    return redirect('/payments')
            except (ValueError,TypeError):
                messages.warning(request,'please enter a valid number')        
                return redirect('/payments')
        return redirect('/payments')        
    else:
        messages.warning(request,'Please login first !')    
        return redirect('/login')

from datetime import date


class chartJsonListView(View):
    def get(self, *args, **kwargs):
        today = date.today()
        if self.request.user.is_authenticated and not self.request.user.is_anonymous:
            vendor = Profile.objects.get(user=self.request.user)

            product_count_list = []
            order_count_list = []
            for i in range(1, 13):
                product_count = Product.objects.filter(
                    product_vendor=vendor,  date__year=today.year, date__month=i,).count()
                product_count_list.append(product_count)
                order_count = OrderSupplier.objects.all().filter(vendor=vendor, order_date__year=today.year,
                                                                 order_date__month=i,).exclude(status="PENDING").count()
                order_count_list.append(order_count)

            return JsonResponse({"product_count_list": product_count_list, "order_count_list": order_count_list, }, safe=False)

       