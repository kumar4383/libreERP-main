from django.contrib.auth.models import User , Group
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import *
from .models import *
from gitweb.serializers import repoLiteSerializer
from ERP.serializers import serviceSerializer
from projects.serializers import projectLiteSerializer

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('created' , 'number' , 'ifsc' , 'bank'  , 'bankAddress' , 'contactPerson' , 'authorizedSignaturies')

class CostCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostCenter
        fields = ('head' , 'name' , 'code' , 'created' , 'account' , 'projects')

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('fromAcc' , 'toAcc' , 'ammount' , 'user' , 'balance')


class InvoiceSerializer(serializers.ModelSerializer):
    service = serviceSerializer(many = False , read_only = True)
    class Meta:
        model = Invoice
        fields = ('user' , 'created' , 'service' , 'amount' , 'currency' , 'dated' , 'attachment' , 'sheet', 'description', 'approved')



class ExpenseSheetSerializer(serializers.ModelSerializer):
    invoices = InvoiceSerializer(many = True , read_only = True)
    project = projectLiteSerializer(many = False , read_only = True)
    class Meta:
        model = ExpenseSheet
        fields = ('pk','user' , 'created' , 'approved' , 'approvalMatrix' , 'approvalStage' , 'dispensed' , 'notes' , 'project' , 'transaction', 'invoices')