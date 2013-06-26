from lispy.dialects.norvig.special_forms import SPECIAL_FORMS as NORVIG_FORMS
from lispy.dialects.pybuiltins.special_forms import SPECIAL_FORMS as PYBUILTIN_FORMS

SPECIAL_FORMS = NORVIG_FORMS
SPECIAL_FORMS.update(PYBUILTIN_FORMS)
