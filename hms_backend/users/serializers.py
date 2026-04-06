from rest_framework import serializers
from .models import User, PatientProfile, DoctorProfile, NurseProfile, PharmacistProfile, LabTechProfile, RadiologistProfile, ReceptionistProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token=super().get_token(user)

        token['role']=user.role
        token['email']=user.email
        token['full_name']=f"{user.first_name} {user.last_name}"

        return token

class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = '__all__'

class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = '__all__'
    
class NurseProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= NurseProfile
        fields='__all__'
    
class PharmacistProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= PharmacistProfile
        fields='__all__'

class LabTechProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= LabTechProfile
        fields='__all__'

class RadiologistProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= RadiologistProfile
        fields='__all__'

class ReceptionistProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= ReceptionistProfile
        fields='__all__'

class UserSerializer(serializers.ModelSerializer):
    profile=serializers.SerializerMethodField()
    
    class Meta:
        model=User
        fields=['id', 'email', 'first_name', 'last_name', 'role', 'profile', 'password']
        extra_kwargs={'password': {'write_only': True}}


    def get_profile(self, obj):
        role_serializer_map={
            'PATIENT': (PatientProfileSerializer, 'patientprofile'),
            'DOCTOR': (DoctorProfileSerializer, 'doctorprofile'),
            'NURSE': (NurseProfileSerializer, 'nurseprofile'),
            'PHARMACIST': (PharmacistProfileSerializer, 'pharmacistprofile'),
            'LAB_TECH': (LabTechProfileSerializer, 'labtechprofile'),
            'RADIOLOGIST': (RadiologistProfileSerializer, 'radiologistprofile'),
            'RECEPTIONIST': (ReceptionistProfileSerializer, 'receptionistprofile'),
        }

        if obj.role in role_serializer_map:
            serializer_class,attr=role_serializer_map[obj.role]
            profile_instance=getattr(obj,attr, None)
            if profile_instance:
                return serializer_class(profile_instance, context=self.context).data
        return None
    
    def create(self, validated_data):
        user=User.objects.create_user(**validated_data)
        return user
    