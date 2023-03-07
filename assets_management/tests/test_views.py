from model_bakery import baker
from datetime import datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from assets_management.models import Company, Employee, Device, Assignment
from assets_management.serializers import CompanySerializer, DeviceSerializer


class CompanyListCreateViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('company-list')
        self.company_data = {'name': 'Acme Corp', 'description': 'A company'}

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
        self.url = reverse('company-detail', kwargs={'pk': self.company.pk})
        self.valid_payload = {'name': 'New name', 'description': 'New description'}
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
        self.url = reverse('employee-list-create')

    def test_get_employee_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee_list.html')

    def test_create_employee(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
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
        self.url = reverse('employee-detail', args=[self.employee.id])

    def test_get_employee_detail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee_detail.html')

    def test_update_employee(self):
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@example.com',
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
        self.device_data = {'name': 'iPhone', 'description': 'Smartphone', 'serial_number': '1234567890',
                            'condition': 'Good'}
        self.response = self.client.post(reverse('device-list'), self.device_data, format='json')

    def test_create_device(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_get_devices(self):
        devices = Device.objects.all()
        serializer = DeviceSerializer(devices, many=True)
        self.assertEqual(self.response.data, serializer.data)


class DeviceRetrieveUpdateDestroyViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.device = baker.make('core.Device')
        self.valid_payload = {'name': 'Updated Device', 'condition': 'Fair'}
        self.invalid_payload = {'name': '', 'condition': 'Poor'}
        self.update_url = reverse('device-detail', kwargs={'pk': self.device.pk})
        self.delete_url = reverse('device-detail', kwargs={'pk': self.device.pk})

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
        self.device = baker.make(Device)
        self.employee = baker.make(Employee)
        self.url = reverse('assignment-list-create')
        self.data = {
            'device': self.device.id,
            'employee': self.employee.id,
            'checkout_time': datetime.now(),
            'checkin_time': None,
            'condition': 'Good',
            'returned_condition': None
        }

    def test_create_assignment(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Assignment.objects.count(), 1)
        self.assertEqual(Assignment.objects.get().device, self.device)

    def test_list_assignments(self):
        baker.make(Assignment, _quantity=3)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)


class AssignmentRetrieveUpdateDestroyViewTest(APITestCase):
    def setUp(self):
        self.assignment = baker.make(Assignment)
        self.url = reverse('assignment-detail', kwargs={'pk': self.assignment.pk})
        self.data = {
            'device': self.assignment.device.id,
            'employee': self.assignment.employee.id,
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
