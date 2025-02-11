from rest_framework.decorators import api_view
from rest_framework.response import Response
from baykartryout.models import Part, Assembly
from .serializers import PartSerializer, AssemblySerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/parts'
        'GET /api/assemblies'
    ]
    return Response(routes)

@api_view(['GET'])
def getParts(request):
    parts = Part.objects.all()
    serializer = PartSerializer(parts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getAssemblies(request):
    assemblies = Assembly.objects.all()
    serializer = AssemblySerializer(assemblies, many=True)
    return Response(serializer.data)