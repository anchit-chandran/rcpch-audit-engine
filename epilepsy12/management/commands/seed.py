from random import randint, choice
from datetime import date
from dateutil.relativedelta import relativedelta
from random import randint
from django.core.management.base import BaseCommand


from ...constants import ETHNICITIES, DUMMY_NAMES
from ...models import HospitalTrust, Keyword, Case, Site, Registration
from ...constants import ALL_HOSPITALS, KEYWORDS, WELSH_HOSPITALS
from ...general_functions import random_postcodes, random_date, first_tuesday_in_january, current_cohort_start_date
from .create_groups import create_groups, add_permissions_to_existing_groups, delete_and_reallocate_permissions
from .create_e12_records import create_epilepsy12_record, create_registrations
from .add_codes_to_hospitals import add_codes_to_hospital


class Command(BaseCommand):
    help = "seed database with hospital trust data for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        if (options['mode'] == 'delete_hospitals'):
            self.stdout.write('Deleting hospital trust data...')
            delete_hospitals()
        elif (options['mode'] == 'seed_hospitals'):
            self.stdout.write('seeding hospital trust data...')
            run_hospitals_seed()
        elif (options['mode'] == 'seed_welsh_hospitals'):
            self.stdout.write('seeding hospital trust data...')
            run_welsh_hospitals_seed()
        elif (options['mode'] == 'add_codes_to_english_hospitals'):
            self.stdout.write(
                'adding ODS codes to existing English hospital trust records...')
            add_codes_to_english_hospitals()
        elif (options['mode'] == 'seed_semiology_keywords'):
            self.stdout.write('seeding hospital trust data...')
            run_semiology_keywords_seed()
        elif (options['mode'] == 'seed_dummy_cases'):
            self.stdout.write('seeding with dummy case data...')
            run_dummy_cases_seed()
        elif (options['mode'] == 'seed_registrations'):
            self.stdout.write(
                'register cases in audit and complete all fields with random answers...')
            run_registrations()
        elif (options['mode'] == 'seed_groups_and_permissions'):
            self.stdout.write('setting up groups and permissions...')
            create_groups()
        elif (options['mode'] == 'add_permissions_to_existing_groups'):
            self.stdout.write('adding permissions to groups...')
            add_permissions_to_existing_groups()
        elif (options['mode'] == 'delete_all_groups_and_recreate'):
            self.stdout.write(
                'deleting all groups/permissions and reallocating...')
            delete_and_reallocate_permissions()

        else:
            self.stdout.write('No options supplied...')
        print('\033[38;2;17;167;142m')
        self.stdout.write(image())
        print('\033[38;2;17;167;142m')
        self.stdout.write('done.')


def run_semiology_keywords_seed():
    added = 0
    for index, semiology_keyword in enumerate(KEYWORDS):
        if Keyword.objects.filter(keyword=semiology_keyword["title"]).exists():
            print(
                f'Keywords already exist. Skipping this step...')
            return
        new_keyword = Keyword(
            keyword=semiology_keyword["title"],
            category=semiology_keyword["category"]
        )
        try:
            new_keyword.save()
        except Exception as e:
            print(f"Error at {semiology_keyword['title']}: error: {e}")
        added += 1
        print(
            f"added {semiology_keyword['title']} in category {semiology_keyword['category']}")
    image()
    print(f"Keywords added: {added}")


