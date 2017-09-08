from django.contrib.auth.models import User , Group
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings as globalSettings
# Related to the REST Framework
from rest_framework import viewsets , permissions , serializers
from rest_framework.exceptions import *
from url_filter.integrations.drf import DjangoFilterBackend
from .serializers import *
from API.permissions import *
from django.db.models import Q
from allauth.account.adapter import DefaultAccountAdapter
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from ERP.models import service
# Create your views here.

class ContactLiteViewSet(viewsets.ModelViewSet):
    permission_classes = (isOwner , )
    serializer_class = ContactLiteSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name', 'company' , 'mobile', 'email']
    def get_queryset(self):
        return Contact.objects.all()

class ContactViewSet(viewsets.ModelViewSet):
    permission_classes = (isOwner , )
    serializer_class = ContactSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name']
    def get_queryset(self):
        return Contact.objects.all()

class DealViewSet(viewsets.ModelViewSet):
    permission_classes = (isOwner , )
    serializer_class = DealSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name', 'state']
    def get_queryset(self):

        if 'created' in self.request.GET and 'won' in self.request.GET and 'lost' in self.request.GET:
            qs1 , qs2 , qs3 = Deal.objects.none(), Deal.objects.none(), Deal.objects.none()
            if self.request.GET['created'] == '1':
                qs1 = Deal.objects.filter(state = 'created')
            if self.request.GET['won'] == '1':
                qs2 = Deal.objects.filter(result = 'won')
            if self.request.GET['lost'] == '1':
                qs2 = Deal.objects.filter(result = 'lost')

            toReturn = qs1 | qs2 | qs3
        else:
            toReturn = Deal.objects.all()

        toReturn = toReturn.filter(active = True)
        if 'company__contains' in self.request.GET:
            comName = self.request.GET['company__contains']
            toReturn = toReturn.filter(company__in = service.objects.filter(name__contains=comName))

        if 'created' in self.request.GET and self.request.GET['created'] == 'false':
            toReturn = toReturn.exclude(state = 'created')
        return toReturn

class ContractViewSet(viewsets.ModelViewSet):
    permission_classes = (isOwner , )
    serializer_class = ContractSerializer
    def get_queryset(self):
        return Contract.objects.all()

class ActivityViewSet(viewsets.ModelViewSet):
    permission_classes = (isOwner , )
    serializer_class = ActivitySerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['contact' , 'deal', 'notes' , 'data']
    def get_queryset(self):
        return Activity.objects.order_by('-created')
