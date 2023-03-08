# Python/Django imports
from datetime import date
from dateutil.relativedelta import relativedelta
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Sum, Count, Q
# third party libraries
from django_htmx.http import HttpResponseClientRedirect

# E12 imports
from epilepsy12.constants import ETHNICITIES, INDIVIDUAL_KPI_MEASURES, SEX_TYPE, INTEGRATED_CARE_BOARDS_LOCAL_AUTHORITIES
from epilepsy12.models import Case, FirstPaediatricAssessment, Assessment, Case, FirstPaediatricAssessment, Assessment, Site, EpilepsyContext, MultiaxialDiagnosis, Syndrome, Investigations, Management, Comorbidity, Registration, Episode, HospitalTrust, KPI
from ..common_view_functions import trigger_client_event, annotate_kpis, cases_aggregated_by_sex, cases_aggregated_by_ethnicity, cases_aggregated_by_deprivation_score, all_registered_and_complete_cases_for_hospital, all_registered_and_complete_cases_for_hospital_trust, all_registered_only_cases_for_hospital, all_registered_only_cases_for_hospital_trust
from ..general_functions import get_current_cohort_data, value_from_key


@login_required
def hospital_reports(request):

    # Audit trail - filter all models and sort in order of updated_at, returning the latest 5 updates
    first_paediatric_assessment = FirstPaediatricAssessment.objects.filter()
    site = Site.objects.filter()
    epilepsy_context = EpilepsyContext.objects.filter()
    multiaxial_diagnosis = MultiaxialDiagnosis.objects.filter()
    episode = Episode.objects.filter()
    syndrome = Syndrome.objects.filter()
    comorbidity = Comorbidity.objects.filter()
    assessment = Assessment.objects.filter()
    investigations = Investigations.objects.filter()
    management = Management.objects.filter()
    registration = Registration.objects.filter()

    all_models = sorted(
        chain(registration, first_paediatric_assessment, site, epilepsy_context, multiaxial_diagnosis,
              episode, syndrome, comorbidity, assessment, investigations, management),
        key=lambda x: x.updated_at, reverse=True)[:5]

    template_name = 'epilepsy12/hospital.html'

    cohort_data = get_current_cohort_data()

    if request.user.hospital_employer is not None:
        # current user is affiliated with an existing hospital - set viewable trust to this
        selected_hospital = HospitalTrust.objects.get(
            OrganisationName=request.user.hospital_employer)
    else:
        # current user is a member of the RCPCH audit team and also not affiliated with a hospital
        # therefore set selected hospital to first of hospital on the list
        selected_hospital = HospitalTrust.objects.filter(
            Sector="NHS Sector"
        ).order_by('OrganisationName').first()

    # query to return all completed E12 cases in the current cohort in this hospital
    count_of_current_cohort_registered_completed_cases_in_this_hospital = all_registered_and_complete_cases_for_hospital(
        hospital_instance=selected_hospital).count()
    # query to return all completed E12 cases in the current cohort in this hospital trust
    count_of_current_cohort_registered_completed_cases_in_this_hospital_trust = all_registered_and_complete_cases_for_hospital_trust(
        hospital_instance=selected_hospital).count()
    # query to return all cases registered in the current cohort at this hospital
    count_of_current_cohort_registered_cases_in_this_hospital = all_registered_only_cases_for_hospital(
        hospital_instance=selected_hospital).count()
    # query to return all cases registered in the current cohort at this hospital trust
    count_of_current_cohort_registered_cases_in_this_hospital_trust = all_registered_only_cases_for_hospital_trust(
        hospital_instance=selected_hospital).count()

    if count_of_current_cohort_registered_completed_cases_in_this_hospital > 0:
        total_percent_hospital = round((count_of_current_cohort_registered_cases_in_this_hospital /
                                       count_of_current_cohort_registered_completed_cases_in_this_hospital) * 100)
    else:
        total_percent_hospital = 0

    if count_of_current_cohort_registered_completed_cases_in_this_hospital_trust > 0:
        total_percent_trust = round((count_of_current_cohort_registered_cases_in_this_hospital_trust /
                                    count_of_current_cohort_registered_completed_cases_in_this_hospital_trust) * 100)
    else:
        total_percent_trust = 0

    return render(request=request, template_name=template_name, context={
        'user': request.user,
        'selected_hospital': selected_hospital,
        'hospital_list': HospitalTrust.objects.filter(Sector="NHS Sector").order_by('OrganisationName').all(),
        'cases_aggregated_by_ethnicity': cases_aggregated_by_ethnicity(selected_hospital=selected_hospital),
        'cases_aggregated_by_sex': cases_aggregated_by_sex(selected_hospital=selected_hospital),
        'cases_aggregated_by_deprivation': cases_aggregated_by_deprivation_score(selected_hospital=selected_hospital),
        'percent_completed_hospital': total_percent_hospital,
        'percent_completed_trust': total_percent_trust,
        'count_of_current_cohort_registered_cases_in_this_hospital': count_of_current_cohort_registered_cases_in_this_hospital,
        'count_of_current_cohort_registered_completed_cases_in_this_hospital': count_of_current_cohort_registered_completed_cases_in_this_hospital,
        'count_of_current_cohort_registered_cases_in_this_hospital_trust': count_of_current_cohort_registered_cases_in_this_hospital_trust,
        'count_of_current_cohort_registered_completed_cases_in_this_hospital_trust': count_of_current_cohort_registered_completed_cases_in_this_hospital_trust,
        'cohort_data': cohort_data,
        'all_models': all_models,
        'model_list': ('allregisteredcases', 'registration', 'firstpaediatricassessment', 'epilepsycontext', 'multiaxialdiagnosis', 'assessment', 'investigations', 'management', 'site', 'case', 'epilepsy12user', 'hospitaltrust', 'comorbidity', 'episode', 'syndrome', 'keyword'),
        'individual_kpi_choices': INDIVIDUAL_KPI_MEASURES
    })


