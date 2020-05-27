# Create your views here.
from .models import Movie
from .serializers import MovieSerializer
from rest_framework import generics, viewsets, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class DynamicSearchFilter(filters.SearchFilter):
    """
    get_search_fields function is overridden from the parent SearchFilter and it returns
    'name' as the default field if no 'search_field' parameter is present, and all the fields present in
    the 'search_field' parameter if it is present.
    """
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', ['name'])


class MovieViewset(viewsets.ModelViewSet):
    """
    Model viewset that uses Generic API view and different mixins to provide default CRUD operations
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = (DynamicSearchFilter,)

    # Overriding the default get_permission to allow only authenticated users to perform GET method on the API
    # And allow only Admin users to execute POST, PUT and PATCH methods, to create or update the movie data
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
