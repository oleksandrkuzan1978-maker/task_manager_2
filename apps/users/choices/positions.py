from django.db import models
from django.utils.translation import gettext_lazy as _

class UserPositions(models.TextChoices):
    CEO = "ceo", _("CEO")
    CTO = "cto", _("CTO")
    DESIGNER = "designer", _("Designer")
    PROGRAMMER = "programmer", _("Programmer")
    PRODUCT_OWNER = "product_owner", _("Product Owner")
    PROJECT_OWNER = "project_owner", _("Project Owner")
    PROJECT_MANAGER = "project_manager", _("Project Manager")
    QA = "qa", _("QA")