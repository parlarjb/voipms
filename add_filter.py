from voipms import Voipms

def load_accounts(credentials_file):
    accounts = []
    with open(credentials_file) as f:
        for line in f:
            username, password, ivr = [x.strip() for x in line.split(",")]
            accounts.append(Voipms(username, password, ivr))
    return accounts

def update_filters(accounts, callerid, action, note):
    '''
    Assumes that each Voipms instance in 'accounts' has already been connected
    '''
    for a in accounts:
        a.connect()
        if action == "hangup":
            routing = u"sys:hangup"
        elif action == "ivr":
            routing = u"ivr:" + a.ivr
        print a.create_callerid_filter(callerid, routing, note=note)


if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    callerid = sys.argv[2]
    action = sys.argv[3] # either 'hangup' or 'ivr'
    note = ""
    if len(sys.argv) == 5:
        note = sys.argv[4]

    accounts = load_accounts(filename)
    for a in accounts:
        a.connect()
    update_filters(accounts, callerid, action, note)


