from django.shortcuts import render


def authenticate_user(myfunc):
    def inner(request):
        if request.user.is_authenticated:
            return render(request,'management/dashboard.html')
        else:
            return myfunc(request)
    return inner    