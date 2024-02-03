from rest_framework.decorators import api_view
from rest_framework.response import Response
import pymongo
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404

class IndexView(APIView):
    def get(self, request):
        return Response({"message": "API Index"}, status=status.HTTP_200_OK)

# Connect to MongoDB
url = 'mongodb://localhost:27017'
client = pymongo.MongoClient(url)
db = client['FormGenerator']  # Replace 'your_database_name' with the actual name of your MongoDB database

# Endpoint to retrieve forms from the forms collection
from django.http import Http404

@api_view(['GET'])
def get_forms(request, form_id):
    # Assuming 'forms' is the collection for form information
    forms_collection = db['forms']

    # Convert the form_id to ObjectId if needed (assuming you're using MongoDB ObjectId)
    from bson import ObjectId
    form_id_object = ObjectId(form_id)

    # Retrieve the specified form from the collection based on form_id
    form = forms_collection.find_one({'_id': form_id_object})

    # Check if the form with the given ID exists
    if not form:
        raise Http404("Form does not exist")

    # Format the form data as needed
    formatted_form = {
        'form_id': str(form['_id']),
        'form_title': form['form_title'],
        'questions': form['components'],
        # Add more form details as needed
    }

    return Response(formatted_form)



# Endpoint to retrieve responses from the responses collection
@api_view(['GET'])
def get_responses(request, form_id):
    # Assuming 'responses' is the collection for responses
    responses_collection = db['responses']

    try:
        # Convert the form_id to ObjectId if needed (assuming you're using MongoDB ObjectId)
        from bson import ObjectId
        form_id_object = ObjectId(form_id)
    except Exception as e:
        raise Http404("Invalid form ID")

    # Retrieve responses for the specified form ID
    responses = list(responses_collection.find({'form_id': form_id_object}))

    # Check if there are no responses found for the given form ID
    if not responses:
        raise Http404("No responses found for the specified form ID")

    # Format the responses data as needed
    formatted_responses = [
        {
            'response_id': str(response['_id']),
            'form_id': response['form_id'],
            'responses': response['responses'],
            # Add more response details as needed
        }
        for response in responses
    ]

    return Response(formatted_responses)

    return Response(formatted_responses)
