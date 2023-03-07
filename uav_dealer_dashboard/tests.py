from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import uavDealer
from customer_dashboard.models import Orders
class OrderListTestCase(TestCase):
    """
    Test the `order_list` view function.
    """
    def setUp(self):
        """
        Set up the test by creating a client, a user, a UAV dealer, and orders.
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.uav_dealer = uavDealer.objects.create(car_dealer=self.user, name='Test Dealer', wallet=500)
        self.order1 = Orders.objects.create(uav_dealer=self.uav_dealer, is_complete=True)
        self.order2 = Orders.objects.create(uav_dealer=self.uav_dealer, is_complete=False)
        self.order3 = Orders.objects.create(uav_dealer=self.uav_dealer, is_complete=False)

    def test_order_list(self):
        """
        Test that the `order_list` view function correctly retrieves the orders of the authenticated UAV dealer that
        are not complete and renders the uav_dealer_order_list.html template with the correct context.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('order_list'))

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Assert that the correct order_list is passed to the template
        self.assertQuerysetEqual(response.context['order_list'], [repr(self.order2), repr(self.order3)], ordered=False)

        # Assert that the template used to render the response is uav_dealer_order_list.html
        self.assertTemplateUsed(response, 'uav_dealer_order_list.html')
