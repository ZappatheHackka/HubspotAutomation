import datetime
import os
from dateutil.relativedelta import relativedelta
import email.generator
from imapclient import IMAPClient
from dataclasses import dataclass
from hubspot import HubSpot
from hubspot.crm.contacts import ApiException, Filter, FilterGroup, PublicObjectSearchRequest, SimplePublicObjectInput


# TODO: [COMPLETE] Authorize w/ Hubspot-They have a library!
HUBSPOT_ACCESS_TOKEN = os.environ['HUBSPOT_ACCESS_TOKEN']
HUBSPOT_SECRET = os.environ['HUBSPOT_SECRET']
USER = os.environ['WORK_EMAIL']
PASS = os.environ['WORK_PASS']
PORT = 993
HOST = "idhoops.com"
VALID_GROUPS = ['2021 Skills Accelerator', '2021 Pure Fundamentals', 'Level 1 Weekday Shooting & Dribbling',
                'Level 2 Weekday Shooting & Dribbling', 'Party Attendee', 'Prospect', '2021Junior Hoopers',
                'Robbinsville Coaches Clinic', 'Schools Out']


answer = input("Welcome to the Inner Drive Hoops Hubspot auto-registration program!\n\n"
               "Would you like to run in Manual Mode? (type 'y' for yes or 'n' for no)\n\n"
               "(Manual Mode requires a manual approval for completely NEW contacts to be created within Hubspot"
               " and for any property to be updated.\nIf you decline, the script will run in Automatic Mode, and all "
               "new contacts will be automatically created.)\n").lower()

if answer == 'y':
    is_manual = True
    print("Running in Manual...")
elif answer == 'n':
    is_manual = False
    print("Running in automatic...")


api_client = HubSpot(access_token=HUBSPOT_ACCESS_TOKEN)


