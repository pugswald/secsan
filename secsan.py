import getpass
import json
import random
import smtplib
import sys

def generate_pairings(participants, exclusions, depth):
    """Pair all participants using a brute force randomizer
    """
    if depth > 10:
        raise Exception("Failed after 10 attempts")
    sfrom = list(participants)
    sto = list(participants)
    pairings = []
    if len(sfrom) < 2:
        raise Exception("Need at least 2 participants")
    while len(sfrom) > 0:
        p_from = random.choice(sfrom)
        p_to = random.choice(sto)
        #print(p_from)
        if p_to == p_from:
            if len(sfrom) == 1:
                # Try again
                print "Ended poorly in match, trying again"
                return generate_pairings(participants, exclusions, depth+1)
            continue
        failed_exclusion = False
        for exclusion in exclusions:
            #print("Testing for exclusion "+p_from+" "+p_to)
            #print(exclusion)
            if p_from in exclusion and p_to in exclusion:
                print "Ended poorly in exclusion, trying again"
                return generate_pairings(participants, exclusions, depth+1)
        pairings.append([p_from, p_to])
        sfrom.remove(p_from)
        sto.remove(p_to)
    return pairings


def main(raw_participants):
    participants = {}
    exclusions = []
    for entry in raw_participants:
        if type(entry[0]) == list:
            couple = []
            for (p, e) in entry:
                couple.append(p)
                participants[p] = e
            exclusions.append(couple)
        else:
            participants[entry[0]] = entry[1]
    pairings = generate_pairings(participants.keys(), exclusions, 0)
    print pairings
    body = """Dear %s, \n\nYour secret santa this year is %s.\n
Do not hit reply, as I don't want to know your secret santa.
If there is a problem with this assignment please email me.\n
Regards,\nThe Secret Santa Generator
https://github.com/pugswald/secsan"""
    uname = getpass.getpass("Gmail username: ")
    pwd = getpass.getpass("Gmail password: ")
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.ehlo()
    s.login(uname, pwd)
    for (p_from, p_to) in pairings:
        if participants[p_from] != "":
            print "Send email to "+p_from+" that his secret santa is "+p_to
            msg = """\From: %s\nTo: %s\nSubject: Your secret santa\n\n%s
            """ % (uname, participants[p_from], body%(p_from, p_to))
            s.sendmail(uname, participants[p_from], msg)
    s.close()


if __name__ == "__main__":
    main(json.load(open(sys.argv[1])))
