from voipms import Voipms

def get_existing_filters(voipms_connection):
    raw_filters = voipms_connection.get_callerid_filtering()
    return raw_filters[u'filtering']


def build_and_connect(user, password):
    voip = Voipms(user, password)
    voip.connect()
    return voip

def map_routing(routing, ivr):
    retval = routing
    if u'ivr' in routing:
        retval = u'ivr:' + ivr
    return retval

def create_filters(existing_filters, new_voip, ivr):
    for cid_filter in existing_filters:
        callerid = cid_filter[u'callerid']
        note = cid_filter[u'note']
        routing = map_routing(cid_filter[u'routing'], ivr)

        print "Creating filter for", callerid
        print new_voip.create_callerid_filter(callerid, routing, "all", note)

if __name__ == "__main__":
    import sys
    original_account_user = sys.argv[1]
    original_account_pass = sys.argv[2]
    new_account_user = sys.argv[3]
    new_account_pass = sys.argv[4]

    ivr = sys.argv[5]

    original_voip = build_and_connect(original_account_user, original_account_pass)
    new_voip = build_and_connect(new_account_user, new_account_pass)

    create_filters( get_existing_filters(original_voip), new_voip, ivr)