@ login_required
def selected_hospital_summary(request):
    """
    POST request from selected_hospital_summary.html on hospital select
    """

    selected_hospital = HospitalTrust.objects.get(
        pk=request.POST.get('selected_hospital_summary'))

    cohort_data = get_current_cohort_data()

    # query to return all completed E12 cases in the current cohort in this hospital
    count_of_current_cohort_registered_completed_cases_in_this_hospital = all_registered_and_complete_cases_for_hospital(
        hospital_instance=selected_hospital).count()
    # query to return all completed E12 cases in the current cohort in this hospital trust
    count_of_current_cohort_registered_completed_cases_in_this_hospital_trust = all_registered_and_complete_cases_for_hospital_trust(
        hospital_instance=selected_hospital).count()
    # query to return all cases registered in the current cohort at this hospital
    count_of_current_cohort_registered_cases_in_this_hospital = all_registered_only_cases_for_hospital(
        hospital_instance=selected_hospital).count()
    # query to return all cases registered in the current cohort at this hospital trust
    count_of_current_cohort_registered_cases_in_this_hospital_trust = all_registered_only_cases_for_hospital_trust(
        hospital_instance=selected_hospital).count()

    if count_of_current_cohort_registered_completed_cases_in_this_hospital > 0:
        total_percent_hospital = round((count_of_current_cohort_registered_cases_in_this_hospital /
                                       count_of_current_cohort_registered_completed_cases_in_this_hospital) * 100)
    else:
        total_percent_hospital = 0

    if count_of_current_cohort_registered_completed_cases_in_this_hospital_trust > 0:
        total_percent_trust = round((count_of_current_cohort_registered_cases_in_this_hospital_trust /
                                    count_of_current_cohort_registered_completed_cases_in_this_hospital_trust) * 100)
    else:
        total_percent_trust = 0

    return render(request=request, template_name='epilepsy12/partials/selected_hospital_summary.html', context={
        'user': request.user,
        'selected_hospital': selected_hospital,
        'hospital_list': HospitalTrust.objects.filter(Sector="NHS Sector").order_by('OrganisationName').all(),
        'cases_aggregated_by_ethnicity': cases_aggregated_by_ethnicity(selected_hospital=selected_hospital),
        'cases_aggregated_by_sex': cases_aggregated_by_sex(selected_hospital=selected_hospital),
        'cases_aggregated_by_deprivation': cases_aggregated_by_deprivation_score(selected_hospital=selected_hospital),
        'percent_completed_hospital': total_percent_hospital,
        'percent_completed_trust': total_percent_trust,
        'count_of_current_cohort_registered_cases_in_this_hospital': count_of_current_cohort_registered_cases_in_this_hospital,
        'count_of_current_cohort_registered_completed_cases_in_this_hospital': count_of_current_cohort_registered_completed_cases_in_this_hospital,
        'count_of_current_cohort_registered_cases_in_this_hospital_trust': count_of_current_cohort_registered_cases_in_this_hospital_trust,
        'count_of_current_cohort_registered_completed_cases_in_this_hospital_trust': count_of_current_cohort_registered_completed_cases_in_this_hospital_trust,
        'cohort_data': cohort_data,
        'individual_kpi_choices': INDIVIDUAL_KPI_MEASURES
    })


