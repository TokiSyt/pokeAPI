from __future__ import annotations

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Model, Q
from django.shortcuts import render
from django.views.generic import TemplateView

from apps.core.import_service import import_for_model


class PokeDetailView(LoginRequiredMixin, TemplateView):
    """
    Generic detail view for any PokeAPI-backed resource.

    Subclass and set class attributes. Override needs_reimport()
    and/or build_context() for custom behavior.
    """

    model: type[Model] | None = None
    context_key: str = ""
    name_field: str = "name"
    id_field: str | None = None
    url_kwarg: str = "name_or_id"
    check_user: bool = True
    error_noun: str = ""

    def get_error_noun(self):
        return self.error_noun or self.model.__name__

    def needs_reimport(self, obj, request):
        if not self.check_user:
            return False
        if not hasattr(obj, "allowed_users"):
            return False
        return not obj.allowed_users.filter(id=request.user.id).exists()

    def build_context(self, obj, request):
        return {self.context_key: obj}

    def _lookup(self, name_or_id):
        try:
            if name_or_id.isdigit() and self.id_field:
                return self.model.objects.get(Q(**{self.id_field: name_or_id}))
            return self.model.objects.get(Q(**{self.name_field: name_or_id}))
        except self.model.DoesNotExist:
            return None

    def get(self, request, **kwargs):
        name_or_id = kwargs[self.url_kwarg]
        obj = self._lookup(name_or_id)

        if obj is None or self.needs_reimport(obj, request):
            obj = import_for_model(self.model, name_or_id, request.user)

        if obj is None:
            noun = self.get_error_noun()
            return render(
                request,
                self.template_name,
                {"error": f'Could not fetch {noun} "{name_or_id}"'},
                status=404,
            )

        return render(request, self.template_name, self.build_context(obj, request))


# TODO: once all DetailViews are migrated, add PokeSearchView base class here.
# All *SearchViews share the same pattern: form_class, context_key, model, and a
# get_context_data that adds the form + filters objects by allowed_users=request.user.
