import re
import json

data = open("data.txt", "r")
lines = data.readlines()

valid_eye = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
passport = {}
valid = 0

for line in lines:
    if line == "\n":
        if len(passport) == 8 or (len(passport) == 7 and not "cid" in passport):
            passes = True

            byr = int(passport["byr"])
            if byr < 1920 or byr > 2002:
                #print("failbyr", byr)
                passes = False

            iyr = int(passport["iyr"])
            if iyr < 2010 or iyr > 2020:
                #print("failiyr", iyr)
                passes = False
            
            eyr = int(passport["eyr"])
            if eyr < 2020 or eyr > 2030:
                #print("faileyr", eyr)
                passes = False

            hgt = passport["hgt"]
            m = re.search('^(\d+)cm$', hgt)
            if m == None:
                m = re.search('^(\d+)in$', hgt)
                if m == None:
                    #print("failhgt1", hgt)
                    passes = False
                else:
                    height = int(m.group(1))
                    if height < 59 or height > 76:
                        #print("failhgt2", hgt)
                        passes = False
            else:
                height = int(m.group(1))
                if height < 150 or height > 193:
                    #print("failhgt3", hgt)
                    passes = False

            hcl = passport["hcl"]
            m = re.search('^#[0-9a-f]{6}$', hcl)
            if m == None:
                #print("failhcl", hcl)
                passes = False

            ecl = passport["ecl"]
            if not ecl in valid_eye:
                #print("failecl", ecl)
                passes = False

            m = re.search('^[0-9]{9}$', passport["pid"])
            if m == None:
                print("failpid", passport["pid"])
                passes = False

            if passes:
                valid = valid + 1
                #print("pass: ", passport)
            else:
                print(json.dumps(passport, indent=4, sort_keys=True))

        passport = {}

        continue

    s = line.split()
    for i in s:
        d = i.split(":")
        passport[d[0]] = d[1]

print(valid, " valid passports")


