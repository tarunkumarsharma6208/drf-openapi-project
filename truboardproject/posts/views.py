from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
import requests
from .serializers import PostSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from datetime import datetime


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination

    @extend_schema(
        description="Get paginated list of filtered posts from JSONPlaceholder",
        responses=PostSerializer(many=True),
        parameters=[
            OpenApiParameter(
                name='page',
                type=int,
                required=False,
                location=OpenApiParameter.QUERY,
                description='Page number for pagination.'
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        response = requests.get('https://jsonplaceholder.typicode.com/posts')
        data = response.json()

        # Filtering out the desired fields
        filtered_data = []
        for item in data:
            filtered_item = {
                "title": item["title"],
                "userId": item["userId"],
                "body": item["body"]
            }
            filtered_data.append(filtered_item)

        paginator = self.pagination_class()
        paginated_data = paginator.paginate_queryset(filtered_data, request)

        serializer = self.serializer_class(paginated_data, many=True)

        # Create the paginated response structure
        paginated_response = {
            "count": paginator.page.paginator.count,
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "results": serializer.data
        }

        # Create the standardized response
        standardized_response = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
            "path": request.path,
            "method": request.method,
            "result": paginated_response
        }

        return Response(standardized_response)