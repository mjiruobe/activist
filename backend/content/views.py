# mypy: disable-error-code="override"
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from backend.paginator import CustomPagination

from .models import Resource, ResourceTopic, Task, Topic, TopicFormat
from .serializers import (
    ResourceSerializer,
    ResourceTopicSerializer,
    TaskSerializer,
    TopicFormatSerializer,
    TopicSerializer,
)


class ResourceViewSet(viewsets.ModelViewSet[Resource]):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    pagination_class = CustomPagination
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request: Request) -> Response:
        if request.user.is_authenticated:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {"error": "You are not allowed to create a resource."},
            status=status.HTTP_403_FORBIDDEN,
        )

    def retrieve(self, request: Request, pk: str | None = None) -> Response:
        if request.user.is_authenticated:
            query = self.queryset.filter(
                Q(private=False) | Q(private=True, created_by=request.user), id=pk
            )
        else:
            query = self.queryset.filter(Q(private=False), id=pk)

        serializer = self.get_serializer(query)
        return Response(serializer.data)

    def list(self, request: Request) -> Response:
        if request.user.is_authenticated:
            query = self.queryset.filter(
                Q(private=False) | Q(private=True, created_by=request.user)
            )
        else:
            query = self.queryset.filter(private=False)

        serializer = self.get_serializer(query, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))

    def update(self, request: Request, pk: str | None = None) -> Response:
        item = self.get_object()
        if not item.created_by == request.user:
            return Response(
                {"error": "You are not allowed to update this resource."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.get_serializer(item, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request: Request, pk: str | None = None) -> Response:
        item = self.get_object()
        if not item.created_by == request.user:
            return Response(
                {"error": "You are not allowed to update this resource."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.get_serializer(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request: Request, pk: str | None = None) -> Response:
        item = self.get_object()
        if not item.created_by == request.user:
            return Response(
                {"error": "You are not allowed to delete this resource."},
                status=status.HTTP_403_FORBIDDEN,
            )

        self.perform_destroy(item)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskViewSet(viewsets.ModelViewSet[Task]):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = CustomPagination


class TopicViewSet(viewsets.ModelViewSet[Topic]):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    pagination_class = CustomPagination


class ResourceTopicViewSet(viewsets.ModelViewSet[ResourceTopic]):
    queryset = ResourceTopic.objects.all()
    serializer_class = ResourceTopicSerializer
    pagination_class = CustomPagination


class TopicFormatViewSet(viewsets.ModelViewSet[TopicFormat]):
    queryset = TopicFormat.objects.all()
    serializer_class = TopicFormatSerializer
    pagination_class = CustomPagination
