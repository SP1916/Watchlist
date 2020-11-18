from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from .models import Movies
from .forms import MovieForm
from .filters import MovieFilter, MovieToWatchFilter
from django.contrib.auth.models import User


# redirect to recommendations page if not logged in
@login_required(login_url='movietowatch')
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


def movie_to_watch(request):
    if request.user.is_authenticated:
# show all movies as recommendations except movies watchlisted by user
# the titles of movies watchlisted by user is stored in a list
# that list is excluded while showing movies for recommendations
        watchlisted_movies = [movie.title for movie in request.user.movies_set.all()]
        movies = Movies.objects.exclude(title__in=watchlisted_movies)
    else:
        movies = Movies.objects.all()

# if two users have same movie then it is repeated in recommendations 
# so id of repeated movies are stored in exclude_id and excluded from query set
    seen_title = []
    exclude_id = []
    for obj in movies:
        if obj.title in seen_title:
            exclude_id += [obj.id]
        else:
            seen_title += [obj.title]
    movies = movies.exclude(id__in=exclude_id).order_by('-year')

# djnago filter
    filter = MovieToWatchFilter(request.GET, queryset=movies)
    movies = filter.qs

    context = {
        'movies': movies,
        'filter': filter
    }
    return render(request, 'movies/movie_to_watch.html', context)


@login_required(login_url='login')
def add_movietowatch(request, pk):
# add movies from recommendations to watchlist
    movie = Movies.objects.get(id=pk)
    Movies.objects.create(
        user=request.user,
        title=movie.title,
        year=movie.year,
        genre=movie.genre
    )
    return redirect('movietowatch')



# admin_home = user status page
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