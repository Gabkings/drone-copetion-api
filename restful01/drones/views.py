from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drones.custompermission import IsCurrentUserOrReadOnly
from django_filters import FilterSet
from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter
from drones.models import Drone,Pilot,DroneCategory,Competition
from drones.serializers import DroneCategorySerializer
from drones.serializers import DroneSerializer,PilotSerializer,CompetitionSerializer,PilotCompetionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class DroneCategoryList(generics.ListCreateAPIView):
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    name = 'dronecategory-list'
    filter_fields = ('name',)
    search_fields = ('^name',)
    ordering_fields = ('name',)


class DroneCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    name = 'dronecategory-detail'

class DroneList(generics.ListCreateAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = 'drone-list'
    filter_fields=(
    'name',
    'drone_category',
    'manufacturing_date',
    'has_it_competed',
    )
    search_fields=(
    '^name',
    )
    ordering_fields=(
    'name',
    'manufacturing_date',
    )

    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsCurrentUserOrReadOnly,
    )

    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)

class DroneDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = 'drone-detail'
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsCurrentUserOrReadOnly,
    )

class PilotList(generics.ListCreateAPIView):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = 'pilot-list'
    filter_fields=(
    'name',
    'gender',
    'race_count',
    )
    search_fields=(
    '^name',
    )
    ordering_fields=(
    'name',
    'race_count'
    )

    authentication_classes =(
    	TokenAuthentication,
    )
    permission_classes = (
    	IsAuthenticated,
    )

class PilotDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = 'pilot-detail'
    authentication_classes =(
    	TokenAuthentication,
    )
    permission_classes = (
    	IsAuthenticated,
    )
class CompetitionFilter(FilterSet):
    from_achievement_date = DateTimeFilter(
        field_name='distance_achievement_date', lookup_expr='gte')
    to_achievement_date = DateTimeFilter(
        field_name='distance_achievement_date', lookup_expr='lte')
    min_distance_in_feet = NumberFilter(
        field_name='distance_in_feet', lookup_expr='gte')
    max_distance_in_feet = NumberFilter(
        field_name='distance_in_feet', lookup_expr='lte')
    drone_name = AllValuesFilter(
        field_name='drone__name')
    pilot_name = AllValuesFilter(
        field_name='pilot__name')

    class Meta:
        model = Competition
        fields = (
            'distance_in_feet',
            'from_achievement_date',
            'to_achievement_date',
            'min_distance_in_feet',
            'max_distance_in_feet',
            # drone__name will be accessed as drone_name
            'drone_name',
            # pilot__name will be accessed as pilot_name
            'pilot_name',
        )
class CompetitionList(generics.ListCreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetionSerializer
    name = 'competion-list'
    filter_class = CompetitionFilter
    ordering_fields = (
        'distance_in_feet',
        'distance_achivement_date',
    )

class CompetitionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetionSerializer
    name = 'competition-detail'

class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self,request,*args,**kwargs):
        return Response({
		'drone-categories':	reverse(DroneCategoryList.name,	request=request),
		'drones':reverse(DroneList.name,request=request),
		'pilots':reverse(PilotList.name,request=request),
		'competitions':reverse(CompetitionList.name,request=request)
        })
