import _sctp
import sctp
from sctp import *
import time

client = "127.0.0.1"
server = "127.0.0.1"
test_impossible_sending = False

if _sctp.getconstant("IPPROTO_SCTP") != 132:
    raise print ( "getconstant failed")
tcp = sctpsocket_tcp(socket.AF_INET)
udp = sctpsocket_udp(socket.AF_INET)
tcp2 = sctpsocket_tcp(socket.AF_INET, socket.socket(socket.AF_INET, socket.SOCK_STREAM, IPPROTO_SCTP))
udp2 = sctpsocket_udp(socket.AF_INET, socket.socket(socket.AF_INET, socket.SOCK_SEQPACKET, IPPROTO_SCTP))
print ("Implementation features: 0x0%x" % features())
try:
    tcp.peeloff(1)
    raise print ( "Should not have worked (TCP socket)!")
except IOError:
    pass

try:
    udp.peeloff(1)
    raise print ( "Should not have worked (No connections && invalid association ID)!")
except IOError:
    pass

print ("Initparam is", udp.initparams)
print ("Initparam.max_instreams is, by default,", udp.initparams.max_instreams)

udp.initparams.max_instreams = 77

if udp.initparams.max_instreams != 77:
    raise print ( "initparams.max_instreams is not the value I just set!")
if _sctp.get_initparams(udp.fileno())["_max_instreams"] != 77:
    raise print ( "initparams.max_instreams is not the value I just set! (2)")

p = udp.initparams.autoflush = False
p = udp.initparams.max_instreams = 78

if udp.initparams.max_instreams != 78:
    raise print ( "initparams.max_instreams is not the value I just set!")
if _sctp.get_initparams(udp.fileno())["_max_instreams"] != 77:
    raise print ( "subjacent max_instreams is not the value I set before!")

print ("Default of properties: NODELAY=%d, MAPPEDV4=%d, MAXSEG=%d" % (tcp.nodelay, tcp.mappedv4, tcp.maxseg))

tcp.nodelay = \
    tcp.disable_fragments = \
    tcp.mappedv4 = 0

tcp.maxseg = 10001
tcp.adaptation = 318

if _sctp.get_nodelay(tcp.fileno()) or \
        _sctp.get_disable_fragments(tcp.fileno()) or \
        _sctp.get_maxseg(tcp.fileno()) != 10001 or \
        _sctp.get_adaptation(tcp.fileno()) != 318 or \
        _sctp.get_mappedv4(tcp.fileno()):
    raise print ( "Property attribution was not effective")

tcp.nodelay = \
    tcp.disable_fragments = \
    tcp.mappedv4 = 1

if not _sctp.get_nodelay(tcp.fileno()) or \
        not _sctp.get_disable_fragments(tcp.fileno()) or \
        not _sctp.get_mappedv4(tcp.fileno()):
    raise print ( "Property attribution was not effective")

udp.autoclose = 0
if _sctp.get_autoclose(udp.fileno()):
    raise print ( "autoclose property was not effective")

udp.autoclose = 1
if not _sctp.get_autoclose(udp.fileno()):
    raise print ( "autoclose property was not effective")

for s in (tcp, udp, tcp2, udp2):
    s.events.clear()
    rawparams = _sctp.get_events(s.fileno())

    if not rawparams["_data_io"] or \
            rawparams["_association"] or \
            rawparams["_address"] or \
            rawparams["_send_failure"] or \
            rawparams["_peer_error"] or \
            rawparams["_shutdown"] or \
            rawparams["_partial_delivery"] or \
            rawparams["_adaptation_layer"]:
        raise print ( "events properties were not effective (in 0)")

    s.events.data_io = True
    s.events.association = True
    s.events.address = True
    s.events.send_failure = True
    s.events.peer_error = True
    s.events.shutdown = True
    s.events.partial_delivery = True
    s.events.adaptation_layer = True

    rawparams = _sctp.get_events(s.fileno())

    if not rawparams["_data_io"] or \
            not rawparams["_association"] or \
            not rawparams["_address"] or \
            not rawparams["_send_failure"] or \
            not rawparams["_peer_error"] or \
            not rawparams["_shutdown"] or \
            not rawparams["_partial_delivery"] or \
            not rawparams["_adaptation_layer"]:
        raise print ( "events properties were not effective (in 1)")

    s.events.data_io = False
    s.events.association = False
    s.events.address = False
    s.events.send_failure = False
    s.events.peer_error = False
    s.events.shutdown = False
    s.events.partial_delivery = False
    s.events.adaptation_layer = False

    rawparams = _sctp.get_events(s.fileno())

    if rawparams["_data_io"] or \
            rawparams["_association"] or \
            rawparams["_address"] or \
            rawparams["_send_failure"] or \
            rawparams["_peer_error"] or \
            rawparams["_shutdown"] or \
            rawparams["_partial_delivery"] or \
            rawparams["_adaptation_layer"]:
        raise print ( "events properties were not effective (in 0)")

