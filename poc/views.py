from poc.models import FeatureRequest, ProductArea, Client
from poc.serializer import FeatureRequestSerializer, ProductAreaSerializer, ClientSerializer
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views import View
from django.db import IntegrityError, transaction
from django.db.models import F
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response

import logging
logger = logging.getLogger('django')

class FeatureList(APIView):
    #View to list all features available.
	
	def get(self, request):
        #GET method to return a list of all the features.
		try:
			logger.info('Feature List Request Received!')
			
			clients = Client.objects.all()
			client_serializer = ClientSerializer(clients, many=True)
			client_serializer_data = client_serializer.data
			
			products = ProductArea.objects.all()
			product_serializer = ProductAreaSerializer(products, many=True)
			product_serializer_data = product_serializer.data
			
			features = FeatureRequest.objects.all()
			feature_serializer = FeatureRequestSerializer(features, many=True)
			feature_serializer_data = format_feature_data(feature_serializer.data)
			
			context = {'feature_request': feature_serializer_data,
						'clients':client_serializer_data, 
						'products':product_serializer_data
						}
			return Response(context)
			
		except Exception as e:
			content = {'Error': 'Error in returning feature list'}
			logger.error("Error while fetching FeatureList data ", repr(e))
			return Response(content, status=500)

class AddRequest(APIView):
	#Add feature details to database
	
	def post(self, request):
		#POST method to save feature details in database
		#It will throw exception if error is found at any level.
		logger.info("Feature Add Request Received!")
		client_id = request.data['client_id']
		product_id = request.data['product_id']
		title = request.data['title'].strip()
		desc = request.data['desc'].strip()
		target_date = request.data['target_date']
		priority = request.data['priority']
		
		try:
			with transaction.atomic():
			
				#If same priority is set for the same client, 
				#then reorder all other feature requests for this client
				previous_priority = FeatureRequest.objects.filter(client__id=client_id).filter(priority__gte=priority)
				if previous_priority.count() > 0:
					 previous_priority.update(priority=F('priority')+1)
					 
				try:
					client = Client.objects.get(pk=client_id)
				except Exception as e:
					logger.error("Error in fetching client details", repr(e))
					content = {'Error_Add': "Error in fetching Client details"}
					return Response(content, status=500)
				try:
					product = ProductArea.objects.get(pk=product_id)
				except Exception as e:
					logger.error("Error in fetching product details", repr(e))
					content = {'Error_Add': "Error in fetching Product details"}
					return Response(content, status=500)
					
				#Save feature data into database
				try:
					feature = FeatureRequest.objects.create(title=title, 
										desc=desc, 
										target_date = target_date, 
										priority=priority, 
										client=client, 
										product_area=product)
					feature_serializer = FeatureRequestSerializer(feature)
					feature_serializer_data = format_feature_data([feature_serializer.data])
					return Response(feature_serializer_data)
					
				except Exception as e:
					logger.error("Error in adding feature details", repr(e))
					content = {'Error_Add': "Error in adding feature details"}
					return Response(content, status=500)
					
		except IntegrityError as e:
			logger.error("Error in saving feature details", repr(e))
			content = {'Error_Add': "Error in saving feature details"}
			return Response(content, status=400)

class FeatureHome(APIView):
	def get(self, request):
		return render_to_response('features.html')
		
def format_feature_data(feature_data):
	final_data = []
	for feature in feature_data:
		feature = dict(feature)
		feature_json = {
							'title': feature['title'],
							'desc': feature['desc'],
							'client': feature['client']['client'],
							'priority': feature['priority'],
							'target_date': feature['target_date'],
							'product_area': feature['product_area']['product'],
							'status':  FeatureRequest.STATUS_CHOICES[int(feature['status'])][1]
						}
		final_data.append(feature_json)
	return final_data
		