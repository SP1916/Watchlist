from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from .models import Movies
from .forms import MovieForm
from .filters import MovieFilter
from django.contrib.auth.models import User


def admin_home(request):
# Check if admin or not
    if not request.user.is_staff:
        return redirect('home')

    users = User.objects.all()
    movies = Movies.objects.all()
    context = {
        'users': users,
        'total_movies': movies.count(),
        'total_users': users.count()
    }
    return render(request, 'movies/admin_home.html', context)


@login_required(login_url='login')
def home(request):
    movies = request.user.movies_set.all()

# djnago filter
    filter = MovieFilter(request.GET, queryset=movies)
    movies = filter.qs

    context = {
        'movies': movies.order_by('-id'),
        'total_movies': movies.count(),
        'unwatched': movies.filter(status=False).count(),
        'filter': filter
    }
    return render(request, 'movies/index.html', context)


@login_required(login_url='login')
def create(request):
    if request.POST:
        form = MovieForm(request.POST)
# assign user to form
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            return redirect('home')
    else: 
        form = MovieForm()

    context = {'form': form}
    return render(request, 'movies/create.html', context)


@login_required(login_url='login')
def update(request, pk):
    movie = Movies.objects.get(id=pk)

    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        form.save()
        return redirect('home')
    else:
        form = MovieForm(instance=movie)

    context = {'form': form}
    return render(request, 'movies/create.html', context)


@login_required(login_url='login')
def changeStatus(request, pk):
    movie = Movies.objects.get(id=pk)
    movie.status = not movie.status
    movie.save()
    return redirect('home')


@login_required(login_url='login')
def delete(request, pk):
    movie = Movies.objects.get(id=pk)
    movie.delete()
    return redirect('home')