def selected_trust_kpis(request, hospital_id):
    """
    HTMX get request returning trust_level_kpi.html partial

    This aggregates all KPI measures at different levels of abstraction related to the selected hospital
    Organisation level, Trust level, ICB level, NHS Region, OPEN UK level, country level and national level

    It uses django aggregation which is super quick
    """

    # filter all Hospitals based on level of abstraction
    hospital_trust = HospitalTrust.objects.get(pk=hospital_id)
    hospital_level = HospitalTrust.objects.filter(
        pk=hospital_id).order_by('OrganisationName')
    trust_level = HospitalTrust.objects.filter(
        ParentName=hospital_trust.ParentName).order_by('OrganisationName')
    icb_level = HospitalTrust.objects.filter(
        ICBODSCode=hospital_trust.ICBODSCode).order_by('OrganisationName')
    nhs_level = HospitalTrust.objects.filter(
        NHSEnglandRegionCode=hospital_trust.NHSEnglandRegionCode).order_by('OrganisationName')
    open_uk_level = HospitalTrust.objects.filter(
        OPENUKNetworkCode=hospital_trust.OPENUKNetworkCode).order_by('OrganisationName')
    country_level = HospitalTrust.objects.filter(
        CountryONSCode=hospital_trust.CountryONSCode).order_by('OrganisationName')
    national_level = HospitalTrust.objects.all().order_by('OrganisationName')

    # create function to aggregate all fields in the related KPI model
    all_kpi_measures = ['paediatrician_with_expertise_in_epilepsies', 'epilepsy_specialist_nurse', 'tertiary_input', 'epilepsy_surgery_referral', 'ecg', 'mri', 'assessment_of_mental_health_issues', 'mental_health_support', 'comprehensive_care_planning_agreement', 'patient_held_individualised_epilepsy_document',
                        'care_planning_has_been_updated_when_necessary', 'comprehensive_care_planning_content', 'parental_prolonged_seizures_care_plan', 'water_safety', 'first_aid', 'general_participation_and_risk', 'service_contact_details', 'sudep', 'school_individual_healthcare_plan']
    aggregation_fields = {}
    for measure in all_kpi_measures:
        aggregation_fields[f'{measure}'] = Sum(f'kpi__{measure}')
    aggregation_fields['total_number_of_cases'] = Count(f'kpi__pk')

    # aggregate at each level of abstraction
    hospital_kpis = hospital_level.aggregate(**aggregation_fields)
    trust_kpis = trust_level.aggregate(**aggregation_fields)
    icb_kpis = icb_level.aggregate(**aggregation_fields)
    nhs_kpis = nhs_level.aggregate(**aggregation_fields)
    open_uk_kpis = open_uk_level.aggregate(**aggregation_fields)
    country_kpis = country_level.aggregate(**aggregation_fields)
    national_kpis = national_level.aggregate(**aggregation_fields)

    # create an empty instance of KPI model to access the labels - this is a bit of a hack but works and
    # and has very little overhead
    hospital_organisation = HospitalTrust.objects.get(pk=hospital_id)
    kpis = KPI.objects.create(
        hospital_organisation=hospital_organisation,
        parent_trust=hospital_organisation.ParentName
    )

    template_name = 'epilepsy12/partials/kpis/kpis.html'
    context = {
        'hospital_organisation': hospital_organisation,
        'hospital_kpis': hospital_kpis,
        'trust_kpis': trust_kpis,
        'icb_kpis': icb_kpis,
        'nhs_kpis': nhs_kpis,
        'open_uk_kpis': open_uk_kpis,
        'country_kpis': country_kpis,
        'national_kpis': national_kpis,
        'kpis': kpis
    }

    response = render(
        request=request, template_name=template_name, context=context)

    # trigger a GET request from the steps template
    trigger_client_event(
        response=response,
        name="registration_active",
        params={})  # reloads the form to show the active steps
    return response