# TODO: make a Manual Mode that requires permission to update contacts
def manual_mode(client, contact, firstname, lastname):
    contact_id = contact.id

    # UPDATING FIRST NAME

    if firstname == contact.properties['firstname']:
        print(f'{firstname} is equal to {contact.properties['firstname']}, moving on...')
    else:
        answer = input(f"{firstname} does not match the Hubspot record of {contact.properties['firstname']}.\n"
                       f"Would you like to change the 'firstname' value to {firstname}?\n"
                       f"Type 'y' for yes or 'n' for no. ").lower()
        if answer == 'y':
            print("Very well. Updating 'firstname' info...")
            try:
                updated_info = SimplePublicObjectInput(
                    properties={
                        'firstname': firstname
                    }
                )
                api_client.crm.contacts.basic_api.update(
                    contact_id=contact_id,
                    simple_public_object_input=updated_info
                )
                print("Contact updated successfully!")
            except ApiException as e:
                print(f"Failed to update contact: {e}")
        else:
            print("Very well, doing nothing for the first name property...")

    # UPDATING LAST NAME

    if lastname == contact.properties['lastname']:
        print(f'{lastname} is equal to {contact.properties['lastname']}, moving on...')
    else:
        answer = input(f"{lastname} does not match the Hubspot record of {contact.properties['lastname']}.\n"
                       f"Would you like to change the 'lastname' value to {lastname}?\n"
                       f"Type 'y' for yes or 'n' for no. ").lower()
        if answer == 'y':
            print("Very well. Updating 'firstname' info...")
            try:
                updated_info = SimplePublicObjectInput(
                    properties={
                        'lastname': lastname
                    }
                )
                api_client.crm.contacts.basic_api.update(
                    contact_id=contact_id,
                    simple_public_object_input=updated_info
                )
                print("Contact updated successfully!")
            except ApiException as e:
                print(f"Failed to update contact: {e}")
        else:
            print("Very well, doing nothing for the last name property...")

    # UPDATING EMAIL

    if client.email == contact.properties['email']:
        print(f'{client.email} is equal to {contact.properties['email']}, moving on...')
    else:
        answer = input(f"{client.email} does not match the Hubspot record of {contact.properties['email']}.\n"
                       f"Would you like to change the 'email' value to {client.email}?\n"
                       f"Type 'y' for yes or 'n' for no. ").lower()
        if answer == 'y':
            print("Very well. Updating 'firstname' info...")
            try:
                updated_info = SimplePublicObjectInput(
                    properties={
                        'email': client.email
                    }
                )
                api_client.crm.contacts.basic_api.update(
                    contact_id=contact_id,
                    simple_public_object_input=updated_info
                )
                print("Contact updated successfully!")
            except ApiException as e:
                print(f"Failed to update contact: {e}")
        else:
            print("Very well, doing nothing for the email property...")

    # UPDATING MOBILEPHONE

    if client.phone:
        if client.phone == contact.properties['mobilephone']:
            print(f'{client.phone} is equal to {contact.properties['mobilephone']}, moving on...')
        else:
            answer = input(f"{client.phone} does not match the Hubspot record of {contact.properties['mobilephone']}.\n"
                           f"Would you like to change the 'mobilephone' value to {client.phone}?\n"
                           f"Type 'y' for yes or 'n' for no. ").lower()
            if answer == 'y':
                print("Very well. Updating 'mobile phone' info...")
                try:
                    updated_info = SimplePublicObjectInput(
                        properties={
                            'mobilephone': client.phone
                        }
                    )
                    api_client.crm.contacts.basic_api.update(
                        contact_id=contact_id,
                        simple_public_object_input=updated_info
                    )
                    print("Contact updated successfully!")
                except ApiException as e:
                    print(f"Failed to update contact: {e}")
            else:
                print("Very well, doing nothing for the mobile phone property...")
    else:
        print(f"No phone number entered in {client.name}'s registration form. Moving on to next property...")

    # UPDATING KID'S YEAR OF BIRTH

    if client.childdob:
        if isadult(client.childdob):
            if contact.properties['kid_s_year_s_of_birth'].strip() is None:
                    answer = input(f"No age is set--update age to Adult for {client.name}?\n"
                                   f"Type 'y' for yes or 'n' for no. ").lower()
                    if answer == 'y':
                        try:
                            print('Updating age...')
                            new_info = "Adult"
                            updated_info = SimplePublicObjectInput(
                               properties={
                                    'kid_s_year_s_of_birth': new_info
                                }
                            )
                            api_client.crm.contacts.basic_api.update(
                                contact_id=contact_id,
                                simple_public_object_input=updated_info
                            )
                            print("Age successfully updated, moving on...")
                        except ApiException as e:
                            print(f"Updating error: {e}, skipping...")
                    else:
                        print("Very well, moving on...")
            else:
                try:
                    bdays = contact.properties['kid_s_year_s_of_birth'].split(";")
                    if 'Adult' in bdays:
                        print("Age up to date. Moving on...")
                    else:
                        answer = input(f"Age is missing from Hubspot ages--append Adult status to ages?\n"
                                       f"Type 'y' for yes or 'n' for no. ").lower()
                        if answer == 'y':
                            try:
                                new_info = contact.properties['kid_s_year_s_of_birth'] + ";Adult"
                                updated_info = SimplePublicObjectInput(
                                    properties={
                                        'kid_s_year_s_of_birth': new_info
                                    }
                                )
                                api_client.crm.contacts.basic_api.update(
                                    contact_id=contact_id,
                                    simple_public_object_input=updated_info
                                )
                                print("Adult status appended to Child's ages. Moving on...")
                            except ApiException as e:
                                print(f"Updating error: {e}, skipping...")
                        else:
                            print("Very well, moving on...")

                except AttributeError:
                    if contact.properties['kid_s_year_s_of_birth'] == 'Adult':
                        print("Adult status up to date. Moving on...")
                    else:
                        answer = input(f"Adult status is not listed in the Age property: "
                                       f"{contact.properties['kid_s_year_s_of_birth']}.\n Add Adult status? Type "
                                       "'y' for yes or 'n' for no. ").lower()
                        if answer == 'y':
                            print("Very well. Adding Adult status to Age property...")
                            try:
                                new_info = contact.properties['kid_s_year_s_of_birth'] + ";Adult"
                                updated_info = SimplePublicObjectInput(
                                    properties={
                                        'kid_s_year_s_of_birth': new_info
                                    }
                                )
                                api_client.crm.contacts.basic_api.update(
                                    contact_id=contact_id,
                                    simple_public_object_input=updated_info
                                )
                                print("Adult status appended to Child's ages. Moving on...")
                            except ApiException as e:
                                print(f"Updating error: {e}, skipping...")
                        else:
                            print("Very well, not updating Age properties and moving on...")
        else:
            if client.childdob:
                if contact.properties['kid_s_year_s_of_birth'] is not None:
                    bday = client.childdob.split()
                    bday_year = bday[3]
                    try:
                        list_of_bdays = contact.properties['kid_s_year_s_of_birth'].split(";")
                        if bday_year in list_of_bdays:
                            print(f"Birthday up to date: {bday_year} is in {list_of_bdays}. Moving on...")
                        else:
                            answer = input(f"Birthday year {bday_year} not found in Hubspot entered Bday years: {list_of_bdays}.\n"
                                           f"Would you like to update the list? 'y' for yes, 'n' for no. ").lower()
                            if answer == 'y':
                                print("Very well. Updating bdays...")
                                try:
                                    new_info = list_of_bdays + f";{bday_year}"
                                    updated_info = SimplePublicObjectInput(
                                        properties={
                                            'kid_s_year_s_of_birth': new_info
                                        }
                                    )
                                    api_client.crm.contacts.basic_api.update(
                                        contact_id=contact_id,
                                        simple_public_object_input=updated_info
                                    )
                                except ApiException as e:
                                    print(f"Skipping update, error: {e}")
                            else:
                                print("Very well, moving on...")
                    except AttributeError:
                        if contact.properties['kid_s_year_s_of_birth'] == bday_year:
                            print("Birthday up to date, moving on...")
                        else:
                            answer = input(
                                f"Birthday year {bday_year} does not match Hubspot's bday year: {contact.properties['kid_s_year_s_of_birth']}.\n"
                                f"Would you like to add {bday_year} to the property? 'y' for yes, 'n' for no. ").lower()
                            if answer == 'y':
                                print("Very well. Updating bdays...")
                                try:
                                    new_info = contact.properties['kid_s_year_s_of_birth'] + f";{bday_year}"
                                    updated_info = SimplePublicObjectInput(
                                        properties={
                                            'kid_s_year_s_of_birth': new_info
                                        }
                                    )
                                    api_client.crm.contacts.basic_api.update(
                                        contact_id=contact_id,
                                        simple_public_object_input=updated_info
                                    )
                                    print("Bday successfully updated. Moving to next property...")
                                except ApiException as e:
                                    print(f"Skipping update, error: {e}")
                            else:
                                print("Very well, moving on...")
    else:
        print(f"No DoB entered in {client.name}'s registration form. Moving to next property...")

    # UPDATING KID'S NAME(s)

    if client.childname:
        if client.childname == " ":
            print(f"Adult registrant detected: {client.name}, skipping 'childname' property...")
        else:
            children = contact.properties['kids_names'].split()
            commaname = client.childname + ","
            if client.childname or commaname in children:
                print(f"{client.childname} already listed in {children}, moving on...")
            else:
                answer = input(f"{client.childname} is not listed under 'kids_names' in Hubspot: {children}.\n"
                               f"Would you like to add {client.childname} to {children}? 'y' for yes, 'n' for no. ").lower()
                if answer == 'y':
                    print("Very well, updating child name info...")
                    try:
                        new_info = contact.properties['kids_names'] + client.childname
                        updated_info = SimplePublicObjectInput(
                            properties={
                                'kids_names': new_info
                            }
                        )
                        api_client.crm.contacts.basic_api.update(
                            contact_id=contact_id,
                            simple_public_object_input=updated_info
                        )
                        print("Child names successfully updated. Moving to next property...")
                    except ApiException as e:
                        print(f"Skipping update, error: {e}")

    # UPDATING ADDRESS

    if client.address:
        if contact.properties['address'] is not None:
            if client.address == contact.properties['address']:
                print(f"Submitted address {client.address} matches Hubspot address {contact.properties['address']}.\n"
                      f"Moving on...")
            else:
                answer = input(f"Submitted address {client.address} does not match the Hubspot address "
                               f"{contact.properties['address']}."
                               f"\nWould you like to update the Hubspot value to {client.address}? "
                               f"Type 'y' for yes or 'n' for no. ").lower()
                if answer == 'y':
                    print("Very well, updating address...")
                    try:
                        new_info = client.address
                        updated_info = SimplePublicObjectInput(
                            properties={
                                'address': new_info
                            }
                        )
                        api_client.crm.contacts.basic_api.update(
                            contact_id=contact_id,
                            simple_public_object_input=updated_info
                        )
                        print("Address successfully updated. Moving to next property...")
                    except ApiException as e:
                        print(f"Skipping update, error: {e}")
                else:
                    print("Very well, moving on...")
        else:
            print(f"No address in Hubspot for {client.name}. Updating address...")
            try:
                new_info = client.address
                updated_info = SimplePublicObjectInput(
                    properties={
                        'address': new_info
                    }
                )
                api_client.crm.contacts.basic_api.update(
                    contact_id=contact_id,
                    simple_public_object_input=updated_info
                )
                print("Address successfully updated. Moving to next property...")
            except ApiException as e:
                print(f"Skipping update, error: {e}")
    else:
        print(f"No address submitted for {client.name}. Moving to next property...")

    # UPDATING ZIP CODE

    if client.zip:
        if contact.properties['zip'] is not None:
            if client.zip == contact.properties['zip']:
                print(f"Submitted zip code {client.zip} matches Hubspot zip code {contact.properties['zip']}.\n"
                      f"Moving on...")
            else:
                answer = input(f"Submitted zip {client.zip} does not match the Hubspot zip code"
                               f" {contact.properties['zip']}."
                               f"Would you like to update the Hubspot value to {client.zip}?"
                               f"Type 'y' for yes or 'n' for no. ").lower()
                if answer == 'y':
                    print("Very well, updating zip code...")
                    try:
                        new_info = client.zip
                        updated_info = SimplePublicObjectInput(
                            properties={
                                'zip': new_info
                            }
                        )
                        api_client.crm.contacts.basic_api.update(
                            contact_id=contact_id,
                            simple_public_object_input=updated_info
                        )
                        print("Zip code successfully updated. Moving to next property...")
                    except ApiException as e:
                        print(f"Skipping update, error: {e}")
        else:
            print(f"No zip code in Hubspot for {client.name}. Updating zip code...")
            try:
                new_info = client.zip
                updated_info = SimplePublicObjectInput(
                    properties={
                        'zip': new_info
                    }
                )
                api_client.crm.contacts.basic_api.update(
                    contact_id=contact_id,
                    simple_public_object_input=updated_info
                )
                print("Zip code successfully updated. Moving to next property...")
            except ApiException as e:
                print(f"Skipping update, error: {e}")
    else:
        print(f"No zip code submitted for {client.name}. Moving to next property...")

    # UPDATING CITY

    if client.city:
        if contact.properties['city'] is not None:
            if client.city == contact.properties['city']:
                print(f"Submitted city {client.city} matches Hubspot city {contact.properties['city']}.\n"
                      f"Moving on...")
            else:
                answer = input(f"Submitted city {client.city} does not match the Hubspot city "
                               f"{contact.properties['city']}."
                               f"Would you like to update the Hubspot value to {client.city}?"
                               f"Type 'y' for yes or 'n' for no. ").lower()
                if answer == 'y':
                    print("Very well, updating city...")
                    try:
                        new_info = client.city
                        updated_info = SimplePublicObjectInput(
                            properties={
                                'city': new_info
                            }
                        )
                        api_client.crm.contacts.basic_api.update(
                            contact_id=contact_id,
                            simple_public_object_input=updated_info
                        )
                        print("City successfully updated. Moving to next property...")
                    except ApiException as e:
                        print(f"Skipping update, error: {e}")
                else:
                    print("skibidi")
        else:
            print(f"No city in Hubspot for {client.name}. Updating city...")
            try:
                new_info = client.city
                updated_info = SimplePublicObjectInput(
                    properties={
                        'city': new_info
                    }
                )
                api_client.crm.contacts.basic_api.update(
                    contact_id=contact_id,
                    simple_public_object_input=updated_info
                )
                print("City successfully updated. Moving to next property...")
            except ApiException as e:
                print(f"Skipping update, error: {e}")
    else:
        print(f"No city submitted for {client.name}. Moving to next property...")

    # UPDATING STATE

    if client.state:
        if contact.properties['state'] is not None:
            if client.state == contact.properties['state']:
                print(f"Submitted state {client.state} matches Hubspot address {contact.properties['state']}.\n"
                      f"Moving on...")
            else:
                answer = input(f"Submitted state {client.state} does not match the Hubspot state "
                               f"{contact.properties['state']}."
                               f"\nWould you like to update the Hubspot value to {client.state}?"
                               f"Type 'y' for yes or 'n' for no.").lower()
                if answer == 'y':
                    print("Very well, updating state...")
                    try:
                        new_info = client.state
                        updated_info = SimplePublicObjectInput(
                            properties={
                                'state': new_info
                            }
                        )
                        api_client.crm.contacts.basic_api.update(
                            contact_id=contact_id,
                            simple_public_object_input=updated_info
                        )
                        print("State successfully updated. Moving to next property...")
                    except ApiException as e:
                        print(f"Skipping update, error: {e}")
        else:
            print(f"No state in Hubspot for {client.name}. Updating state...")
            try:
                new_info = client.state
                updated_info = SimplePublicObjectInput(
                    properties={
                        'state': new_info
                    }
                )
                api_client.crm.contacts.basic_api.update(
                    contact_id=contact_id,
                    simple_public_object_input=updated_info
                )
                print("State successfully updated. Moving to next property...")
            except ApiException as e:
                print(f"Skipping update, error: {e}")
    else:
        print(f"No state submitted for {client.name}. Moving to next property...")

    # LAST HOORAHH, UPDATING GROUPS!

    if client.group:
        if client.group in VALID_GROUPS:
            if client.group == 'Party Attendee' or client.group == 'Prospect':
                if contact.properties['facility_tour'] is not None:
                    try:
                        prosplist = contact.properties['facility_tour'].split(';')
                        if client.group in prosplist:
                            print(f"{client.group} already in {prosplist}. Moving on...")
                        else:
                            answer = input(f"{client.group} not found in {prosplist}.\nWould you like to append "
                                           f"{client.group} to the list? Type 'y' for yes or 'n' for no. ").lower()
                            if answer == 'y':
                                print(f"Very well, adding {client.group} to {prosplist}...")
                                try:
                                    new_info = contact.properties['facility_tour'] + f";{client.group}"
                                    updated_info = SimplePublicObjectInput(
                                        properties={
                                            'facility_tour': new_info
                                        }
                                    )
                                    api_client.crm.contacts.basic_api.update(
                                        contact_id=contact_id,
                                        simple_public_object_input=updated_info
                                    )
                                    print("Group successfully added. Moving on...")
                                except ApiException as e:
                                    print(f"Group not updated. Error: {e}")
                            else:
                                print("Very well, moving on...")
                    except AttributeError:
                        if client.group == contact.properties['facility_tour']:
                            print(f"{client.group} is equal to {contact.properties['facility_tour']}. Moving on...")
                        else:
                            answer = input(f"{client.group} is not equal to {contact.properties['facility_tour']}." 
                                           f"Would you like to append {client.group} to the list? "
                                           f"Type 'y' for yes or 'n' for no. ").lower()
                            if answer == 'y':
                                try:
                                    new_info = contact.properties['facility_tour'] + f";{client.group}"
                                    updated_info = SimplePublicObjectInput(
                                        properties={
                                            'facility_tour': new_info
                                        }
                                    )
                                    api_client.crm.contacts.basic_api.update(
                                        contact_id=contact_id,
                                        simple_public_object_input=updated_info
                                    )
                                    print("Group successfully added. Moving on...")
                                except ApiException as e:
                                    print(f"Group not updated. Error: {e}")
                            else:
                                print("Very well, moving on...")
                else:
                    print(f"The prospective property in Hubspot is empty for {client.name}. "
                          f"Adding {client.group} to the property...")
                    try:
                        new_info = client.group
                        updated_info = SimplePublicObjectInput(
                            properties={
                                'facility_tour': new_info
                            }
                        )
                        api_client.crm.contacts.basic_api.update(
                            contact_id=contact_id,
                            simple_public_object_input=updated_info
                        )
                        print("Group successfully added. Moving on...")
                    except ApiException as e:
                        print(f"Group not updated. Error: {e}")

            elif contact.properties['clinics_classes'] is not None:
                hubspotgroup = contact.properties['clinics_classes']
                try:
                    grouplist = hubspotgroup.split(";")
                    if client.group in grouplist:
                        print(f"For contact {client.name}, {client.group} is in Hubspot client group list: {grouplist}."
                              f"\nMoving on... ")
                    else:
                        answer = input(f"{client.group} is not in {grouplist}.\nWould you like to append "
                                       f"{client.group} to the list?\nType 'y' for yes or 'n' for no. ").lower()
                        if answer == 'y':
                            print("Very well, updating the group list...")
                            try:
                                new_info = contact.properties['clinics_classes'] + f";{client.group}"
                                updated_info = SimplePublicObjectInput(
                                    properties={
                                        'clinics_classes': new_info
                                    }
                                )
                                api_client.crm.contacts.basic_api.update(
                                    contact_id=contact_id,
                                    simple_public_object_input=updated_info
                                )
                                print("Group successfully updated. Moving to next property...")
                            except ApiException as e:
                                print(f"Skipping update. Error: {e}")
                        else:
                            print("Very well, moving to next property...")
                except AttributeError:
                    if client.group == contact.properties['clinics_classes']:
                        print(f"{client.group} matches {contact.properties['clinics_classes']}. Moving on...")
                    else:
                        answer = input(f"{client.group} does not match the Hubspot property value of "
                                       f"{contact.properties['clinics_classes']}.\nWould you like to append"
                                       f"{client.group} to {contact.properties['clinics_classes']}?\nType 'y' for yes"
                                       f"or 'n' for no. ").lower()
                        if answer == 'y':
                            print(f"Very well, appending {client.group} to {contact.properties['clinics_classes']}...")
                            try:
                                new_info = contact.properties['clinics_classes'] + f";{client.group}"
                                updated_info = SimplePublicObjectInput(
                                    properties={
                                        'clinics_classes': new_info
                                    }
                                )
                                api_client.crm.contacts.basic_api.update(
                                    contact_id=contact_id,
                                    simple_public_object_input=updated_info
                                )
                                print("Group successfully updated. Moving to next property...")
                            except ApiException as e:
                                print(f"Skipping update. Error: {e}")
                        else:
                            print("Very well, moving on...")
            else:
                print(f"No values entered in the Hubspot groups property for {client.name}. "
                      f"Adding {client.group} to property...")
                try:
                    new_info = client.group
                    updated_info = SimplePublicObjectInput(
                        properties={
                            'clinics_classes': new_info
                        }
                    )
                    api_client.crm.contacts.basic_api.update(
                        contact_id=contact_id,
                        simple_public_object_input=updated_info
                    )
                    print("Group successfully updated. Moving to next property...")
                except ApiException as e:
                    print(f"Skipping update. Error: {e}")
        else:
            print(f"Client group {client.group} unconfigured to be automatically added.\n"
                  f"Property must be configured interally in Python or added manually through Hubspot. \n"
                  f"Skipping group for now...")


