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

        # Retrieve the specific form by ID
        form = forms_collection.find_one({'_id': ObjectId(form_id)})

        if form:
            # Format the form data as needed
            formatted_form = {
                'form_id': str(ObjectId(str(form['_id']))),
                'form_title': form['form_title'],
                'questions': form['components'],
                # Add more form details as needed
            }

            return Response(formatted_form)
        else:
            return Response({'error': 'Form not found'}, status=404)

    except pymongo.errors.OperationFailure as e:
        # Handle the case where the provided form_id is not a valid ObjectId
        print(f"Invalid form_id: {form_id}")
        return Response({'error': 'Invalid form_id'}, status=400)

    except Exception as e:
        # Handle other exceptions, log them, and return an error response
        print(f"An error occurred: {e}")
        return Response({'error': 'An error occurred while retrieving the form'}, status=500)

    
@api_view(['PUT'])
def edit_form(request, form_id):
    try:
        # Assuming 'forms' is the collection for form information
        forms_collection = db['forms']

        # Retrieve the specific form by ID
        form = forms_collection.find_one({'_id': ObjectId(form_id)})

        if not form:
            return Response({'error': 'Form not found'}, status=404)

        # Extract form data from the request
        form_data = request.data

        # Update form fields based on the request data
        if 'form_title' in form_data:
            form['form_title'] = form_data['form_title']

        if 'questions' in form_data:
            form['components'] = form_data['questions']

        # Use update_one with $set to update specific fields
        forms_collection.update_one(
            {'_id': ObjectId(form_id)},
            {'$set': {'form_title': form_data.get('form_title', form['form_title']),
                      'components': form_data.get('questions', form['components'])}
            }
        )

        return Response({'message': 'Form updated successfully'})

    except Exception as e:
        # Handle the exception, log it, and return an error response
        print(f"An error occurred: {e}")
        return Response({'error': 'An error occurred while updating the form'}, status=500)