def run_hospitals_seed():
    # this adds all the English hospitals from JSON in the constants folder
    # There are also lists of hospitals across northern ireland, wales and scotland, but the JSON has a different structure
    if HospitalTrust.objects.all().exists():
        print('Hospital table already exists. Skipping this step...')
        return
    added = 0
    for index, hospital in enumerate(ALL_HOSPITALS):
        if hospital["Sector"] == "NHS Sector":
            hospital_trust = HospitalTrust(
                OrganisationID=hospital.get("OrganisationID"),
                OrganisationCode=hospital.get("OrganisationCode", None),
                OrganisationType=hospital.get("OrganisationType", None),
                SubType=hospital.get("SubType", None),
                Sector=hospital.get("Sector", None),
                OrganisationStatus=hospital.get("OrganisationStatus", None),
                IsPimsManaged=hospital.get("IsPimsManaged", None),
                OrganisationName=hospital.get("OrganisationName", None),
                Address1=hospital.get("Address1", None),
                Address2=hospital.get("Address2", None),
                Address3=hospital.get("Address3", None),
                City=hospital.get("City", None),
                County=hospital.get("County", None),
                Postcode=hospital.get("Postcode", None),
                Latitude=hospital.get("Latitude", None),
                Longitude=hospital.get("Longitude", None),
                ParentODSCode=hospital.get("ParentODSCode", None),
                ParentName=hospital.get("ParentName", None),
                Phone=hospital.get("Phone", None),
                Email=hospital.get("Email", None),
                Website=hospital.get("Website", None),
                Fax=hospital.get("Fax", None),
                DateValid=date(2023, 1, 1)
            )

            add_codes_to_hospital(hospital_trust=hospital_trust)

            try:
                hospital_trust.save()
            except Exception as error:
                print("Exception at "+hospital["ParentName"])
                print(error)
            added += 1
            chosen_hospital = hospital["OrganisationName"]
            print(
                '\033[31m', f"New English hospital added...{added}: {chosen_hospital}", '\033[31m')
    print(f"English Hospitals added...{added}")

    run_welsh_hospitals_seed()


def run_welsh_hospitals_seed():
    # this adds all the English hospitals from JSON in the constants folder
    # There are also lists of hospitals across northern ireland, wales and scotland, but the JSON has a different structure
    added = 0

    for index, hospital in enumerate(WELSH_HOSPITALS):
        try:
            welsh_hospital = HospitalTrust(
                OrganisationID=index + 90000,
                OrganisationCode=hospital.get(
                    "OrganisationCode", None),
                OrganisationType=hospital.get("OrganisationType", None),
                SubType=hospital.get("SubType", None),
                Sector=hospital.get("Sector", None),
                OrganisationStatus=hospital.get("OrganisationStatus", None),
                IsPimsManaged=hospital.get("IsPimsManaged", None),
                OrganisationName=hospital.get("OrganisationName", None),
                Address1=hospital.get("Address1", None),
                Address2=hospital.get("Address2", None),
                Address3=hospital.get("Address3", None),
                City=hospital.get("City", None),
                County=hospital.get("County", None),
                Postcode=hospital.get("Postcode", None),
                Latitude=hospital.get("Latitude", None),
                Longitude=hospital.get("Longitude", None),
                ParentODSCode=hospital.get("ParentODSCode", None),
                ParentName=hospital.get("ParentName", None),
                Phone=hospital.get("Phone", None),
                Email=hospital.get("Email", None),
                Website=hospital.get("Website", None),
                Fax=hospital.get("Fax", None),
                DateValid=date(2023, 1, 1)
            )
            welsh_hospital.save()
            print(
                '\033[94m', f"New Welsh hospital added...{added}: {welsh_hospital.OrganisationName}({welsh_hospital.ParentName})", '\033[94m')
            added += 1

            add_codes_to_hospital(welsh_hospital)

        except Exception as error:
            print("Exception creating "+hospital["OrganisationName"])

    print(f"Welsh Hospitals added...{added}")


def add_codes_to_english_hospitals():
    """
    A custom function to run in the rare likelihood that an existing table of hospitals exists but does not have 
    the ODS codes in it
    """
    index = 0
    for hospital in HospitalTrust.objects.all():
        add_codes_to_hospital(hospital)
        index += 1
    print(f'Updated {index} English hospitals with ODS Codes.')


def delete_hospitals():
    try:
        HospitalTrust.objects.all().delete()
    except:
        print("Unable to delete Hospital table")
    print("...all hospitals deleted.")


