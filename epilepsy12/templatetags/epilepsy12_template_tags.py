from django import template
from django.utils.safestring import mark_safe
from ..general_functions import fetch_concept

register = template.Library()


@register.simple_tag
def percent_complete(registration):
    total = 0
    if registration.audit_progress.first_paediatric_assessment_complete:
        total += 12
    if registration.audit_progress.epilepsy_context_complete:
        total += 6
    if registration.audit_progress.multiaxial_diagnosis_complete:
        total += 6
    if registration.audit_progress.assessment_complete:
        total += 16
    if registration.audit_progress.investigations_complete:
        total += 4
    if registration.audit_progress.management_complete:
        total += 4
    return total


@register.simple_tag
def date_string(date):
    return date.strftime("%d %B %Y")


@register.simple_tag
def characters_left(description):
    length = 2000-len(description)
    colour = 'black'
    if (length < 100):
        colour = 'red'
    safe_text = f'<span style="color:{colour}">{length}</span>'
    return mark_safe(safe_text)


@register.simple_tag
def percentage_of_total(numerator, denominator):
    if numerator and denominator:
        if (int(denominator) > 0):
            return round(int(numerator)/int(denominator)*100)


@register.filter
def custom_filter(text, color):
    safe_text = '<span style="color:{color}">{text}</span>'.format(
        color=color, text=text)
    return mark_safe(safe_text)


@register.simple_tag
def permission_text(add_permission, change_permission, delete_permission, model_name):
    return_string = 'You do not have permission to'
    if add_permission:
        if change_permission and not delete_permission:
            return_string += f' delete {model_name}.'
        elif not change_permission and delete_permission:
            return_string += f' edit {model_name}.'
        elif not change_permission and not delete_permission:
            return_string += f' edit or delete {model_name}.'
        else:
            return_string = ""
    else:
        if change_permission and not delete_permission:
            return_string += f' add or delete {model_name}.'
        elif not change_permission and not delete_permission:
            return_string += f' add, edit or delete {model_name}.'
        elif change_permission and delete_permission:
            return_string += f' add {model_name}.'
        else:
            return_string = ""
    print(return_string)
    return return_string


@register.simple_tag
def matches_model_field(field_name, model):
    if field_name:
        value = getattr(model, field_name)
        if value:
            return True
        else:
            return False


@register.filter
def snomed_concept(concept_id):
    if concept_id is None:
        return
    concept = fetch_concept(concept_id)
    return concept['preferredDescription']['term']


@register.filter
def is_in(url_name, args):
    """
    receives the request.resolver_match.url_name
    and compares with the template name (can be a list in a string separated by commas),
    returning true if a match is present
    """
    if args is None:
        return None
    arg_list = [arg.strip() for arg in args.split(',')]
    if url_name in arg_list:
        return True
    else:
        return False


@register.simple_tag
def match_two_values(val1, val2):
    """
    Matches two values
    """
    return val1 == val2


@register.filter
def to_class_name(value):
    if value.__class__.__name__ == "Registration":
        return 'Verification/Registration'
    elif value.__class__.__name__ == "FirstPaediatricAssessment":
        return 'First Paediatric Assessment'
    elif value.__class__.__name__ == "EpilepsyContext":
        return 'Epilepsy Context'
    elif value.__class__.__name__ == "MultiaxialDiagnosis":
        return 'Multiaxial Diagnosis'
    elif value.__class__.__name__ == "Assessment":
        return 'Milestones'
    elif value.__class__.__name__ == "Investigations":
        return 'Investigations'
    elif value.__class__.__name__ == "Management":
        return 'Management'
    elif value.__class__.__name__ == "Site":
        return 'Site'
    elif value.__class__.__name__ == "Episode":
        return 'Episode'
    elif value.__class__.__name__ == "Syndrome":
        return 'Syndrome'
    elif value.__class__.__name__ == "Comorbidity":
        return 'Comorbidity'
    elif value.__class__.__name__ == "Epilepsy12User":
        return 'Epilepsy12 User'
    elif value.__class__.__name__ == "Antiepilepsy Medicine":
        return 'Antiepilepsy Medicine'
    else:
        return 'Error'


@register.filter
def return_case(value):
    if value.__class__.__name__ == "Registration":
        return value.case
    elif value.__class__.__name__ == "FirstPaediatricAssessment":
        return value.registration.case
    elif value.__class__.__name__ == "EpilepsyContext":
        return value.registration.case
    elif value.__class__.__name__ == "MultiaxialDiagnosis":
        return value.registration.case
    elif value.__class__.__name__ == "Assessment":
        return value.registration.case
    elif value.__class__.__name__ == "Investigations":
        return value.registration.case
    elif value.__class__.__name__ == "Management":
        return value.registration.case
    elif value.__class__.__name__ == "Site":
        return value.case
    elif value.__class__.__name__ == "Episode":
        return value.multiaxial_diagnosis.registration.case
    elif value.__class__.__name__ == "Syndrome":
        return value.multiaxial_diagnosis.registration.case
    elif value.__class__.__name__ == "Comorbidity":
        return value.multiaxial_diagnosis.registration.case
    elif value.__class__.__name__ == "Epilepsy12User":
        return 'Epilepsy12 User'
    elif value.__class__.__name__ == "Antiepilepsy Medicine":
        return value.management.registration.case
    else:
        return 'Error'


@register.filter('has_group')
def has_group(user, group_names_string):
    # thanks to Lucas Simon for this efficiency
    # https://stackoverflow.com/questions/1052531/get-user-group-in-a-template
    """
    Check if user has permission
    """
    result = [x.strip() for x in group_names_string.split(',')]
    groups = user.groups.all().values_list('name', flat=True)
    match = False
    for group in groups:
        if group in result:
            match = True
    return match


@register.simple_tag
def none_masked(field):
    if field is None:
        return "##########"
    else:
        return field


@register.simple_tag
def none_percentage(field):
    if field is None:
        return "No data"
    else:
        return f'{field} %'


@register.filter(name='icon_for_score')
def icon_for_score(score):
    if score is None:
        return
    if score < 1:
        return mark_safe(
            """<i 
                    class='rcpch_light_blue exclamation triangle icon'
                    data-title="Not achieved"
                    data-content="This measure has not been achieved for this child."
                    data-position="top right"
                    _="init js $('.rcpch_light_blue.exclamation.triangle.icon').popup(); end"
                ></i>
            """)
    elif score > 1:
        return mark_safe(
            """<i 
                    class='rcpch_light_grey ban icon'
                    data-title="Not applicable"
                    data-content="This measure does not apply to this child."
                    data-position="top right"
                    _="init js $('.rcpch_light_grey.ban.icon').popup(); end"
                ></i>"""
        )
    elif score == 1:
        return mark_safe(
            """<i 
                class='check circle outline rcpch_pink icon'
                data-title="Achieved"
                data-content="This child's care has met the Epilepsy12 standard for this measure."
                data-position="top right"
                _="init js $('.check.circle.outline.rcpch_pink.icon').popup(); end"
                ></i>
                """)
    else:
        return mark_safe(
            """<i 
                class='rcpch dot circle icon'
                data-title="Unscored"
                data-content="This measure has not yet been scored."
                data-position="top right"
                _="init js $('.rcpch.dot.circle.icon').popup(); end"
                ></i>
                """)
