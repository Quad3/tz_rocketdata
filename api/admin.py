from django.contrib import admin

from .models import (
    Address,
    Contact,
    Producer,
    Product,
    Employee,
)


admin.site.register([
    Address,
    Contact,
    Producer,
    Product,
    Employee,
])