def run_dummy_cases_seed():
    added = 0

    # there should not be any cases yet, but sometimes seed gets run more than once
    if Case.objects.all().exists():
        print(f'Cases already exist. Skipping this step...')
        return

    postcode_list = random_postcodes.generate_postcodes(requested_number=100)

    for index in range(len(DUMMY_NAMES)-1):
        random_date = date(randint(2005, 2021), randint(1, 12), randint(1, 28))
        nhs_number = randint(1000000000, 9999999999)
        first_name = DUMMY_NAMES[index]['firstname']
        surname = DUMMY_NAMES[index]['lastname']
        gender_object = DUMMY_NAMES[index]['gender']
        if gender_object == 'm':
            sex = 1
        else:
            sex = 2
        date_of_birth = random_date
        postcode = postcode_list[index]
        ethnicity = choice(ETHNICITIES)[0]

        # get a random hospital
        hospital_trust = HospitalTrust.objects.filter(
            Sector="NHS Sector").order_by("?").first()

        case_has_error = False

        try:
            new_case = Case(
                locked=False,
                nhs_number=nhs_number,
                first_name=first_name,
                surname=surname,
                sex=sex,
                date_of_birth=date_of_birth,
                postcode=postcode,
                ethnicity=ethnicity
            )
            new_case.save()
        except Exception as e:
            print(f"Error saving case: {e}")
            case_has_error = True

        if not case_has_error:
            try:
                new_site = Site.objects.create(
                    hospital_trust=hospital_trust,
                    site_is_actively_involved_in_epilepsy_care=True,
                    site_is_primary_centre_of_epilepsy_care=True,
                    case=new_case
                )
                new_site.save()
            except Exception as e:
                print(f"Error saving site: {e}")

            added += 1
            print(f"Saved {new_case.first_name} {new_case.surname} at {new_site.hospital_trust.ParentName}({new_site.hospital_trust.OrganisationName})...")
    print(f"Saved {added} cases.")


def run_registrations():
    """
    Calling function to register all cases in Epilepsy12 and complete all fields with random answers
    """
    create_registrations()

    complete_registrations()


def complete_registrations():
    """
    Loop through the registrations and score all fields
    """
    for registration in Registration.objects.all():
        current_cohort_end_date = first_tuesday_in_january(
            current_cohort_start_date().year + 2) + relativedelta(days=7)
        registration.registration_date = random_date(
            start=current_cohort_start_date(), end=current_cohort_end_date)
        registration.eligibility_criteria_met = True
        registration.save()

        create_epilepsy12_record(registration_instance=registration)

    # calculate national level kpis
    # kpis_for_abstraction_level()


def image():
    return """

                                .^~^      ^777777!~:       ^!???7~:
                                ^JJJ:.:!^ 7#BGPPPGBGY:   !5BBGPPGBBY.
                                 :~!!?J~. !BBJ    YBB?  ?BB5~.  .~J^
                              .:~7?JJ?:   !BBY^~~!PBB~ .GBG:
                              .~!?JJJJ^   !BBGGGBBBY^  .PBG^
                                 ?J~~7?:  !BBJ.:?BB5^   ~GBG?^:^~JP7
                                :?:   .   !BBJ   ~PBG?.  :?PBBBBBG5!
                                ..::...     .::. ...:^::. .. .:^~~^:.
                                !GPGGGGPY7.   :!?JJJJ?7~..PGP:    !GGJ
                                7BBY~~!YBBY  !JJ?!^^^!??::GBG:    7BBJ
                                7BB?   .GBG.^JJ7.     .. .GBG!^^^^JBBJ
                                7BB577?5BBJ ~JJ!         .GBBGGGGGGBBJ
                                7BBGPPP5J~  :JJJ^.   .^^ .GBG^.::.?BBJ
                                7#B?         :7JJ?77?JJ?^:GBB:    7##Y
                                ~YY!           :~!77!!^. .JYJ.    ~YY7


                                           Epilepsy12 2022

                """
