CyberShield Networking Lab 001
IPv4 Subnetting and Network Segmentation
1. Network Addressing
Original network: 192.168.10.0/24

Subnet prefix: /26

Subnet mask: 255.255.255.192

Total subnets: 4

Usable hosts per subnet: 62
Network	Network Address	First Host	Last Host	Broadcast
Staff	192.168.10.0/26	192.168.10.1	192.168.10.62	192.168.10.63
Guest Wi-Fi	192.168.10.64/26	192.168.10.65	192.168.10.126	192.168.10.127
Servers	192.168.10.128/26	192.168.10.129	192.168.10.190	192.168.10.191
Reserved	192.168.10.192/26	192.168.10.193	192.168.10.254	192.168.10.255

2. Suggested Gateways
- Staff: 192.168.10.1
- Guest Wi-Fi: 192.168.10.65
- Servers: 192.168.10.129
3. Network Topology
                 INTERNET
                    |
             ROUTER / FIREWALL
                    |
              MANAGED SWITCH
              /      |      \
           STAFF    GUEST   SERVERS
           VLAN 10  VLAN 20 VLAN 30
              |       |       |
           Staff   Guest AP  Business
           PCs               Servers


4. Firewall Policy
Default policy: DENY unless explicitly permitted.
Source	Destination	Action
Staff	Internet	Allow
Staff	Approved servers	Allow
Guest Wi-Fi	Internet	Allow
Guest Wi-Fi	Staff	Deny
Guest Wi-Fi	Servers	Deny
Servers	Staff	Deny by default
Servers	Guest Wi-Fi	Deny
Internet	Internal networks	Deny by default

Additional controls:
- Allow DHCP and DNS to approved services.
- Restrict server administration to authorized administrators.
- Permit established return traffic.
- Log denied connections.
- Review firewall rules regularly.
