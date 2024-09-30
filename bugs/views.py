from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from bugs.filters import BugFilter
from bugs.models import Bug
from bugs.serializers import (
    CreateBugSerializer,
    ListBugsSerializer,
    RetrieveBugSerializer,
)


class CreateListBugsView(ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Bug.objects.all()
    filterset_class = BugFilter

    def get_serializer_class(self) -> CreateBugSerializer | ListBugsSerializer:
        if self.request.method == 'POST':
            return CreateBugSerializer
        return ListBugsSerializer


class RetrieveBugsView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RetrieveBugSerializer
    queryset = Bug.objects.all()
