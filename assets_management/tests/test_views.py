from model_bakery import baker
from datetime import datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from assets_management.models import Company, Employee, Device, Assignment
from assets_management.serializers import CompanySerializer, DeviceSerializer, AssignmentSerializer


class CompanyListCreateViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('company_list_create')
        self.company_data = {
            'name': 'Acme Corp',
            'address': 'Dhaka',
            'phone_number': '+8801777777777',
            'website': 'https://www.youtube.com/',
            'description': 'A company'
        }

    def test_create_company(self):
        response = self.client.post(self.url, self.company_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Company.objects.get().name, 'Acme Corp')

    def test_list_companies(self):
        baker.make(Company, _quantity=3)
        response = self.client.get(self.url)
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CompanyRetrieveUpdateDestroyViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.company = baker.make(Company)
        self.url = reverse('company_retrieve_update_destroy', kwargs={'pk': self.company.pk})
        self.valid_payload = {
            'name': 'New name',
            'address': 'Chittagong',
            'phone_number': '+8801888888888',
            'website': 'https://www.google.com/',
            'description': 'New description'}
        self.invalid_payload = {'name': '', 'description': 'New description'}

    def test_retrieve_company(self):
        response = self.client.get(self.url)
        company = Company.objects.get(pk=self.company.pk)
        serializer = CompanySerializer(company)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_company_valid_payload(self):
        response = self.client.put(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Company.objects.get(pk=self.company.pk).name, 'New name')

    def test_update_company_invalid_payload(self):
        response = self.client.put(self.url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_company(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Company.objects.count(), 0)


class EmployeeListCreateViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.company = baker.make(Company)
        self.url = reverse('employee_list_create')

    def test_get_employee_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_employee(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'departments': 'sales',
            'position': 'executive',
            'company': self.company.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(Employee.objects.first().first_name, 'John')


class EmployeeRetrieveUpdateDestroyViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.company = baker.make(Company)
        self.employee = baker.make(Employee, company=self.company)
        self.url = reverse('employee_retrieve_update_destroy', args=[self.employee.id])

    def test_get_employee_detail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_employee(self):
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@example.com',
            'departments': 'marketing',
            'position': 'digital marketer',
            'company': self.company.id
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Employee.objects.first().first_name, 'Jane')

    def test_delete_employee(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Employee.objects.count(), 0)


class DeviceListCreateViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.company = baker.make(Company)
        self.device_data = {'name': 'iPhone',
                            'description': 'Smartphone',
                            'serial_number': '1234567890',
                            'condition': 'Good',
                            'company': self.company.id
                            }
        self.url = reverse('device_list_create')
        self.response = self.client.post(reverse('device_list_create'), self.device_data, format='json')

    def test_create_device(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_get_devices(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class DeviceRetrieveUpdateDestroyViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.device = baker.make('Device')
        self.valid_payload = {'name': 'Updated Device', 'condition': 'Fair'}
        self.invalid_payload = {'name': '', 'condition': 'Poor'}
        self.update_url = reverse('device_retrieve_update_destroy', kwargs={'pk': self.device.pk})
        self.delete_url = reverse('device_retrieve_update_destroy', kwargs={'pk': self.device.pk})

    def test_valid_update_device(self):
        response = self.client.patch(self.update_url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_device(self):
        response = self.client.patch(self.update_url, data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_device(self):
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AssignmentListCreateViewTest(APITestCase):
    def setUp(self):
        self.company = baker.make(Company)
        self.employee = baker.make(Employee)
        self.device = baker.make(Device)
        self.url = reverse('assignment_list_create')
        self.data = {
            'company': self.company.id,
            'device': self.device.id,
            'employee': self.employee.id,
            'checkout_time': datetime.now(),
            'checkin_time': datetime.now(),
            'condition': 'Good',
            'returned_condition': 'Good'
        }

    def test_create_assignment(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Assignment.objects.count(), 1)
        self.assertEqual(Assignment.objects.get().device, self.device)

    # def test_list_assignments(self):
    #     baker.make(Assignment, _quantity=3)
    #     response = self.client.get(self.url)
    #     companies = Assignment.objects.all()
    #     serializer = AssignmentSerializer(companies, many=True)
    #     self.assertEqual(response.data, serializer.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)


class AssignmentRetrieveUpdateDestroyViewTest(APITestCase):
    def setUp(self):
        self.assignment = baker.make(Assignment)
        self.url = reverse('assignment_retrieve_update_destroy', kwargs={'pk': self.assignment.pk})
        self.data = {
            'device': self.assignment.device.id,
            'employee': self.assignment.employee.id,
            'company': self.assignment.company.id,
            'checkout_time': self.assignment.checkout_time,
            'checkin_time': datetime.now(),
            'condition': 'Damaged',
            'returned_condition': 'Damaged'
        }

    def test_retrieve_assignment(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['device'], self.assignment.device.id)

    def test_update_assignment(self):
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assignment.refresh_from_db()
        self.assertEqual(self.assignment.condition, 'Damaged')

    def test_partial_update_assignment(self):
        response = self.client.patch(self.url, {'condition': 'Broken'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assignment.refresh_from_db()
        self.assertEqual(self.assignment.condition, 'Broken')

    def test_delete_assignment(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Assignment.objects.filter(pk=self.assignment.pk).exists())
