import re
from rest_framework import serializers
from .models import LabTestProfile, LabRequest, LabResult


class LabTestProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=LabTestProfile
        fields= '__all__'

class LabResultSerializer(serializers.ModelSerializer):
    class Meta:
        model=LabResult
        fields=['id', 'request', 'lab_tech', 'result_value', 'is_abnormal', 'technician_remarks', 'completed_at']
        read_only_fields=['lab_tech', 'completed_at', 'is_abnormal']

    
    def validate(self, data):
        request_obj=data.get('request')
        result_val=data.get('result_value')

        normal_range=request_obj.test_type.normal_range
        numbers=re.findall(r"[-+]?\d*\.\d+|\d+", normal_range)
        if len(numbers)==2:
            try:
                low=float(numbers[0])
                high=float(numbers[1])
                val=float(result_val)

            except ValueError:
                pass
        return data
    

class LabRequestSerializer(serializers.ModelSerializer):
    result=LabResultSerializer(read_only=True)
    test_name=serializers.CharField(source='test_type.name', read_only=True)

    class Meta:
        model=LabRequest
        fields=['id', 'patient', 'doctor', 'test_type', 'test_name', 'requested_at', 'status', 'clinical_note', 'result']


