import json
import csv
import requests

def download_member_flags():
    
    member_progress_url="https://docs.google.com/spreadsheets/d/19bFpL8zS8Zr22hPYOQgJ63c4MGtWFeF1J1AjauAbKxI/export?format=csv&gid=0"
    res=requests.get(url=member_progress_url)
    open('member-flags.csv', 'wb').write(res.content)

    data = {}

    with open('member-flags.csv', encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
    
        for rows in csvReader:

            key = rows['Name']
            data[key] = rows

    with open("member-flags.json", 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))
    
    print("Member flags synced from: " + member_progress_url)




def parse_attendance():

    member_flags_file = 'member-flags.json';
    member_flag_details = json.load(open(member_flags_file, 'r'))
    mains = member_flag_details.keys()

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

    main_attendees = list(set(mains) & set(attendees))
    #print("Main attendees: ")
    #print(main_attendees)
    #print('\n')

    main_attendees_flag_needed = []
    for main in main_attendees:
        flagged = member_flag_details[main][event]
        if flagged == "FALSE":
            main_attendees_flag_needed.append(main)

    print('\n')
    print("Main attendees who need " + event + " flag: ")
    print(main_attendees_flag_needed)
    print('\n')

    num_mains_flag_needed = len(main_attendees_flag_needed)
    print("Number of main attendees who need " + event + " flag: ")
    print(num_mains_flag_needed)
    print('\n')

    #num_mains = len(main_attendees_flag_needed)
    #print("Number of main attendees who need a flag: ")
    #print(num_mains)

    flags_remaining = 72 - num_mains_flag_needed
    print("Flags remaining for alts: ")
    print(flags_remaining)
    print('\n')

    missing_mains = list(set(mains).difference(attendees))
    missing_mains_flag_needed = []
    #print(missing_mains)
    
    missing_mains_no_buddy = []

    for main in missing_mains:
        flagged = member_flag_details[main][event]
        if flagged == "FALSE":
            missing_mains_flag_needed.append(main)

    print("Missing mains who need  " + event + " flag: ")
    print(missing_mains_flag_needed)
    print('\n')

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
            print("Main: " + main)
            print("Flag buddies: " + flag_buddies)
            print('\n')
        else:
            missing_mains_no_buddy.append(main)

    print("Missing mains with no flag buddies in attendance: ")
    print(', '.join(missing_mains_no_buddy))




def cleanup():
    #TODO: delete .csv and .json files created for the script
    return True

   
download_member_flags()
parse_attendance()
cleanup()


