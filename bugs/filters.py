from django_filters import rest_framework as filters

from bugs.models import Bug


class BugFilter(filters.FilterSet):
    bug_type = filters.ChoiceFilter(choices=Bug.BugType.choices)
    status_type = filters.ChoiceFilter(choices=Bug.StatusType.choices)

    class Meta:
        model = Bug
        fields = ["bug_type", "status_type"]