# TODO: Make age check so client names are properly assigned if age >= 18 [COMPLETE]
def isadult(bday):
    dob = bday[-9:]
    dob = dob.split()
    dob = dob[1]
    if len(dob) == 3:
        dob = dob[0:2]
        dob = int(dob)
        if dob >= 18:
            return True
        else:
            return False
    else:
        return False


# TODO: Make func that translates "Group" values to internal Hubspot correlatives [COMPLETE]
def internalcode(group):
    if group == 'Junior Hoopers (Ages 4-6)':
        group = "2021Junior Hoopers"
        return group
    elif group == 'Robbinsville Coaches Training':
        group = "Robbinsville Coaches Clinic"
        return group
    elif group == "School's Out ID Hoops Lab":
        group = "Schools Out"
        return group
    elif group == 'Membership Info Form':
        group = "Prospect"
        return group
    elif "Birthday" in group.split(" ") and "Party" in group.split(" "):
        group = "Party Attendee"
        return group
    else:
        return group


# TODO: Make check for Sunday Skills Clinics & Weekday Clinics discrepancy [COMPLETE]
def infograbber(items):  # Creating function to handle email formatting discrepancies and create Client() objs
    for index, line in enumerate(items):
        line = line.rstrip()
        line = line[:6]
        if line == 'Group:':
            group = items[index]
            group = group[7:].strip()
            if group == 'ID Hoops Skills Programs' or group == 'Weekday Clinics':  # Reformatting for Sunday & Weekdays
                new_id = index - 3
                true_group = items[new_id]
                true_group = true_group.split()
                if 'Accelerator' in true_group:
                    group = '2021 Skills Accelerator'
                elif 'Fundamentals' in true_group:
                    group = '2021 Pure Fundamentals'
                elif 'Level' in true_group:
                    id = true_group.index('Level')
                    if true_group[id+1] == '1':
                        if true_group[id+2] == 'Shooting':
                            group = 'Level 1 Weekday Shooting & Dribbling'
                    elif true_group[id+1] == '2':
                        if true_group[id+2] == 'Shooting':
                            group = 'Level 2 Weekday Shooting & Dribbling'
            group = internalcode(group)
            name = items[index+1]
            name = name[9:].strip()
            formatting = name.split()  # Ensuring names are properly capitalized
            for str in formatting:
                str1 = str.capitalize()
                str1.strip()
                formatting[formatting.index(str)] = str1
            name = " ".join(formatting)
            address = items[index+2]
            address = address[9:]
            formatting = address.split()
            for str in formatting:  # Ensuring addresses are properly capitalized
                str1 = str.capitalize()
                str1.strip()
                formatting[formatting.index(str)] = str1
            address = " ".join(formatting)
            city = items[index+3]
            city = city[6:].capitalize()
            state = items[index+4]
            state = state[7:].upper()
            zip = items[index+5]
            zip = zip[5:]
            phone = items[index+9]
            phone = phone[12:].strip()
            email = items[index+10].lower()
            email = email[7:].strip()
            parent = items[index+12]
            parent = parent[24:]
            bday = items[index+15]
            bday = bday[15:]
            if isadult(bday):
                client = Contact(email=email, name=name, group=group, phone=phone, address=address,
                                 city=city, state=state, zip=zip, childname=" ", childdob=bday)
                adult_list.append(client)
                all_clients.append(client)
            if not isadult(bday):
                client = Contact(email=email, name=parent, group=group, phone=phone, address=address,
                                 city=city, state=state, zip=zip, childname=name, childdob=bday)
                child_list.append(client)
                all_clients.append(client)
        else:
            continue


