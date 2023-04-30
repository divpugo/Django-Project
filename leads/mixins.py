from django.contrib.auth.mixins import AccessMixin

class LeadRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_lead:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
