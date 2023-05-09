from django.http import HttpRequest
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Tag
from .serializers import ProductSerializer, TagSerializer
from rest_framework.views import APIView
from http import HTTPStatus

#displays all the products in the db on the template view
def index(request):
    products = Product.objects.all()
    return render(request, "products/index.html", {"products": products})

#class ProductList(APIView):

@api_view(['GET', 'POST'])
def get_products_and_create_product(request, format=None):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=HTTPStatus.OK)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            tags = serializer.validated_data.get('tags', [])     
            serializer.save()

            for tag in tags:
                #print(tag.id)
                # Create a new Django HttpRequest instance using DRF's Request
                django_request = HttpRequest()
                django_request.method = 'GET'
                django_request.user = request.user
                # Pass the new HttpRequest instance to get_tag view
                response = get_tag(django_request, pk=tag.id)
                #print(response.data)

                #tag_id = tag.id
                #response = get_tag(request, pk=tag_id)
                tag_data = response.data
                # update the tag field of serializer.data with tag_data
                serializer.data['tags'].append(tag_data)

          

            return Response(serializer.data, status=HTTPStatus.CREATED)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
    
#class ProductDetail(APIView):    

@api_view(['GET', 'PUT', 'DELETE'])
def product_by_id(request, pk, format=None):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response({"error": "Product does not exist."}, status=HTTPStatus.NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ProductSerializer(instance=product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.OK)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
    
    elif request.method == 'PATCH':
        serializer = ProductSerializer(instance=product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.OK)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(f"Product {pk} deleted successfully", status=HTTPStatus.NO_CONTENT)


# Tag views
@api_view(['GET', 'POST'])
def get_tags_and_create_tag(request, format=None):
    if request.method == 'GET':
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=HTTPStatus.OK)
    
    elif request.method == 'POST':
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.CREATED)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def tag_by_id(request, pk, format=None):
#     try:
#         tag = Tag.objects.get(id=pk)
#     except Tag.DoesNotExist:
#         return Response({"error": "Tag does not exist."}, status=HTTPStatus.NOT_FOUND)

#     if request.method == 'GET':
#         serializer = TagSerializer(tag)
#         return Response(serializer.data)
    
#     elif request.method == 'PUT':
#         serializer = TagSerializer(instance=tag, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=HTTPStatus.OK)
#         return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
    
#     elif request.method == 'DELETE':
#         tag.delete()
#         return Response("Tag deleted successfully", status=HTTPStatus.NO_CONTENT)

@api_view(['GET'])
def get_tag(request, pk):
    tag = Tag.objects.get(id=pk)
    serializer = TagSerializer(tag, many=False)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
def update_tag(request, pk):
    tag = Tag.objects.get(id=pk) 
    serializer = TagSerializer(instance=tag, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def delete_tag(request, pk):
    tag = Tag.objects.get(id=pk)
    tag.delete()

    return Response("Tag deleted successfully")