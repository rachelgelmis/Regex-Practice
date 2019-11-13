# CS 390 Program 1
# October 26th, 2019
# Rachel Gelmis

import re                                   # import regular expression operations
from collections import Counter

#regular expressions
r_get = re.compile(r'GET\s+(\S+)',re.A)       # takes a regex pattern and turns into regex object
r_ips = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',re.A)
#r_staff = re.compile(r'(\/\~|)',re.A)
r_bots = re.compile(r'/robots\.txt.*;\s+(\D+[B,b]ot/\d+.\d+)', re.A)
r_days = re.compile(r'(\d{2,3}/\D{2,3}/\d{2,3})', re.A)
r_error = re.compile(r'([A-Z][a-z]{2}\s[A-Z][a-z]{2,3}\s\d+)', re.A)
r_denied = re.compile(r'Permission denied:\s+', re.A)
r_deniedstaff = re.compile(r'Permission denied:\s+.*CS/([^/]+)', re.A)
r_pid = re.compile(r'pid\s+(\d+)', re.A)

#open and read files
access = open('access.log').readlines()
error = open('error.log').readlines()

#variables for access.log
gets_count = 0
staff_count = Counter()                                
nonstaff_count = 0
ips = Counter()
requests = Counter()
#staff = Counter()
requests = Counter()
bots = Counter()
robotrequests = 0

#variables for error.log
denied = 0
deniedstaff = 0
ipError = Counter()
staffdeny = Counter()
pidcount = Counter()
accessdays = Counter()
errordays = Counter()

#access.log parsing
for line in access:    
    # parse GET requests    
    parseGET = re.search(r_get,line)              # search for the GET regex object 
    if parseGET:        
        gets_count += 1                    # if the object is found, increment the num_gets counter  
        requests[parseGET.group(1)] +=1
        if "/~" in parseGET.group(1):
            arr = parseGET.group(1).split("/")
            if len (arr) > 1:
                staff = arr[1][1:]
                staff_count[staff] += 1
        else:
           arr = parseGET.group().split("/")
           if len(arr) > 1:
              nonstaff = arr[1][1:]
              nonstaff_count += 1
        parseBot = re.search(r_bots, line)
        if parseBot:
            bots[parseBot.group(1)] += 1
        #botIndex = re.search(r_bots, line)
        #if botIndex:
            #bots[botIndex.group(1)] += 1
        parseDays = re.search(r_days, line)
        if parseDays:
            accessdays[parseDays.group(0)] += 1
        parseIP = re.search(r_ips,line)          # search for the IP regex object
        #parseStaff = re.search(r_staff,line)
        if parseIP:                              # if the object is found, 
            ips[parseIP.group(1)] += 1
        #parseStaff = re.search(r_staff,line)
        #if parseStaff:
            #staff[parseStaff.group(1)] +=1

#error.log parsing
for line in error:
    perm_denied = re.search(r_denied, line)
    staff_denied = re.search(r_deniedstaff, line)
    if perm_denied:
        denied += 1
    if staff_denied:
        staffdeny[staff_denied.group(1)] += 1
    parseIP = re.search(r_ips, line)
    if parseIP:
        ipError[parseIP.group(1)] += 1
    parsePID = re.search(r_pid, line)
    if parsePID:
        pidcount[parsePID.group(0)] += 1
    parseError = re.search(r_error, line)
    if parseError:
        errordays[parseError.group(0)] += 1

    errorFreq = ((denied)/(denied+gets_count) * 100)   

#print output
print("GET requests: {}".format(gets_count))
print("Total unique IP addresses: {}".format(len(ips)))
print("Most common IP: {} which is seen {} times".format(Counter(ips).most_common(1)[0][0],(Counter(ips).most_common(1)[0][1])))
print("{} GET requests were for faculty/staff pages".format(staff_count[staff]))
print("{} was the most popular staff member with {} requests".format(staff_count.most_common(1)[0][0], staff_count.most_common(1)[0][1]))
print("The 3 most popular resources were:")
print("REQUESTS:    RESOURCE:")
for res in range(0,3):
    print("{:>7}       {}".format(requests.most_common(3)[res][1], requests.most_common(3)[res][0]))
print("The most popular non-staff resource was [/f{}]".format(nonstaff))
print("There were {} requests for robots.txt".format(robotrequests))
print("There were {} bots that indexed the site".format(len(bots)))
print("The 3 most active bots were:")
print("BOT               VER          REQUESTS")
print("{}          {}          {}".format(bots.most_common(3)[0][0].split('/')[0], bots.most_common(3)[0][0].split('/')[1], bots.most_common(3)[0][1]))
print("{}             {}          {}".format(bots.most_common(3)[1][0].split('/')[0], bots.most_common(3)[1][0].split('/')[1], bots.most_common(3)[1][1]))
print("{}          {}          {}".format(bots.most_common(3)[2][0].split('/')[0], bots.most_common(3)[2][0].split('/')[1], bots.most_common(3)[2][1]))
print("There were {} permission denied errors".format(denied))
print("There were {} staff who had permission denied errors on their content".format(len(staffdeny)))
print("The staff member with the most permission denied errors was {} with {} errors".format(staffdeny.most_common(1)[0][0],staffdeny.most_common(1)[0][1]))
print("There were {} IP addresses with errors".format(len(ipError)))
print("The IP address with the most errors was {} with {} errors".format(ipError.most_common(1)[0][0], ipError.most_common(1)[0][1]))
print("There were {} unique process IDs in the error log".format(len(pidcount)))
print("{} showed up as the process ID with the most errors".format(pidcount.most_common(1)[0][0]))
print("There was a {0:.3f} % frequency of errors".format(errorFreq))
print("The access.log file covered {} days".format(len(accessdays)))
for days in accessdays:
    print("{}:  {} accesses".format(days, accessdays[days]))
print("The error.log file covered {} days".format(len(errordays)))
for days in errordays:
    print("{}{}/{}{}{}/2018:  {} accesses".format(days[8], days[9],days[4], days[5], days[6], errordays[days]))