ipv4 = _sctp._sockaddr_test(("10.0.1.1", 1234))
ipv6 = _sctp._sockaddr_test(("FE80::0:0:34", 65534))

if ipv4[3] != ("10.0.1.1", 1234):
    print (ipv4)
    raise print ( "Sockaddr conversion went wrong")

if ipv6[3] != ("fe80::34", 65534):
    print (ipv6)
    raise print ( "Sockaddr conversion went wrong")

try:
    _sctp._sockaddr_test(("fe:80:88:34:34:34", 1234))
    _sctp._sockaddr_test(("10.0.1", 1234))
    _sctp._sockaddr_test(("10.0.1.1", 2349238234))
    raise print ( "sockaddr_test throwed invalid addresses!")
except ValueError:
    pass

if test_impossible_sending:
    udp.sctp_send("bla", to=("1.2.3.4", 0x1415), flags=MSG_UNORDERED, timetolive=10000, context=741)
    lastnotif = None
    while True:
        try:
            (fromaddr, flags, msg, notif) = udp.sctp_recv(10000)
            print ("Received: fromaddr=%s:%d" % fromaddr)
            print ("flags=%d, msg=\'%s\'" % (flags, msg))
            print ("notif=", notif)
            if msg is None:
                lastnotif = notif
                print ("Conte??do da notif: ", notif.__dict__)
        except IOError:
            print ("Recebido IOError (esperado)")
            break

tcp.close()
udp.close()
tcp2.close()
udp2.close()

baseport = 0x1415

udp = sctpsocket_udp(socket.AF_INET)
udp.autoclose = 60
udp.initparams.max_instreams = 3
udp.initparams.num_ostreams = 3
udp.events.clear()
udp.events.data_io = 1
udp.events.association = 1

udp.bindx([(client, baseport + 1000)])

