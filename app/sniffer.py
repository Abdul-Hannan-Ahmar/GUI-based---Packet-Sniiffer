from scapy.all import IP, TCP, sniff

def start_sniff(iface, callback):
    sniff(iface=iface, prn=callback, store=0)

def parse_packet(packet):
    if IP in packet:
        src = packet[IP].src
        dst = packet[IP].dst
        proto = packet[IP].proto
        flags = ''
        if TCP in packet:
            flags = str(packet[TCP].flags)
        return src, dst, proto, flags
    return None