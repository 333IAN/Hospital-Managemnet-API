from rest_framework import serializers
from .models import Appointment, Vitals, Consultation, Prescription, PrescriptionItem, LabRequest

class VitalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vitals
        fields = '__all__'

class PrescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionItem
        fields = '__all__'

class PrescriptionSerializer(serializers.ModelSerializer):
    items = PrescriptionItemSerializer(many=True, read_only=True)

    class Meta:
        model = Prescription
        fields = '__all__'

class LabRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabRequest
        fields = '__all__'

class ConsultationSerializer(serializers.ModelSerializer):
    prescription = PrescriptionSerializer(read_only=True)
    lab_requests = LabRequestSerializer(many=True, read_only=True)

    class Meta:
        model = Consultation
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    vitals = VitalsSerializer(read_only=True)
    consultation = ConsultationSerializer(read_only=True)

    patient_name=serializers.CharField(source='patient', read_only=True)
    doctor_name=serializers.CharField(source='doctor', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id','patient', 'patient_name', 'doctor', 'doctor_name', 'appointment_date', 'reason', 'status', 'vitals', 'consultation']
        