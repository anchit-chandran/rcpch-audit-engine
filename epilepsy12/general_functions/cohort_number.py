"""
Cohort numbers functions
"""

# python imports
from datetime import date
from dateutil.relativedelta import relativedelta

# e12 imports
from .date_functions import first_tuesday_in_january


def cohort_number_from_enrolment_date(enrolment_date: date) -> int:
    """
    * Returns the cohort number as an `int` from the enrolment date as a Python `datetime.date`

    * Dates which are too early to return a valid cohort number will return `None`. Ensure to test for a `None` return value before doing anything with the result.

    * Cohort Number is used to identify the groups in the audit by year.

    * Cohorts are defined between 1st December year and 30th November in the subsequent year.

    * Time zone is not explicity supplied. Since this is a UK audit, time zone is assumed always to be UK.

    #### Examples of cohort numbers:
    Cohort 4: 1 December 2020 - 30 November 2021
    Cohort 5: 1 December 2021 - 30 November 2022
    Cohort 6: 1 December 2022 - 30 November 2023
    Cohort 7: 1 December 2023 - 30 November 2024
    """

    # reject dates which are too early with a return value of None
    if enrolment_date.year < 2020:
        return None

    for cohort_starting_year in range(2020, 2030):
        if enrolment_date >= date(cohort_starting_year, 12, 1) and enrolment_date <= date(cohort_starting_year+1, 11, 30):
            return cohort_starting_year - 2016


def cohort_start_date_from_cohort_number(cohort):
    """
    Returns start date of cohort
    """

    cohort_year = 2016 + cohort
    return date(cohort_year, 12, 1)


def current_cohort_start_date():
    """
    Returns the start date of the current cohort
    """
    today = date.today()

    if date(today.year, 12, 1) < today:
        return date(today.year, 12, 1)
    else:
        return date(today.year-1, 12, 1)


def get_current_cohort_data() -> dict:
    """
    Returns all current cohort dates and cohort number
    Return keys are:
    'cohort_start_date'
    'cohort_end_date'
    'cohort'
    'submission_date'
    'days_remaining'
    """
    current_cohort = cohort_number_from_enrolment_date(
        current_cohort_start_date())

    cohort_data = {
        'cohort_start_date': current_cohort_start_date(),
        'cohort_end_date': date(current_cohort_start_date().year+1, 11, 30),
        'cohort': current_cohort,
        'submission_date': first_tuesday_in_january(current_cohort_start_date().year+1) + relativedelta(days=7),
        'days_remaining':  relativedelta(first_tuesday_in_january(current_cohort_start_date().year+1) + relativedelta(days=7) - date.today()).days
    }

    return cohort_data
