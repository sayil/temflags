import json
  
def parse_attendance():

    characters_file = 'characters_file.json' #characters_file must be in the same folder as this script
    characters_file_pointer = open(characters_file, 'r')

    characters = json.load(characters_file_pointer)
    #print(characters)
    
    mains = characters["mains"].keys()
    print(mains)

    attendees = []
    print("Paste attendees here: ")
    while True:
        line = input()

        if line:
            attendee = line.split("]")[2].strip().split(" ")[0].strip()
            attendees.append(attendee)
        else:
            break

    print("Attendees: ")
    print(attendees)

    main_attendees = list(set(mains) & set(attendees))
    print("Main attendees: ")
    print(main_attendees)

    num_mains = len(main_attendees)
    print("Number of main attendees: ")
    print(num_mains)

    flags_remaining = 72 - num_mains
    print("Flags remaining for alts: ")
    print(flags_remaining)

    missing_mains = list(set(mains).difference(attendees))
    print("Missing mains: ")
    print(missing_mains)

    for main in missing_mains:
        print("Main: " + main)
        flag_buddies = ", ".join(characters["mains"][main]["buddies"])
        print("Flag buddies: " + flag_buddies)

    

   

parse_attendance()

