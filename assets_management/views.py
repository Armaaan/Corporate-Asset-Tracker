from rest_framework import generics
from .models import Company, Employee, Device, Assignment
from .serializers import CompanySerializer, EmployeeSerializer, DeviceSerializer, AssignmentSerializer


class CompanyListCreateView(generics.ListCreateAPIView):
    """ This view handles the GET and POST requests to retrieve a
    list of all companies or create a new company respectively. """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """ This view handles GET, PUT, PATCH and DELETE requests to
    retrieve, update or delete a specific company object. """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class EmployeeListCreateView(generics.ListCreateAPIView):
    """ This view handles the GET and POST requests to retrieve a
    list of all employees or create a new employee respectively.  """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """ This view handles GET, PUT, PATCH and DELETE requests to
    retrieve, update or delete a specific employee object. """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class DeviceListCreateView(generics.ListCreateAPIView):
    """ This view handles the GET and POST requests to retrieve a
    list of all devices or create a new device respectively. """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class DeviceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """ This view handles GET, PUT, PATCH and DELETE requests to
    retrieve, update or delete a specific device object. """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class AssignmentListCreateView(generics.ListCreateAPIView):
    """ This view handles the GET and POST requests to retrieve a list
    of all assignments or create a new assignment respectively. """
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer


class AssignmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """ This view handles GET, PUT, PATCH and DELETE requests to
    retrieve, update or delete a specific assignment object. """
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