@ login_required
def child_hospital_select(request, hospital_id, template_name):
    """
    POST call back from hospital_select to allow user to toggle between hospitals in selected trust
    """

    selected_hospital_id = request.POST.get('child_hospital_select')

    # get currently selected hospital
    hospital_trust = HospitalTrust.objects.get(pk=selected_hospital_id)

    # trigger page reload with new hospital
    return HttpResponseClientRedirect(reverse(template_name, kwargs={'hospital_id': hospital_trust.pk}))


@ login_required
def view_preference(request, hospital_id, template_name):
    """
    POST request from Toggle in has rcpch_view_preference.html template
    Users can toggle between national, trust and hospital views.
    Only RCPCH staff can request a national view.
    """
    hospital_trust = HospitalTrust.objects.get(pk=hospital_id)

    request.user.view_preference = request.htmx.trigger_name
    request.user.save()

    return HttpResponseClientRedirect(reverse(template_name, kwargs={'hospital_id': hospital_trust.pk}))


def selected_trust_select_kpi(request, hospital_id):
    """
    POST request from dropdown in selected_hospital_summary.html

    It takes the kpi_name parameter in the HTMX request which contains the value of the selected KPI measure from
    the select field. This is then aggregated across the levels of abstraction
    """

    hospital_trust = HospitalTrust.objects.get(pk=hospital_id)
    kpi_name = request.POST.get('kpi_name')
    if kpi_name is None:
        # on page load there may be no kpi_name - default to paediatrician_with_experise_in_epilepsy
        kpi_name = INDIVIDUAL_KPI_MEASURES[0][0]
    kpi_value = value_from_key(
        key=kpi_name, choices=INDIVIDUAL_KPI_MEASURES)

    hospital_level = HospitalTrust.objects.filter(
        pk=hospital_id).order_by('OrganisationName')
    trust_level = HospitalTrust.objects.filter(
        ParentName=hospital_trust.ParentName).order_by('OrganisationName')
    icb_level = HospitalTrust.objects.filter(
        ICBODSCode=hospital_trust.ICBODSCode).order_by('OrganisationName')
    nhs_level = HospitalTrust.objects.filter(
        NHSEnglandRegionCode=hospital_trust.NHSEnglandRegionCode).order_by('OrganisationName')
    open_uk_level = HospitalTrust.objects.filter(
        OPENUKNetworkCode=hospital_trust.OPENUKNetworkCode).order_by('OrganisationName')
    country_level = HospitalTrust.objects.filter(
        CountryONSCode=hospital_trust.CountryONSCode).order_by('OrganisationName')
    national_level = HospitalTrust.objects.all().order_by('OrganisationName')

    # create aggregate function for selected KPI measure
    aggregate_parameter = {}
    aggregate_parameter[f'{kpi_name}'] = Sum(f'kpi__{kpi_name}')
    aggregate_parameter['total_cases'] = Count(f'kpi__pk')

    hospital_kpi = hospital_level.aggregate(**aggregate_parameter)
    trust_kpi = trust_level.aggregate(**aggregate_parameter)
    icb_kpi = icb_level.aggregate(**aggregate_parameter)
    nhs_kpi = nhs_level.aggregate(**aggregate_parameter)
    open_uk_kpi = open_uk_level.aggregate(**aggregate_parameter)
    country_kpi = country_level.aggregate(**aggregate_parameter)
    national_kpi = national_level.aggregate(**aggregate_parameter)

    context = {
        'kpi_name': kpi_name,
        'kpi_value': kpi_value,
        'selected_hospital': hospital_trust,
        'hospital_kpi': hospital_kpi[kpi_name],
        'total_hospital_kpi_cases': hospital_kpi['total_cases'],
        'trust_kpi': trust_kpi[kpi_name],
        'total_trust_kpi_cases': trust_kpi['total_cases'],
        'icb_kpi': icb_kpi[kpi_name],
        'total_icb_kpi_cases': icb_kpi['total_cases'],
        'nhs_kpi': nhs_kpi[kpi_name],
        'total_nhs_kpi_cases': nhs_kpi['total_cases'],
        'open_uk_kpi': open_uk_kpi[kpi_name],
        'total_open_uk_kpi_cases': open_uk_kpi['total_cases'],
        'country_kpi': country_kpi[kpi_name],
        'total_country_kpi_cases': country_kpi['total_cases'],
        'national_kpi': national_kpi[kpi_name],
        'total_national_kpi_cases': national_kpi['total_cases'],
        # 'ranked': ranked_kpis
    }

    template_name = 'epilepsy12/partials/hospital/metric.html'

    return render(request=request, template_name=template_name, context=context)
