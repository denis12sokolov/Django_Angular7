from rest_framework import mixins, status
from rest_framework.response import Response


class BulkCreateModelMixin(mixins.CreateModelMixin):
    """
    Create valid objects and return errors for invalid ones.
    """

    def create(self, request, *args, **kwargs):
        # The initial serializer
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid()
        return_data = []

        if serializer.errors:
            for errors, data in zip(serializer.errors, serializer.initial_data):
                # If item doesn't have errors
                if not errors:
                    # Create a an individual serializer for the valid object and save it
                    object_serializer = self.get_serializer(data=data)
                    if object_serializer.is_valid():
                        object_serializer.save()
                else:
                    return_data.append(errors)
            return_status = status.HTTP_206_PARTIAL_CONTENT
        else:
            serializer.save()
            return_data = {"success": True}
            return_status = status.HTTP_201_CREATED

        return Response(return_data, status=return_status)
