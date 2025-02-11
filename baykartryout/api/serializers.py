from rest_framework.serializers import ModelSerializer
from baykartryout.models import Part, Assembly

class PartSerializer(ModelSerializer):
    class Meta:
        model = Part
        fields = '__all__'

class AssemblySerializer(ModelSerializer):
    class Meta:
        model = Assembly
        fields = '__all__'