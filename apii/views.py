from rest_framework.decorators import api_view
from rest_framework.response import Response
import pymongo
from django.http import Http404
from bson import ObjectId
    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from base.models import Form
from .serializers import FormSerializer


url = 'mongodb://localhost:27017'
client = pymongo.MongoClient(url)
db = client['FormGenerator']  # Replace 'your_database_name' with the actual name of your MongoDB database

@api_view(['GET'])
def get_all_forms(request):
    try:
        # Assuming 'forms' is the collection for form information
        forms_collection = db['forms']

        # Retrieve all forms
        forms = list(forms_collection.find())

        # Format the forms data as needed
        formatted_forms = [
            {
                #'form_id': str(form['_id']),
                'form_id': str(ObjectId(str(form['_id']))),
                'form_title': form['form_title'],
                'questions': form['components'],
                # Add more form details as needed
            }
            for form in forms
        ]

        return Response(formatted_forms)

    except Exception as e:
        # Handle the exception, log it, and return an error response
        print(f"An error occurred: {e}")
        return Response({'error': 'An error occurred while retrieving forms'}, status=500)

'''
@api_view(['GET', 'PUT'])
def form_detail(request, form_id):
    try:
        form = Form.objects.get(id=form_id)

        if request.method == 'GET':
            serializer = FormSerializer(form)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = FormSerializer(form, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Form updated successfully'})
            return Response(serializer.errors, status=400)

    except Form.DoesNotExist:
        return Response({'error': 'Form not found'}, status=404)
'''
@api_view(['GET'])
def get_form(request, form_id):
    try:
        # Assuming 'forms' is the collection for form information
        forms_collection = db['forms']

        # Fetch the form details based on the form ID
        form_document = forms_collection.find_one({'_id': ObjectId(form_id)})

        if not form_document:
            return JsonResponse({'message': 'Form not found'}, status=404)

        return JsonResponse({
            'form_title': form_document['form_title'],
            'components': form_document['components'],
        })
    except Exception as e:
        return JsonResponse({'message': f'Error fetching form: {str(e)}'}, status=500)

@api_view(['POST'])
def edit_form(request, form_id):
    try:
        form_data = request.data
        form_title = form_data.get('formTitle')
        components = form_data.get('components')

        # Assuming 'forms' is the collection for form information
        forms_collection = db['forms']

        # Update the existing document in the forms collection for the edited form
        forms_collection.update_one(
            {'_id': ObjectId(form_id)},
            {'$set': {
                'form_title': form_title,
                'components': components if components else [],
            }}
        )

        return JsonResponse({'message': f'Form {form_title} edited successfully with ID: {form_id}'})
    except Exception as e:
        return JsonResponse({'message': f'Error editing form: {str(e)}'},status=500)
