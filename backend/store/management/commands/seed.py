from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Collection, Product, Customer, Order, OrderItem

class Command(BaseCommand):
    help = 'Insert sample data'

    def handle(self, *args, **options):
        c1, _ = Collection.objects.get_or_create(title='Default')
        c2, _ = Collection.objects.get_or_create(title='Featured')

        p1, _ = Product.objects.get_or_create(title='Sample Product 1', slug='sample-product-1', price=19.99, inventory=100, collection=c1)
        p2, _ = Product.objects.get_or_create(title='Sample Product 2', slug='sample-product-2', price=49.99, inventory=50, collection=c2, featured=True)

        user, _ = User.objects.get_or_create(username='demo', defaults={'email': 'demo@example.com'})
        user.set_password('demo1234')
        user.save()
        cust, _ = Customer.objects.get_or_create(user=user, first_name='Demo', last_name='User', email='demo@example.com')

        order, _ = Order.objects.get_or_create(customer=cust)
        OrderItem.objects.get_or_create(order=order, product=p1, quantity=2, unit_price=p1.price)
        OrderItem.objects.get_or_create(order=order, product=p2, quantity=1, unit_price=p2.price)
        order.total = p1.price * 2 + p2.price
        order.save()
        self.stdout.write(self.style.SUCCESS('Seed data inserted'))