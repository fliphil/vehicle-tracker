from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from .models import Vehicle
from django.contrib.auth.models import User
from .models import VehicleStatus
from .models import UserStatus
from .models import TripReservation


class VehicleTestCase(TestCase):
    def setUp(self):
        Vehicle.objects.create(desc="Corolla",
                               odometer=100)

    def test_sanity(self):
        """
        Test the sanity of Vehicle entry creation.
        :return:
        """
        car = Vehicle.objects.get(desc="Corolla")

        self.assertEqual(car.odometer, 100)
        self.assertIsNotNone(car.photo)
        self.assertEqual(str(car), "Corolla")

    def test_vehicle_status(self):
        """
        Ensure a valid VehicleStatus table entry was automatically created.
        :return:
        """
        car = Vehicle.objects.get(desc="Corolla")
        status = VehicleStatus.objects.get(vehicle=car)

        self.assertFalse(status.on_trip)
        self.assertIsNone(status.most_recent_trip)

    def test_delete(self):
        car = Vehicle.objects.get(desc="Corolla")
        car.delete()

        # Make sure the user was deleted
        try:
            Vehicle.objects.get(desc="Corolla")
            deleted = False
        except ObjectDoesNotExist:
            deleted = True
        self.assertTrue(deleted, "Vehicle entry was not deleted properly")

        # Make sure the delete cascaded to the UserStatus
        try:
            VehicleStatus.objects.get(vehicle=car)
            deleted = False
        except ObjectDoesNotExist:
            deleted = True
        self.assertTrue(deleted, "VehicleStatus entry was not deleted properly")


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="coolbob",
                            first_name="Bob",
                            last_name="Smith",
                            email="blah@...",
                            password="secret")

    def test_sanity(self):
        """
        Test the sanity of User entry creation.
        :return:
        """
        user = User.objects.get(username="coolbob")

        self.assertEqual(user.first_name, "Bob")
        self.assertEqual(user.last_name, "Smith")
        self.assertEqual(user.email, "blah@...")
        self.assertEqual(user.password, "secret")

    def test_user_status(self):
        """
        Ensure a valid UserStatus table entry was automatically created.
        :return:
        """
        user = User.objects.get(username="coolbob")
        status = UserStatus.objects.get(user=user)

        self.assertFalse(status.on_trip)
        self.assertIsNone(status.most_recent_trip)

    def test_delete(self):
        user = User.objects.get(username="coolbob")
        user.delete()

        # Make sure the user was deleted
        try:
            User.objects.get(username="coolbob")
            deleted = False
        except ObjectDoesNotExist:
            deleted = True
        self.assertTrue(deleted, "User entry was not deleted properly")

        # Make sure the delete cascaded to the UserStatus
        try:
            UserStatus.objects.get(user=user)
            deleted = False
        except ObjectDoesNotExist:
            deleted = True
        self.assertTrue(deleted, "UserStatus entry was not deleted properly")


class TripTestCase(TestCase):
    def setUp(self):
        vehicle = Vehicle.objects.create(desc="Ferrari",
                                         odometer=500)

        user = User.objects.create(username="coolalice",
                            first_name="Alice",
                            last_name="Wonder",
                            password="dummy")

        TripReservation.objects.create(user=user,
                                       vehicle=vehicle,
                                       pre_odometer=vehicle.odometer)

    def test_sanity(self):
        """
        Test the sanity of Vehicle entry creation.
        :return:
        """
        trip = TripReservation.objects.get(pk=1)

        user = User.objects.get(username="coolalice")
        vehicle = Vehicle.objects.get(desc="Ferrari")

        self.assertEqual(trip.user, user)
        self.assertEqual(trip.user_first_name, user.first_name)
        self.assertEqual(trip.user_last_name, user.last_name)
        self.assertEqual(trip.vehicle, vehicle)
        self.assertEqual(trip.vehicle_desc, vehicle.desc)
        self.assertIsNotNone(trip.time_check_out)
        self.assertEqual(str(trip), str(trip.time_check_out) + '-' + \
                                    str(trip.user_first_name) + '_' + \
                                    str(trip.user_last_name) + '-' + \
                                    str(trip.vehicle_desc))
