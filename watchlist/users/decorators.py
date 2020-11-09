from django.shortcuts import redirect

# when user views register, login page then
# redirect to home if user is already logged in
def redirect_if_logged(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func