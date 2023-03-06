import django_filters

from users.models import User

class UserListFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='contains', label='First name')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='contains', label='Last name')
    profession_title = django_filters.CharFilter(field_name='profession_title', lookup_expr='contains', label='Profession title')
    workplace = django_filters.CharFilter(field_name='workplace', lookup_expr='contains', label='Workplace')
    city = django_filters.CharFilter(field_name='city', lookup_expr='contains', label='City')

    def __init__(self, data, *args, **kwargs):
        data = data.copy()
        data.setdefault('format', 'paperback')
        data.setdefault('order', '-added')
        super().__init__(data, *args, **kwargs)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profession_title', 'workplace', 'country', 'city']