for i in [0, 1, 2, 3, 4, 5]:
    msg = "tcp %d" % (baseport + i)

    saddr = (server, baseport + i)

    print ("TCP ", saddr, " ----------------------------------------------")
    tcp = sctpsocket_tcp(socket.AF_INET)

    tcp.initparams.max_instreams = 3
    tcp.initparams.num_ostreams = 3

    tcp.events.clear()
    tcp.events.data_io = 1

    expected_ret = "#" + msg
    tcp.connect(saddr)

    paddrs = tcp.getpaddrs()
    laddrs = tcp.getladdrs()

    print ("tcp paddrs: ", paddrs)
    print ("tcp laddrs: ", laddrs)

    try:
        tcp.set_primary(0, saddr)
        tcp.set_peer_primary(0, (client, laddrs[0][1]))
    except IOError:
        raise print ( "set_primary or set_peer_primary failed: /proc/sys/net/sctp/addip_enable is probably 0")

    x = tcp.get_rtoinfo(0)
    if not x.max:
        raise print ( "get_rtoinfo() did not work")
    x.max = 33333
    print ("rtoinfo:", x.__dict__)
    tcp.set_rtoinfo(x)
    if tcp.get_rtoinfo(0).max != 33333:
        raise print ( "set_rtoinfo() did not work for TCP socket")

    x = udp.get_rtoinfo(0)
    if not x.max:
        raise print ( "get_rtoinfo() did not work")

    x.max = 33334
    print ("rtoinfo:", x.__dict__)
    udp.set_rtoinfo(x)
    if udp.get_rtoinfo(0).max != 33334:
        raise print ( "set_rtoinfo(zero) did not work for UDP socket")

    x = udp.get_assocparams(0)
    if not x.cookie_life:
        raise print ( " get_assocparams() did not work")
    print ("assocparams:", x.__dict__)
    x.cookie_life = 334
    udp.set_assocparams(x)
    x = udp.get_assocparams(0)
    print ("assocparams:", x.__dict__)
    if x.cookie_life != 334:
        raise print ( "set_assocparams() did not work for UDP socket")

    x = tcp.get_assocparams()
    if not x.cookie_life:
        raise print ( " get_assocparams() did not work")
    print ("assocparams:", x.__dict__)
    # FIXME
    # x.cookie_life = 335
    # print ( "assocparams:", x.__dict__
    # tcp.set_assocparams(x)
    # x = tcp.get_assocparams()
    # print ( "assocparams:", x.__dict__
    # if x.cookie_life != 335:
    #   	raise print ( "set_assocparams() did not work for TCP socket"

    x = tcp.get_paddrparams(0, saddr)
    if not x.hbinterval:
        raise print ( "get_paddrparams did not work")
    x.hbinterval = 60003
    print ("paddrparams:", x.__dict__)
    tcp.set_paddrparams(x)
    x = tcp.get_paddrparams(0, saddr)
    print ("paddrparams:", x.__dict__)
    if x.hbinterval != 60003:
        raise print ( "set_paddrparms() did not work for TCP socket")

    x = tcp.get_status(0)
    if not x.rwnd:
        raise print ( "get_status() did not work for TCP socket")
    else:
        print ("rwnd of TCP socket: %d" % x.rwnd)

    x = tcp.get_paddrinfo(0, saddr)
    if not x.cwnd:
        raise print ( "get_paddrinfo() did not work for TCP socket")
    else:
        print ("cwnd of TCP socket: %d" % x.cwnd)

    tcp.sctp_send(msg)
    while 1:
        fromaddr, flags, msgret, notif = tcp.sctp_recv(1000)
        print ("	Msg arrived, flag %d" % flags)

        if flags & FLAG_NOTIFICATION:
            raise print ( "We did not subscribe to receive notifications!")

        if msgret != expected_ret:
            raise print ( "Unexpected return from server")
        else:
            # Next mesage should be a 0-length message to signal EOF
            expected_ret = ''

        if notif.__class__ != sndrcvinfo:
            raise print ( "Unexpected notification event")

        if i >= 2 and notif.stream != 2:
            raise print ( "Should return msg via stream 2")
        if expected_ret == '':
            # connection close (empty message) was received
            break

    tcp.close()

    print (
    "UDP ", saddr, " ----------------------------------------------")

    msg = "udp %d" % (baseport + i)
    expected_ret = "#" + msg
    udp.sctp_send(msg, to=saddr)
    time.sleep(1)

    while 1:
        fromaddr, flags, msgret, notif = udp.sctp_recv(1000)
        print ("		Arrived msg, flag %d, content %s" % (flags, msgret))

        if flags & FLAG_NOTIFICATION:
            if notif.__class__ != assoc_change:
                raise print ( "Unexpected notification")
            print ("Connection state: %d" % notif.state)
            if notif.state == assoc_change.state_COMM_UP:
                print ("assoc id = %d" % notif.assoc_id)

                print ("udp paddrs: ", udp.getpaddrs(notif.assoc_id))

                laddrs = udp.getladdrs(0)
                print ("udp laddrs: ", laddrs)

                udp.set_primary(notif.assoc_id, saddr)

                udp.set_peer_primary(notif.assoc_id, (client, laddrs[0][1]))

                x = udp.get_rtoinfo(notif.assoc_id)
                x.max = 33333
                udp.set_rtoinfo(x)
                print ("rtoinfo:", x.__dict__)
                if udp.get_rtoinfo(notif.assoc_id).max != 33333:
                    raise print ( "set_rtoinfo() did not work for UDP socket")

                x = udp.get_assocparams(notif.assoc_id)
                x.cookie_life = 333
                udp.set_assocparams(x)
                print ("assocparams:", x.__dict__)
                if udp.get_assocparams(notif.assoc_id).cookie_life != 333:
                    raise print ( "set_assocparams() did not work for UDP socket")

                x = udp.get_paddrparams(notif.assoc_id, saddr)
                print ("paddrparams:", x)
                x.hbinterval = 34444
                udp.set_paddrparams(x)
                if udp.get_paddrparams(notif.assoc_id, saddr).hbinterval != 34444:
                    raise print ( "set_paddrparms() did not work for UDP socket")

                x = udp.get_status(notif.assoc_id)
                if not x.rwnd:
                    raise print ( "get_status() did not work for UDP socket")
                else:
                    print ("rwnd of UDP socket: %d" % x.rwnd)

                x = udp.get_paddrinfo(notif.assoc_id, saddr)
                if not x.cwnd:
                    raise print ( "get_paddrinfo() did not work for UDP socket")
                else:
                    print ("cwnd of UDP socket: %d" % x.cwnd)

            elif notif.state == assoc_change.state_CANT_START_ASSOCIATION:
                raise print ( "Connection could not be set up, aborting.")

        # ok, wait for the data
        else:
            if msgret != expected_ret:
                raise print ( "Unexpected return from server ('%s' was returned)" % msgret)
            if fromaddr != saddr:
                raise print ( "Answer came from unknown address")
            if notif.__class__ != sndrcvinfo:
                raise print ( "Unexpected notification event")
            if i >= 2 and notif.stream != 2:
                raise print ( "Should return msg via stream 2")

            # For now, we are satisfied with this.
            break
