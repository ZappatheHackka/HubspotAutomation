import datetime
import os
from dateutil.relativedelta import relativedelta
import email.generator
from imapclient import IMAPClient
from dataclasses import dataclass
from hubspot import HubSpot
from hubspot.crm.contacts import ApiException, Filter, FilterGroup, PublicObjectSearchRequest, SimplePublicObjectInput

answer = input("Welcome to the Inner Drive Hoops Hubspot auto-registration program!\n"
               "Would you like to run in Manual Mode? (type 'y' for yes or 'n' for no)\n\n"
               "(Manual Mode requires a manual approval for completely NEW contacts to be created within Hubspot.\n"
               "If you decline, the script will run in Automatic Mode, and all new contacts will be automatically created.)\n").lower()

if answer == 'y':
    is_manual = True
    print("Running in Manual...")
elif answer == 'n':
    is_manual = False
    print("Running in automatic...")

# TODO: [COMPLETE] Authorize w/ Hubspot-They have a library!
HUBSPOT_ACCESS_TOKEN = os.environ['HUBSPOT_ACCESS_TOKEN']
HUBSPOT_SECRET = os.environ['HUBSPOT_SECRET']
USER = os.environ['WORK_EMAIL']
PASS = os.environ['WORK_PASS']
PORT = 993
HOST = "idhoops.com"


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
                        answer = input("Adult status is not listed in the Age property. Add Adult status? Type "
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
                                 city=city, state=state, zip=zip, childname="Adult", childdob=bday)
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
                        hubspotgroup = contact.properties['clinics_classes']
                        try:
                            grouplist = hubspotgroup.split(";")
                            if client.group in grouplist:
                                print(f"{client.group} is in {grouplist}")
                                print(f"{client.email} is tagged in the group {client.group} on Hubspot")
                        except AttributeError:
                            if client.group == hubspotgroup:
                                print(f"{client.group} matches {hubspotgroup}!")
                        else:
                            print(type(contact.properties['facility_tour']))
                else:
                    print(f"No contacts found for {email}.")
                    if is_manual:
                        answer = input(f"Would you like to create a new Hubspot contact for {client.email}?"
                                       f"\nType 'y' for yes or 'n' for no. ").lower()
                        if answer == 'y':
                            print(f"Creating Hubspot contact for {client.email}")
                        elif answer == 'n':
                            print(f"SKIPPING Hubspot contact creation for {client.email}")
                    else:
                        pass
            except ApiException as e:
                print(f"An error occurred while searching for {client.name}: {e}")
        else:
            print(f"No valid filters provided for {client.name}.")


# contactmaker(all_clients)
# How do I compare and contrast properties?
