from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Orders, Vehicles, uavDealer

class UpdateOrderTestCase(TestCase):
    """
    Test the `update_order` view function.
    """
    def setUp(self):
        """
        Set up the test by creating a client, a user, a vehicle, a UAV dealer, and an order.
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.vehicle = Vehicles.objects.create(capacity=10, is_available=False)
        self.uav_dealer = uavDealer.objects.create(name='Test Dealer', wallet=500)
        self.order = Orders.objects.create(vehicle=self.vehicle, uav_dealer=self.uav_dealer, rent=100)

    def test_update_order(self):
        """
        Test that the `update_order` view function correctly updates the order, vehicle, and UAV dealer, and
        renders the customer_confirmation.html template with the correct context.
        """
        self.client.login(username='testuser', password='testpass')
        data = {'id': self.order.id}
        response = self.client.post(reverse('update_order'), data)

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Assert that the vehicle is now available
        self.assertTrue(Vehicles.objects.get(id=self.vehicle.id).is_available)

        # Assert that the UAV dealer's wallet has been deducted by the correct amount
        self.assertEqual(uavDealer.objects.get(id=self.uav_dealer.id).wallet, 400)

        # Assert that the order has been deleted
        self.assertFalse(Orders.objects.filter(id=self.order.id).exists())

        # Assert that the template used to render the response is customer_confirmation.html
        self.assertTemplateUsed(response, 'customer_confirmation.html')

        # Assert that the context passed to the template is correct
        self.assertEqual(response.context['vehicle'], self.vehicle)
        self.assertEqual(response.context['cost_per_day'], self.vehicle.capacity * 13)
