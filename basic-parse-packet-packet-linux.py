#!/usr/bin/python3

import struct
import socket
import binascii

def ethernet_head(raw_data):
    dest, src, prototype = struct.unpack('! 6s 6s H', raw_data[:14])
    dest_mac = ':'.join(f'{b:02x}' for b in dest)
    src_mac = ':'.join(f'{b:02x}' for b in src)
    proto = socket.htons(prototype)
    data = raw_data[14:]
    return dest_mac, src_mac, proto, data

def obtener_descripcion_por_id(id_decimal):
    tabla_ethertypes = {        
        0: "0000-05DC: IEEE802.3 Length Field [IEEE Std 802.3]",
        511: "0101-01FF: Old Xerox Experimental values. Invalid as an Ethertype since 1983. [Neil_Sembower]",
        512: "0200: Formerly XEROX PUP. Invalid as an Ethertype since 1983. Use 0x0A00. [Boggs, D., J. Shoch, E. Taft, and R. Metcalfe, \"PUP: An Internetwork Architecture\", XEROX Palo Alto Research Center, CSL-79-10, July 1979; also in IEEE Transactions on Communication, Volume COM-28, Number 4, April 1980.][Neil_Sembower]",
        513: "0201: Formerly PUP Addr Trans. Invalid as an Ethertype since 1983. Use 0x0A01. [Neil_Sembower]",
        1024: "0400: Old Nixdorf private protocol. Invalid as an Ethertype since 1983. [Neil_Sembower]",
        1536: "0600: XEROX NS IDP [\"The Ethernet, A Local Area Network: Data Link Layer and Physical Layer Specification\", AA-K759B-TK, Digital Equipment Corporation, Maynard, MA. Also as: \"The Ethernet - A Local Area Network\", Version 1.0, Digital Equipment Corporation, Intel Corporation, Xerox Corporation, September 1980. And: \"The Ethernet, A Local Area Network: Data Link Layer and Physical Layer Specifications\", Digital, Intel and Xerox, November 1982. And: XEROX, \"The Ethernet, A Local Area Network: Data Link Layer and Physical Layer Specification\", X3T51/80-50, Xerox Corporation, Stamford, CT., October 1980.][Neil_Sembower]",
        1632: "0660: DLOG [Neil_Sembower]",
        1633: "0661: DLOG [Neil_Sembower]",
        2048: "0800: Internet Protocol version 4 (IPv4) [RFC-ietf-intarea-rfc7042bis-11]",
        2049: "0801: X.75 Internet [Neil_Sembower]",
        2050: "0802: NBS Internet [Neil_Sembower]",
        2051: "0803: ECMA Internet [Neil_Sembower]",
        2052: "0804: Chaosnet [Neil_Sembower]",
        2053: "0805: X.25 Level 3 [Neil_Sembower]",
        2054: "0806: Address Resolution Protocol (ARP) [RFC-ietf-intarea-rfc7042bis-11]",
        2055: "0807: XNS Compatability [Neil_Sembower]",
        2056: "0808: Frame Relay ARP [RFC1701]",
        2076: "081C: Symbolics Private [David_Plummer]",
        2184: "0888-088A: Xyplex [Neil_Sembower]",
        2304: "0900: Ungermann-Bass net debugr [Neil_Sembower]",
        2560: "0A00: Xerox IEEE802.3 PUP [Neil_Sembower]",
        2561: "0A01: PUP Addr Trans [Neil_Sembower]",
        2989: "0BAD: Banyan VINES [Neil_Sembower]",
        2990: "0BAE: VINES Loopback [RFC1701]",
        2991: "0BAF: VINES Echo [RFC1701]",
        4096: "1000: Berkeley Trailer nego [Neil_Sembower]",
        4097: "1001-100F: Berkeley Trailer encap/IP [Neil_Sembower]",
        5632: "1600: Valid Systems [Neil_Sembower]",
        8947: "22F3: TRILL [RFC6325]",
        8948: "22F4: L2-IS-IS [RFC6325]",
        16962: "4242: PCS Basic Block Protocol [Neil_Sembower]",
        21000: "5208: BBN Simnet [Neil_Sembower]",
        24576: "6000: DEC Unassigned (Exp.) [Neil_Sembower]",
        24577: "6001: DEC MOP Dump/Load [Neil_Sembower]",
        24578: "6002: DEC MOP Remote Console [Neil_Sembower]",
        24579: "6003: DEC DECNET Phase IV Route [Neil_Sembower]",
        24580: "6004: DEC LAT [Neil_Sembower]",
        24581: "6005: DEC Diagnostic Protocol [Neil_Sembower]",
        24582: "6006: DEC Customer Protocol [Neil_Sembower]",
        24583: "6007: DEC LAVC, SCA [Neil_Sembower]",
        24584: "6008-6009: DEC Unassigned [Neil_Sembower]",
        24592: "6010-6014: 3Com Corporation [Neil_Sembower]",
        25944: "6558: Trans Ether Bridging [RFC1701]",
        25945: "6559: Raw Frame Relay [RFC1701]",
        28672: "7000: Ungermann-Bass download [Neil_Sembower]",
        28674: "7002: Ungermann-Bass dia/loop [Neil_Sembower]",
        28704: "7020-7029: LRT [Neil_Sembower]",
        28720: "7030: Proteon [Neil_Sembower]",
        28724: "7034: Cabletron [Neil_Sembower]",
        32771: "8003: Cronus VLN [RFC824][Daniel_Tappan]",
        32772: "8004: Cronus Direct [RFC824][Daniel_Tappan]",
        32773: "8005: HP Probe [Neil_Sembower]",
        32774: "8006: Nestar [Neil_Sembower]",
        32776: "8008: AT&T [Neil_Sembower]",
        32784: "8010: Excelan [Neil_Sembower]",
        32787: "8013: SGI diagnostics [Andrew_Cherenson]",
        32788: "8014: SGI network games [Andrew_Cherenson]",
        32789: "8015: SGI reserved [Andrew_Cherenson]",
        32790: "8016: SGI bounce server [Andrew_Cherenson]",
        32793: "8019: Apollo Domain [Neil_Sembower]",
        32814: "802E: Tymshare [Neil_Sembower]",
        32815: "802F: Tigan, Inc. [Neil_Sembower]",
        32821: "8035: Reverse Address",
        33100: "SNMP",
        9728:  "Reserved [RFC1701]",
        8: "ARP (Address Resolution Protocol)"
     }

    return tabla_ethertypes.get(id_decimal, "ID no encontrado en la tabla")


def main():
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    while True:
        raw_data = s.recvfrom(65535)
        eth = ethernet_head(raw_data[0])
        if eth[2] != 8:
            print("\nEthernet frame")
            #print('Dest MAC: {}, Src MAC: {}, Prototype: {}, Data: {}'.format(eth[0], eth[1], eth[2], eth[3]))
            print('Dest MAC: {}, Src MAC: {}, Prototype: {}, {}'.format(eth[0], eth[1], eth[2],obtener_descripcion_por_id(eth[2])))

main()
