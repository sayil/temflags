import json
import csv
import requests

pop_flags_url="https://docs.google.com/spreadsheets/d/19bFpL8zS8Zr22hPYOQgJ63c4MGtWFeF1J1AjauAbKxI"

def download_member_flags():
    
    export_details = "/export?format=csv&gid=0"
    member_progress_url=pop_flags_url + export_details
    res=requests.get(url=member_progress_url)
    open('member-flags.csv', 'wb').write(res.content)

    data = {}

    with open('member-flags.csv', encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
    
        for row in csvReader:
            key = row['Name']
            data[key] = row

    with open("member-flags.json", 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))
    
    print("Member flags synced from: " + pop_flags_url + " using " + export_details)


def download_all_mains():
    
    export_details = "/export?format=csv&gid=1536719939"
    all_mains_url=pop_flags_url + export_details
    res=requests.get(url=all_mains_url)
    open('all-mains.csv', 'wb').write(res.content)

    data = {}

    with open('all-mains.csv', encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        for row in csvReader:
            key = row['Name']
            data[key] = row

    with open("all-mains.json", 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))




def parse_attendance():

    member_flags_file = 'member-flags.json';
    member_flag_details = json.load(open(member_flags_file, 'r'))
    mains = member_flag_details.keys()

    all_mains_file = 'all-mains.json';
    all_mains = json.load(open(all_mains_file, 'r')).keys()

    flag_events = member_flag_details['Taelor'].keys()
    event = ""

    attendees = []
    print("Paste attendees here: ")
    while True:
    #while line not in flag_events:
        line = input()

        if line:

            if line in flag_events:
                event = line
                break

            attendee = line.split("]")[2].strip().split(" ")[0].strip()
            attendees.append(attendee)

        else:
            break

    #print("Attendees: ")
    #print(attendees)
    #print('\n')

    undocumented_main_attendees = list((set(attendees) & set(all_mains)).difference(mains))

    print('\n')
    print("These mains are in attendance but do not have an entry in the PoP flag tracker: ")
    print(', '.join(sorted(undocumented_main_attendees)))
    print('\n')

    main_attendees = list(set(mains) & set(attendees))
    #print("Main attendees: ")
    #print(main_attendees)
    #print('\n')

    main_attendees_flag_needed = []
    for main in main_attendees:
        flagged = member_flag_details[main][event]
        if flagged == "FALSE":
            main_attendees_flag_needed.append(main)

    num_mains_flag_needed = len(main_attendees_flag_needed)

    print(str(num_mains_flag_needed) + " main attendees who need " + event + " flag: ")
    print(', '.join(sorted(main_attendees_flag_needed)))
    print('\n')

    #num_mains = len(main_attendees_flag_needed)
    #print("Number of main attendees who need a flag: ")
    #print(num_mains)

    missing_mains = sorted(list(set(mains).difference(attendees)))
  
    missing_mains_flag_needed = []
    #print(missing_mains)
    
    missing_mains_no_buddy = []

    for main in missing_mains:
        flagged = member_flag_details[main][event]
        if flagged == "FALSE":
            missing_mains_flag_needed.append(main)



    #print("Missing mains who need  " + event + " flag: ")
    #print(missing_mains_flag_needed)
    #print('\n')

    print('-----------------------------------------------------------------------')
    print('\n')
    print("Missing mains with a buddy in attendance who need  " + event + " flag: ")
    print('\n')

    num_missing_mains_with_buddy = 0
    for main in missing_mains_flag_needed:

        flag_buddies = [] 

        flag_buddy = member_flag_details[main]['Flag buddy #1']
        if(len(flag_buddy)> 0 and (flag_buddy in attendees)):
            flag_buddies.append(flag_buddy)

        flag_buddy = member_flag_details[main]['#2']
        if(len(flag_buddy)> 0 and (flag_buddy in attendees)):
            flag_buddies.append(flag_buddy)

        flag_buddy = member_flag_details[main]['#3']
        if(len(flag_buddy)> 0 and (flag_buddy in attendees)):
            flag_buddies.append(flag_buddy)
        
        flag_buddies = ", ".join(flag_buddies)


        if(len(flag_buddies) > 0):
            num_missing_mains_with_buddy += 1
            print(str(num_missing_mains_with_buddy) + ". " + main)
            print("Flag buddies: " + flag_buddies)
            print('\n')
        else:
            missing_mains_no_buddy.append(main)

    print('-----------------------------------------------------------------------')
    print('\n')
    #num_mains_flag_needed = len(main_attendees_flag_needed)
    #print("Number of main attendees who need " + event + " flag: ")
    #print(num_mains_flag_needed)
    #print('\n')

    print("Number of main attendees who need " + event + " flag: " + str(num_mains_flag_needed))
    print("Missing mains with a flag buddy in attendance: " + str(num_missing_mains_with_buddy))

    flags_remaining = 72 - num_mains_flag_needed - num_missing_mains_with_buddy
    print("Flags remaining for alts: " + str(flags_remaining))
    print('\n')

    print("Missing mains with no flag buddies in attendance: " + str(len(missing_mains_no_buddy)))
    print(', '.join(missing_mains_no_buddy))
    print('\n')




def cleanup():
    #TODO: delete .csv and .json files created for the script
    return True

   
download_member_flags()
download_all_mains()
parse_attendance()
cleanup()
