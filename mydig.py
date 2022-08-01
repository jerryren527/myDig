import sys
import time
import datetime
import dns
import dns.name
import dns.query

def mydig(domain, where, timer):
    domain = str(domain)
    
    qname = dns.name.from_text(domain)
    if domain.startswith('www.'):
        domain = domain[4:]

    dns_start = time.perf_counter() # timer start
    q = dns.message.make_query(qname, dns.rdatatype.A) # query
    dns_end = time.perf_counter() # timer end
    timer = timer + ((dns_end - dns_start) * 1000) # time in msec


    where = str(where)
    dns_start = time.perf_counter() # timer start
    r = dns.query.udp(q, where) # response
    
    dns_end = time.perf_counter() # timer end
    timer = timer + ((dns_end - dns_start) * 1000)

    rToString = str(r) # turn response to string for parsing

    # parsing Answer section
    answer_position = rToString.find("ANSWER")
    answer = rToString[answer_position:]
    answer = answer.split('\n')

    # parsing Additional section
    additional_position = rToString.find(";ADDITIONAL")
    additional = rToString[additional_position:]
    additional = additional.split('\n')

    first_answer = answer[1]

    additional.pop(0) # remove first element in additional section

    if first_answer[-1].isdigit(): # looks at Answer section
        answer.remove('ANSWER')
        print("QUESTION SECTION:")
        print("%s        IN A" % str(sys.argv[1]))
        print("ANSWER SECTION:")
        cutoff_position = first_answer.find(" ")
        first_answer = first_answer[cutoff_position:]
        print("{} {}".format(str(sys.argv[1]),first_answer))
        timer = float(timer)
        print("Query time: %.2f ms" % timer)
        print("WHEN: %s" % str(datetime.datetime.now()))
    elif "CNAME" in first_answer: # if Answer has a CNAME, return it
        answer.remove('ANSWER')
        print("QUESTION SECTION:")
        print("%s        IN A" % str(sys.argv[1]))
        print("ANSWER SECTION:")
        print(first_answer)
        timer = float(timer)
        print("Query time: %.2f ms" % timer)
        print("WHEN: %s" % str(datetime.datetime.now()))
    elif additional != []: # looks at Additional section
        additional_position= rToString.find("ADDITIONAL")
        additional = rToString[additional_position:]
        additional_list = additional.split(" A ")
        firstIP= additional_list[1].split('\n')
        firstIP = firstIP[0]
        mydig(domain,firstIP,timer)
    else: # looks at Authority section
        authority_position = rToString.find("AUTHORITY")
        authority = rToString[authority_position:]
        if " SOA " in authority:
            authority_list = authority.split(" SOA ")
            authority_list.pop(0)
            # find position of ".com" + 1
            first_authoritative_NS = authority_list[0]
            authoritative_NS_position = first_authoritative_NS.find(".com")
            authoritative_NS = first_authoritative_NS[:authoritative_NS_position + 4]
        elif " NS " in authority:
            authority_list = authority.split(" NS ")
            authority_list.pop(0)

            first_authoritative_NS = authority_list[0]
            
            if ".com" in first_authoritative_NS:
                authoritative_NS_position = first_authoritative_NS.find(".com")
                authoritative_NS = first_authoritative_NS[:authoritative_NS_position + 4]
            if ".net" in first_authoritative_NS:
                authoritative_NS_position = first_authoritative_NS.find(".net")
                authoritative_NS = first_authoritative_NS[:authoritative_NS_position + 4]
            if ".org" in first_authoritative_NS:
                authoritative_NS_position = first_authoritative_NS.find(".org")
                authoritative_NS = first_authoritative_NS[:authoritative_NS_position + 4]
            if ".gov" in first_authoritative_NS:
                authoritative_NS_position = first_authoritative_NS.find(".gov")
                authoritative_NS = first_authoritative_NS[:authoritative_NS_position + 4]
            if ".edu" in first_authoritative_NS:
                authoritative_NS_position = first_authoritative_NS.find(".edu")
                authoritative_NS = first_authoritative_NS[:authoritative_NS_position + 4]
            if ".cn" in first_authoritative_NS:
                authoritative_NS_position = first_authoritative_NS.find(".cn")
                authoritative_NS = first_authoritative_NS[:authoritative_NS_position + 3]
            if ".uk" in first_authoritative_NS:
                authoritative_NS_position = first_authoritative_NS.find(".uk")
                authoritative_NS = first_authoritative_NS[:authoritative_NS_position + 3]

        mydig(authoritative_NS,where,timer)


def run_mydig(timer):
    mydig(sys.argv[1], sys.argv[2], timer)

run_mydig(0)