# TODO: Create a class for each contact containing their contact info [COMPLETE]
@dataclass
class Contact:
    name: str
    email: str
    phone: str
    group: str
    childname: str
    childdob: str
    address: str
    city: str
    state: str
    zip: str


adult_list = []
child_list = []
all_clients = []

# Pick a date when the fetching should begin (1 week from present??)
date = datetime.datetime.now()
fetch_date = date - relativedelta(weeks=1)
fetch_date = fetch_date.strftime('%d-%b-%Y')

server = IMAPClient(host=HOST, port=PORT, use_uid=True)
server.login(username=USER, password=PASS)
server.select_folder(folder="INBOX")


# TODO: Fetch registration emails from roundcube in form of UIDs [COMPLETE]
messages = server.search(['Subject', 'A NEW ONLINE REGISTRATION HAS BEEN SUBMITTED', 'Since', fetch_date], 'UTF8')


# TODO: Loop through list of clients and create objects for each of them, adding said objects to a list [COMPLETE]
for message in messages:
    ct_msg = server.fetch([message], ['RFC822'])
    msg = email.message_from_bytes(ct_msg[message][b'RFC822'])
    if msg.get_content_type() == 'text/plain':
        # Looping through emails and contructing Contact() objects based on email contents
        body = msg.get_payload(decode=True).decode(msg.get_content_charset())
        body = body.split('\n')
        b_test = body[6].rstrip()
        infograbber(body)


