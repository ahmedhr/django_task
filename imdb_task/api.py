from rest_framework import routers
from api import views as imdb_views

router = routers.DefaultRouter()
router.register('imdb/movies', imdb_views.MovieViewset)
