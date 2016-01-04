from django.contrib.auth.models import User , Group
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import *
from .models import *
from PIM.serializers import *

class userSearchSerializer(serializers.ModelSerializer):
    # to be used in the typehead tag search input, only a small set of fields is responded to reduce the bandwidth requirements
    class Meta:
        model = User
        fields = ( 'pk', 'username' , 'first_name' , 'last_name' )

class moduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = module
        fields = ( 'pk', 'name' , 'discription' )

class applicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = application
        fields = ( 'pk', 'name', 'module' , 'discription')

class applicationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = appSettingField
        fields = ( 'pk', 'name', 'flag' , 'value')

class applicationSettingsAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = appSettingField
        fields = ( 'pk', 'name', 'flag' , 'value' , 'discription' , 'app' , 'security' , 'created')

class applicationAdminSerializer(serializers.ModelSerializer):
    module = moduleSerializer(read_only = True , many = False)
    owners = userSearchSerializer(read_only = True , many = True)
    class Meta:
        model = application
        fields = ( 'pk', 'name', 'module' , 'owners' , 'discription' , 'created')
    def update (self, instance, validated_data):
        for pk in self.context['request'].data['owners']:
            instance.owners.add(User.objects.get(pk = pk))
        instance.save()
        return instance

class rankSerializer(serializers.ModelSerializer):
    class Meta:
        model = rank
        fields = ( 'title' , 'category' )

class permissionSerializer(serializers.ModelSerializer):
    app = applicationSerializer(read_only = True, many = False)
    class Meta:
        model = permission
        fields = ( 'pk' , 'app' , 'user' )
    def create(self , validated_data):
        user = self.context['request'].user
        app =application.objects.get(pk = self.context['request'].data['app'])
        if not user.is_superuser and user not in app.owners.all():
            raise PermissionDenied(detail=None)
        perm , created = permission.objects.get_or_create(app =  app, user = validated_data['user'] , givenBy = user)
        return perm

class groupPermissionSerializer(serializers.ModelSerializer):
    app = applicationSerializer(read_only = True, many = False)
    class Meta:
        model = groupPermission
        fields = ( 'pk' , 'app' , 'group' )

class userDesignationSerializer(serializers.ModelSerializer):
    rank = moduleSerializer(read_only = True, many = False)
    class Meta:
        model = designation
        fields = ('url' , 'unitType' , 'domain' , 'rank' , 'unit' , 'department' , 'reportingTo' , 'primaryApprover' , 'secondaryApprover')
class userProfileSerializer(serializers.ModelSerializer):
    """ allow all the user """
    class Meta:
        model = profile
        fields = ( 'url' , 'mobile' , 'displayPicture' , 'website' , 'prefix' , 'almaMater', 'pgUniversity' , 'docUniversity' )
        read_only_fields = ('website' , 'prefix' , 'almaMater', 'pgUniversity' , 'docUniversity' , )

class userProfileAdminModeSerializer(serializers.HyperlinkedModelSerializer):
    """ Only admin """
    class Meta:
        model = profile
        fields = ( 'url', 'empID', 'dateOfBirth' , 'anivarsary' , 'permanentAddressStreet' , 'permanentAddressCity' , 'permanentAddressPin', 'permanentAddressState' , 'permanentAddressCountry',
        'localAddressStreet' , 'localAddressCity' , 'localAddressPin' , 'localAddressState' , 'localAddressCountry' , 'prefix', 'gender' , 'email', 'email2', 'mobile' , 'emergency' , 'tele' , 'website',
        'sign', 'IDPhoto' , 'TNCandBond' , 'resume' ,  'certificates', 'transcripts' , 'otherDocs' , 'almaMater' , 'pgUniversity' , 'docUniversity' , 'fathersName' , 'mothersName' , 'wifesName' , 'childCSV',
        'note1' , 'note2' , 'note3')



class userSerializer(serializers.HyperlinkedModelSerializer):
    profile = userProfileSerializer(many=False , read_only=True)
    class Meta:
        model = User
        fields = ('url' , 'username' , 'email' , 'first_name' , 'last_name' , 'designation' ,'profile'  ,'settings' , 'password' , 'social')
        read_only_fields = ('designation' , 'profile' , 'settings' ,'social' )
        extra_kwargs = {'password': {'write_only': True} }
    def create(self , validated_data):
        raise PermissionDenied(detail=None)
    def update (self, instance, validated_data):
        user = self.context['request'].user
        if authenticate(username = user.username , password = self.context['request'].data['oldPassword']) is not None:
            user = User.objects.get(username = user.username)
            user.set_password(validated_data['password'])
            user.save()
        else :
            raise PermissionDenied(detail=None)
        return user

class userAdminSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url' , 'username' , 'email' , 'first_name' , 'last_name' , 'is_staff' ,'is_active' )
    def create(self , validated_data):
        if not self.context['request'].user.is_superuser:
            raise PermissionDenied(detail=None)
        user = User.objects.create(**validated_data)
        user.email = user.username + '@cioc.com'
        password =  self.context['request'].data['password']
        user.set_password(password)
        user.save()
        return user
    def update (self, instance, validated_data):
        user = self.context['request'].user
        if user.is_staff or user.is_superuser:
            u = User.objects.get(username = self.context['request'].data['username'])
            if (u.is_staff and user.is_superuser ) or user.is_superuser: # superuser can change password for everyone , staff can change for everyone but not fellow staffs
                if 'password' in self.context['request'].data:
                    u.set_password(self.context['request'].data['password'])
                u.first_name = validated_data['first_name']
                u.last_name = validated_data['last_name']
                u.is_active = validated_data['is_active']
                u.is_staff = validated_data['is_staff']
                u.save()
            else:
                raise PermissionDenied(detail=None)
        try:
            return u
        except:
            raise PermissionDenied(detail=None)

class groupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url' , 'name')
