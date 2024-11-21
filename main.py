import datetime
import os
from dateutil.relativedelta import relativedelta
import email.generator
from imapclient import IMAPClient
from dataclasses import dataclass
from hubspot import HubSpot
from hubspot.crm.contacts import ApiException, Filter, FilterGroup, PublicObjectSearchRequest

# TODO: [COMPLETE] Authorize w/ Hubspot-They have a library!
HUBSPOT_ACCESS_TOKEN = os.environ['HUBSPOT_ACCESS_TOKEN']
HUBSPOT_SECRET = os.environ['HUBSPOT_SECRET']
USER = os.environ['WORK_EMAIL']
PASS = os.environ['WORK_PASS']
PORT = 993
HOST = "idhoops.com"


"""Clinics & Classes is stored internally in hubspot under clinics_classes"""

api_client = HubSpot(access_token=HUBSPOT_ACCESS_TOKEN)


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

# TODO: Make func that translates "Group" values to internal Hubspot correlatives


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
            name = name[9:]
            address = items[index+2]
            address = address[9:]
            city = items[index+3]
            city = city[6:]
            state = items[index+4]
            state = state[7:]
            zip = items[index+5]
            zip = zip[5:]
            phone = items[index+9]
            phone = phone[12:].strip()
            email = items[index+10]
            email = email[7:].strip()
            parent = items[index+12]
            parent = parent[24:]
            bday = items[index+15]
            bday = bday[15:]
            print(group)
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


# TODO Connect with Hubspot's API [COMPLETE], Ensure relevant properties are fetched
new_clients = []

# for client in all_clients:
#     email = client.email    # The weird '.' return for some clients, despite having their emails in the DB,
#     # was caused by whitespace in the email
#     name = client.name.split()
#     firstname = name[0] if len(name) > 0 else ""
#     lastname = name[1] if len(name) > 1 else ""
#     phone = client.phone
#
#     filters = []
#     if email:
#         filters.append(Filter(property_name="email", operator="EQ", value=email))
#
#     if filters:
#         filter_group = FilterGroup(filters=filters)
#         search_request = PublicObjectSearchRequest(  # 'properties' determines which fields are returned
#             filter_groups=[filter_group],
#             properties=['firstname', 'lastname', 'mobilephone', 'email', "kid_s_year_s_of_birth",
#                         "clinics_classes", "facility_tour", "address", "city", "state", "zip"]
#             )
#
#         try:
#             response = api_client.crm.contacts.search_api.do_search(public_object_search_request=search_request)
#
#             # print(response)  # Debugging: print the entire response to check for issues
#
#             if response.results:
#                 for contact in response.results:
#                     print(contact.properties)
#                     # firstname = contact.properties.get('firstname', 'No firstname')
#                     # lastname = contact.properties.get('lastname', 'No lastname')
#                     # phone = contact.properties.get('mobilephone', 'No phone')
#                     #
#                     # print(f"Contact ID: {contact.id}, Email: {contact.properties.get('email')}, "
#                     #       f"Name: {firstname} {lastname}, Phone: {phone}")
#             else:
#                 print(f"No contacts found for {email}.")
#                 new_clients.append(client)
#         except ApiException as e:
#             print(f"An error occurred while searching for {client.name}: {e}")
#     else:
#         print(f"No valid filters provided for {client.name}.")


# How do I compare and contrast properties?
