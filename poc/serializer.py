from rest_framework import serializers
from poc.models import FeatureRequest, Client, ProductArea

class ProductAreaSerializer(serializers.ModelSerializer):
	#Serialization class for Product Area model
	class Meta:
		model = ProductArea
		fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
	#Serialization class for Client model
	class Meta:
		model = Client
		fields = '__all__'

class FeatureRequestSerializer(serializers.ModelSerializer):
	#Serialization class for Feature request Model
	product_area = ProductAreaSerializer()
	client = ClientSerializer()

	class Meta:
		model = FeatureRequest
		fields = ('id','title','desc','target_date','create_date','product_area','client','priority','status')

			