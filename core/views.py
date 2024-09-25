from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from core.serializers import BaseSerializer


import keys
from core.methods import PageNumberPaginationWithoutCount


class CustomSearchFilter(SearchFilter):
    def get_search_terms(self, request):
        """
        Search terms are set by a ?search=... query parameter,
        and may be comma and/or whitespace delimited.
        """
        params = request.query_params.get(self.search_param, None)
        if params:
            params = params.replace('\x00', '')  # strip null characters
            params = params.replace(',', ':')
            return params.split(sep=":")
        else:
            return None

    def filter_queryset(self, request, queryset, view):
        return super().filter_queryset(request, queryset, view)


class ModelPaginationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPaginationWithoutCount
    filter_backends = [CustomSearchFilter, DjangoFilterBackend, OrderingFilter]

    user = None
    fields = None
    default_fields = None
    serializer_context = {}
    exclude_fields = []

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.user = request.user

        self.serializer_context = self.get_serializer_context()
        self.serializer_context['request'] = request
        self.serializer_context['action'] = self.action

        if self.pagination_class is not None:
            page_size = int(request.query_params.get('page_size', 10))
            self.pagination_class.page_size = page_size

        try:
            request.data._mutable = True
        except Exception as e:
            pass

        custom_fields = request.query_params.get(keys.KEY_FIELDS, None)
        if custom_fields:
            self.fields = self.default_fields + custom_fields.split(",")
        else:
            self.fields = self.default_fields
            


    def get_serializer_context(self):
        context = super().get_serializer_context()
        depth = 0
        try:
            depth = int(self.request.query_params.get('depth', 1))
        except ValueError:
            pass

        context['depth'] = depth

        return context

    def is_action_detail(self, action_name):

        if action_name == 'retrieve':
            return True

        try:
            action = getattr(self, action_name)
            return getattr(action, 'detail', False)
        except AttributeError:
            return False

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(
            page, many=True,
            fields=self.fields if self.fields else None,
            context=self.serializer_context,
            exclude=self.exclude_fields
        )

        return self.get_paginated_response(serializer.data)
    
    def get_serializer(self, *args, **kwargs):
        if isinstance(self.get_serializer_class(), BaseSerializer):
            if self.exclude_fields:
                kwargs.setdefault('exclude', self.exclude_fields)
        return super().get_serializer(*args, **kwargs)