# TODO Connect with Hubspot's API [COMPLETE], Ensure relevant properties are fetched [COMPLETE]
def contactmaker(all_clients):
    for client in all_clients:
        email = client.email    # The weird '.' return for some clients, despite having their emails in the DB,
        # was caused by whitespace in the email
        name = client.name.split()
        firstname = name[0] if len(name) > 0 else ""
        lastname = name[1] if len(name) > 1 else ""
        phone = client.phone

        filters = []
        if email:
            filters.append(Filter(property_name="email", operator="EQ", value=email))

        if filters:
            filter_group = FilterGroup(filters=filters)
            search_request = PublicObjectSearchRequest(  # 'properties' determines which fields are returned
                filter_groups=[filter_group],
                properties=['firstname', 'lastname', 'mobilephone', 'email', "kids_names", "kid_s_year_s_of_birth",
                            "clinics_classes", "facility_tour", "former_member", "address", "city", "state", "zip"]
                )

            try:
                response = api_client.crm.contacts.search_api.do_search(public_object_search_request=search_request)
                if response.results:
                    for contact in response.results:
                        if is_manual:
                            manual_mode(client, contact, firstname, lastname)
                        else:
                            print("Automatic mode under construction. Doing nothing!")
                else:
                    print(f"No contacts found for {email}.")
                    if is_manual:
                        answer = input(f"Would you like to create a new Hubspot contact for {client.email}?"
                                       f"\nType 'y' for yes or 'n' for no. ").lower()
                        if answer == 'y':
                            print(f"Creating Hubspot contact for {client.email}")
                            # make manual_mode() func for NEW clients
                        elif answer == 'n':
                            print(f"SKIPPING Hubspot contact creation for {client.email}")
                    else:
                        # automatic mode here
                        print("Automatic mode under construction. Doing nothing!")
            except ApiException as e:
                print(f"An error occurred while searching for {client.name}: {e}")
        else:
            print(f"No valid filters provided for {client.name}.")


contactmaker(all_clients)
# How do I compare and contrast properties?
