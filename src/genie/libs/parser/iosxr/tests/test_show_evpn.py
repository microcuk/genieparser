
# Python
import unittest
from unittest.mock import Mock

# ATS
from ats.topology import Device
from ats.topology import loader

# Metaparser
from genie.metaparser.util.exceptions import SchemaEmptyParserError, SchemaMissingKeyError

# iosxr show_evpn
from genie.libs.parser.iosxr.show_evpn import (ShowEvpnEvi,
                                               ShowEvpnEviDetail,
                                               ShowEvpnEviMac,
                                               ShowEvpnEviMacPrivate,
                                               ShowEvpnEthernetSegment,
                                               ShowEvpnEthernetSegmentDetail,
                                               ShowEvpnEthernetSegmentEsiDetail,
                                               ShowEvpnInternalLabel,
                                               ShowEvpnEthernetSegmentPrivate)

# ===================================================
#  Unit test for 'show evpn evi'
# ===================================================

class TestShowEvpnEvi(unittest.TestCase):

    '''Unit test for 'show evpn evi'''
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output1 = {
        'evi': {
            1000: {
                'bridge_domain': 'VPWS:1000',
                'type': 'VPWS (vlan-unaware)',
            },
            2000: {
                'bridge_domain': 'XC-POD1-EVPN',
                'type': 'EVPN',
            },
            2001: {
                'bridge_domain': 'XC-POD2-EVPN',
                'type': 'EVPN',
            },
        },
    }

    golden_output1 = {'execute.return_value': '''
        RP/0/RSP1/CPU0:Router1#show evpn evi
        EVI        Bridge                       Domain Type
        ---------- ---------------------------- -------------------
        1000        VPWS:1000                   VPWS (vlan-unaware)
        2000        XC-POD1-EVPN                EVPN
        2001        XC-POD2-EVPN                EVPN

        '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowEvpnEvi(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output1)
        obj = ShowEvpnEvi(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output1)

# ===================================================
#  Unit test for 'show evpn evi detail'
# ===================================================

class TestShowEvpnEviDetail(unittest.TestCase):

    '''Unit test for 'show evpn evi detail'''
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output1 = {
        'evi': {
            145: {
                'bridge_domain': 'tb1-core1',
                'type': 'PBB',
                'unicast_label': '16000',
                'multicast_label': '16001',
                'rd_config': 'none',
                'rd_auto': '(auto) 1.100.100.100:145',
                'rt_auto': '100:145',
                'route_target_in_use': {
                    '100:145': {
                        'import': True,
                        'export': True,
                    },
                },
            },
            165: {
                'bridge_domain': 'tb1-core2',
                'type': 'PBB',
                'unicast_label': '16002',
                'multicast_label': '16003',
                'rd_config': 'none',
                'rd_auto': '(auto) 1.100.100.100:165',
                'rt_auto': '100:165',
                'route_target_in_use': {
                    '100:165': {
                        'import': True,
                        'export': True,
                    },
                },
            },
            185: {
                'bridge_domain': 'tb1-core3',
                'type': 'PBB',
                'unicast_label': '16004',
                'multicast_label': '16005',
                'rd_config': 'none',
                'rd_auto': '(auto) 1.100.100.100:185',
                'rt_auto': '100:185',
                'route_target_in_use': {
                    '100:185': {
                        'import': True,
                        'export': True,
                    },
                },
            },
            65535: {
                'bridge_domain': 'ES:GLOBAL',
                'type': 'BD',
                'unicast_label': '0',
                'multicast_label': '0',
                'rd_config': 'none',
                'rd_auto': '(auto) 1.100.100.100:0',
                'rt_auto': 'none',
            },
        },
    }

    golden_output1 = {'execute.return_value': '''
        RP/0/RSP0/CPU0:Router1#show evpn evi detail
        EVI        Bridge Domain                Type   
        ---------- ---------------------------- -------
        145        tb1-core1                    PBB 
        Unicast Label  : 16000
        Multicast Label: 16001
        RD Config: none
        RD Auto  : (auto) 1.100.100.100:145
        RT Auto  : 100:145
        Route Targets in Use           Type   
        ------------------------------ -------
        100:145                        Import 
        100:145                        Export 

        165        tb1-core2                    PBB 
        Unicast Label  : 16002
        Multicast Label: 16003
        RD Config: none
        RD Auto  : (auto) 1.100.100.100:165
        RT Auto  : 100:165
        Route Targets in Use           Type   
        ------------------------------ -------
        100:165                        Import 
        100:165                        Export 

        185        tb1-core3                    PBB 
        Unicast Label  : 16004
        Multicast Label: 16005
        RD Config: none
        RD Auto  : (auto) 1.100.100.100:185
        RT Auto  : 100:185
        Route Targets in Use           Type   
        ------------------------------ -------
        100:185                        Import 
        100:185                        Export 

        65535      ES:GLOBAL                    BD  
        Unicast Label  : 0
        Multicast Label: 0
        RD Config: none
        RD Auto  : (auto) 1.100.100.100:0
        RT Auto  : none
        Route Targets in Use           Type   
        ------------------------------ -------
        0100.9e00.0210                 Import 
        0100.be01.ce00                 Import 
        0100.be02.0101                 Import

        '''}
    
    golden_parsed_output2 = {
        'evi': {
            1: {
                'bridge_domain': 'core1',
                'type': 'PBB',
                'unicast_label': '24001',
                'multicast_label': '24002',
                'flow_label': 'N',
                'table-policy_name': 'forward_class_1',
                'forward-class': '1',
                'rd_config': 'none',
                'rd_auto': 'none',
                'rt_auto': 'none',
            },
        },
    }

    golden_output2 = {'execute.return_value': '''
        show evpn evi detail 
        Mon Aug 24 14:14:19.873 EDT

        EVI        Bridge Domain                Type   
        ---------- ---------------------------- -------
        1          core1                        PBB    
        Unicast Label  : 24001
        Multicast Label: 24002
        Flow Label: N
        Table-policy Name: forward_class_1
        Forward-class: 1
        RD Config: none
        RD Auto  : none
        RT Auto  : none
        Route Targets in Use           Type   
        ------------------------------ -------

        '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowEvpnEviDetail(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output1)
        obj = ShowEvpnEviDetail(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output1)
    
    def test_golden2(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output2)
        obj = ShowEvpnEviDetail(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output2)

# ===================================================
#  Unit test for 'show evpn evi mac'
# ===================================================

class test_show_evpn_evi_mac(unittest.TestCase):

    '''Unit test for 'show evpn evi mac'''
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output1 = {
        'vpn_id': {
            65535: {
                'mac_address': {
                    '0000.0000.0000': {
                        'encap': 'N/A',
                        'ip_address': '::',
                        'next_hop': 'Local',
                        'label': 0,
                    },
                },
            },
        },
    }

    golden_output1 = {'execute.return_value': '''
        show evpn evi mac
        Tue Sep 17 20:04:11.302 UTC

        VPN-ID     Encap  MAC address    IP address                               Nexthop                                 Label 
        ---------- ------ -------------- ---------------------------------------- --------------------------------------- --------
        65535      N/A    0000.0000.0000 ::                                       Local                                   0     

        '''}
    
    golden_parsed_output2 = {
        'vpn_id': {
            65535: {
                'mac_address': {
                    '0000.0000.0000': {
                        'encap': 'N/A',
                        'ip_address': '::',
                        'next_hop': 'Local',
                        'label': 0,
                    },
                },
            },
        },
    }

    golden_output2 = {'execute.return_value': '''
        show evpn evi vpn-id 65535 mac
        Tue Sep 17 20:04:11.302 UTC

        VPN-ID     Encap  MAC address    IP address                               Nexthop                                 Label 
        ---------- ------ -------------- ---------------------------------------- --------------------------------------- --------
        65535      N/A    0000.0000.0000 ::                                       Local                                   0     

        '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowEvpnEviMac(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output1)
        obj = ShowEvpnEviMac(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output1)
    
    def test_golden2(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output2)
        obj = ShowEvpnEviMac(device=self.device)
        parsed_output = obj.parse(vpn_id='65535')
        self.assertEqual(parsed_output,self.golden_parsed_output2)

# ===================================================
#  Unit test for 'show evpn evi mac private'
# ===================================================

class test_show_evpn_evi_mac_private(unittest.TestCase):

    '''Unit test for 'show evpn evi mac private'''
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output1 = {
        'vpn_id': {
            65535: {
                'mac_address': {
                    '0000.0000.0000': {
                        'encap': 'N/A',
                        'ip_address': '::',
                        'next_hop': 'Local',
                        'label': 0,
                        'ethernet_tag': 0,
                        'multipaths_resolved': 'False',
                        'multipaths_internal_label': 0,
                        'local_static': 'No',
                        'remote_static': 'No',
                        'local_ethernet_segment': '0000.0000.0000.0000.0000',
                        'remote_ethernet_segment': '0000.0000.0000.0000.0000',
                        'local_sequence_number': 0,
                        'remote_sequence_number': 0,
                        'local_encapsulation': 'N/A',
                        'remote_encapsulation': 'N/A',
                        'esi_port_key': 0,
                        'source': 'Local',
                        'flush_requested': 0,
                        'flush_received': 0,
                        'soo_nexthop': '::',
                        'bp_xcid': '0xffffffff',
                        'mac_state': 'Init',
                        'mac_producers': '0x0 (Best: 0x0)',
                        'local_router_mac': '0000.0000.0000',
                        'l3_label': 0,
                        'object': {
                            'EVPN MAC': {
                                'base_info': {
                                    'version': '0xdbdb0008',
                                    'flags': '0x4000',
                                    'type': 8,
                                    'reserved': 0,
                                },
                                'num_events': 0,
                            },
                        },
                    },
                },
            },
        },
    }

    golden_output1 = {'execute.return_value': '''
        show evpn evi mac private
        Tue Sep 17 20:08:26.843 UTC

        VPN-ID     Encap  MAC address    IP address                               Nexthop                                 Label 
        ---------- ------ -------------- ---------------------------------------- --------------------------------------- --------
        65535      N/A    0000.0000.0000 ::                                       Local                                   0     
        Ethernet Tag                            : 0
        Multi-paths Resolved                    : False
        Multi-paths Internal label              : 0
        Local Static                            : No
        Remote Static                           : No
        Local Ethernet Segment                  : 0000.0000.0000.0000.0000
        Remote Ethernet Segment                 : 0000.0000.0000.0000.0000
        Local Sequence Number                   : 0
        Remote Sequence Number                  : 0
        Local Encapsulation                     : N/A
        Remote Encapsulation                    : N/A
        ESI Port Key                            : 0
        Source                                  : Local
        Flush Requested                         : 0
        Flush Received                          : 0
        SOO Nexthop                             : ::
        BP XCID                                 : 0xffffffff
        MAC State                               : Init
        MAC Producers                           : 0x0 (Best: 0x0)
        Local Router MAC                        : 0000.0000.0000
        L3 Label                                : 0

        Object: EVPN MAC
        Base info: version=0xdbdb0008, flags=0x4000, type=8, reserved=0
        EVPN MAC event history  [Num events: 0]
        ----------------------------------------------------------------------------
            Time                Event                         Flags      Flags
            ====                =====                         =====      =====
        ---------------------------------------------------------------------------- 

        '''}
    
    golden_parsed_output2 = {
        'vpn_id': {
            7: {
                'mac_address': {
                    '001b.0100.0001': {
                        'next_hop': 'N/A',
                        'label': 24014,
                        'ip_address': '7.7.7.8',
                        'ethernet_segment': '0000.0000.0000.0000.0000',
                        'source': 'Local',
                        'object': {
                            'EVPN MAC': {
                                'base_info': {
                                    'version': '0xdbdb0008',
                                    'flags': '0x204100',
                                    'type': 2113792,
                                    'reserved': 0,
                                },
                                'num_events': 12,
                                'event_history': {
                                    1: {
                                        'time': 'Jun 14 14:02:12.864',
                                        'event': 'Create',
                                        'flag_1': '00000000',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    2: {
                                        'time': 'Jun 14 14:02:12.864',
                                        'event': 'MAC advertise rejected',
                                        'flag_1': '00000003',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    3: {
                                        'time': 'Jun 14 14:07:33.376',
                                        'event': 'Redundant path buffer',
                                        'flag_1': '00000000',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    4: {
                                        'time': 'Jun 14 14:07:33.376',
                                        'event': 'Modify',
                                        'flag_1': '00000000',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    5: {
                                        'time': 'Jun 14 14:07:33.376',
                                        'event': 'MAC advertise rejected',
                                        'flag_1': '00000003',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    6: {
                                        'time': 'Jun 14 14:55:40.544',
                                        'event': 'Redundant path buffer',
                                        'flag_1': '00000000',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    7: {
                                        'time': 'Jun 14 14:55:40.544',
                                        'event': 'Modify',
                                        'flag_1': '00000000',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    8: {
                                        'time': 'Jun 14 14:55:40.544',
                                        'event': 'MAC advertise rejected',
                                        'flag_1': '00000003',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    9: {
                                        'time': 'Jun 14 15:00:53.888',
                                        'event': 'Redundant path buffer',
                                        'flag_1': '00000000',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    10: {
                                        'time': 'Jun 14 15:00:53.888',
                                        'event': 'Modify',
                                        'flag_1': '00000000',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    11: {
                                        'time': 'Jun 14 15:00:53.888',
                                        'event': 'MAC advertise rejected',
                                        'flag_1': '00000003',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    12: {
                                        'time': 'Jun 14 15:13:16.800',
                                        'event': 'Advertise to BGP',
                                        'flag_1': '00004110',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    golden_output2 = {'execute.return_value': '''
        sh evpn evi mac private
        Tue Jun 14 15:14:25.359 UTC
        
        MAC address    Nexthop                                 Label    vpn-id 
        -------------- --------------------------------------- -------- --------
        001b.0100.0001 N/A                                     24014    7      
        IP Address   : 7.7.7.8
        Ether.Segment: 0000.0000.0000.0000.0000
        ESI port key : 0x0000
        Source       : Local
        Multi-paths resolved: FALSE
        Multi-paths local label: 0        
        Flush Count  : 0
        BP IFH: 0
        Flush Seq ID : 0
        Static: No
        
        Object: EVPN MAC
        Base info: version=0xdbdb0008, flags=0x204100, type=2113792, reserved=0
        EVPN MAC event history  [Num events: 12]
        ----------------------------------------------------------------------------
            Time                Event                         Flags      Flags     
            ====                =====                         =====      =====     
            Jun 14 14:02:12.864 Create                        00000000, 00000000 -  -
            Jun 14 14:02:12.864 MAC advertise rejected        00000003, 00000000 -  -
            Jun 14 14:07:33.376 Redundant path buffer         00000000, 00000000 -  -
            Jun 14 14:07:33.376 Modify                        00000000, 00000000 -  -
            Jun 14 14:07:33.376 MAC advertise rejected        00000003, 00000000 -  -
            Jun 14 14:55:40.544 Redundant path buffer         00000000, 00000000 -  -
            Jun 14 14:55:40.544 Modify                        00000000, 00000000 -  -
            Jun 14 14:55:40.544 MAC advertise rejected        00000003, 00000000 -  -
            Jun 14 15:00:53.888 Redundant path buffer         00000000, 00000000 -  -
            Jun 14 15:00:53.888 Modify                        00000000, 00000000 -  -
            Jun 14 15:00:53.888 MAC advertise rejected        00000003, 00000000 -  -
            Jun 14 15:13:16.800 Advertise to BGP              00004110, 00000000 -  -
        ----------------------------------------------------------------------------

        '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowEvpnEviMacPrivate(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output1)
        obj = ShowEvpnEviMacPrivate(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output1)
    
    def test_golden2(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output2)
        obj = ShowEvpnEviMacPrivate(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output2)

# ===================================================
#  Unit test for 'show evpn ethernet-segment'
# ===================================================

class test_show_evpn_ethernet_segment(unittest.TestCase):

    '''Unit test for 'show evpn ethernet-segment'''
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output1 = {
        'segment_id': {
            '0012.1200.0000.0000.0000': {
                'interface': {
                    'Nv101': {
                        'next_hops': ['10.10.10.10'],
                    },
                },
            },
            '0012.1200.0001.0000.0001': {
                'interface': {
                    'PW:40.40.40.40,10001': {
                        'next_hops': ['10.10.10.10'],
                    },
                },
            },
            '0012.1200.0001.0000.0002': {
                'interface': {
                    'Bundle-Ether1': {
                        'next_hops': ['10.10.10.10'],
                    },
                },
            },
            '0012.1200.0001.0000.0003': {
                'interface': {
                    'VFI:ves-vfi-1': {
                        'next_hops': ['10.10.10.10'],
                    },
                },
            },
            '0012.1200.0002.0000.0001': {
                'interface': {
                    'PW:40.40.40.40,10011': {
                        'next_hops': ['10.10.10.10'],
                    },
                },
            },
            '0012.1200.0002.0000.0003': {
                'interface': {
                    'VFI:ves-vfi-2': {
                        'next_hops': ['10.10.10.10'],
                    },
                },
            },
            'N/A': {
                'interface': {
                    'PW:40.40.40.40,10007': {
                        'next_hops': ['10.10.10.10'],
                    },
                    'PW:40.40.40.40,10017': {
                        'next_hops': ['10.10.10.10'],
                    },
                },
            },
        },
    }

    golden_output1 = {'execute.return_value': '''
        show evpn ethernet-segment

        Ethernet Segment Id      Interface                          Nexthops
        ------------------------ ---------------------------------- --------------------
        0012.1200.0000.0000.0000 nv101                              10.10.10.10
        0012.1200.0001.0000.0001 PW:40.40.40.40,10001               10.10.10.10
        0012.1200.0001.0000.0002 BE1                                10.10.10.10
        0012.1200.0001.0000.0003 VFI:ves-vfi-1                      10.10.10.10
        0012.1200.0002.0000.0001 PW:40.40.40.40,10011               10.10.10.10
        0012.1200.0002.0000.0003 VFI:ves-vfi-2                      10.10.10.10
        N/A                      PW:40.40.40.40,10007               10.10.10.10
        N/A                      PW:40.40.40.40,10017               10.10.10.10
    '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowEvpnEthernetSegment(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output1)
        obj = ShowEvpnEthernetSegment(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output1)

# ===================================================
#  Unit test for 'show evpn ethernet-segment detail'
# ===================================================

class test_show_evpn_ethernet_segment_detail(unittest.TestCase):

    '''Unit test for 'show evpn ethernet-segment detail'''
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output1 = {
        'segment_id': {
            '0210.0300.9e00.0210.0000': {
                'interface': {
                    'GigabitEthernet0/3/0/0': {
                        'next_hops': ['1.100.100.100', '2.100.100.100'],
                        'es_to_bgp_gates': 'Ready',
                        'es_to_l2fib_gates': 'Ready',
                        'main_port': {
                            'interface': 'GigabitEthernet0/3/0/0',
                            'if_handle': '0x1800300',
                            'state': 'Up',
                            'redundancy': 'Not Defined',
                        },
                        'source_mac': '0001.ed9e.0001 (PBB BSA)',
                        'topology': {
                            'operational': 'MHN',
                            'configured': 'A/A per service (default)',
                        },
                        'primary_services': 'Auto-selection',
                        'secondary_services': 'Auto-selection',
                        'service_carving_results': {
                            'bridge_ports': {
                                'num_of_total': 3,
                            },
                            'elected': {
                                'num_of_total': 0,
                            },
                            'not_elected': {
                                'num_of_total': 3,
                                'i_sid_ne': ['1450101', '1650205', '1850309'],
                            },
                        },
                        'mac_flushing_mode': 'STP-TCN',
                        'peering_timer': '45 sec [not running]',
                        'recovery_timer': '20 sec [not running]',
                        'flush_again_timer': '60 sec',
                    },
                },
            },
            'be01.0300.be01.ce00.0001': {
                'interface': {
                    'Bundle-Ether1': {
                        'next_hops': ['1.100.100.100', '2.100.100.100'],
                        'es_to_bgp_gates': 'Ready',
                        'es_to_l2fib_gates': 'Ready',
                        'main_port': {
                            'interface': 'Bundle-Ether1',
                            'if_handle': '0x000480',
                            'state': 'Up',
                            'redundancy': 'Active',
                        },
                        'source_mac': '0024.be01.ce00 (Local)',
                        'topology': {
                            'operational': 'MHN',
                            'configured': 'A/A per flow (default)',
                        },
                        'primary_services': 'Auto-selection',
                        'secondary_services': 'Auto-selection',
                        'service_carving_results': {
                            'bridge_ports': {
                                'num_of_total': 3,
                            },
                            'elected': {
                                'num_of_total': 3,
                                'i_sid_e': ['1450102', '1650206', '1850310'],
                            },
                            'not_elected': {
                                'num_of_total': 0,
                            },
                        },
                        'mac_flushing_mode': 'STP-TCN',
                        'peering_timer': '45 sec [not running]',
                        'recovery_timer': '20 sec [not running]',
                        'flush_again_timer': '60 sec',
                    },
                },
            },
        },
    }

    golden_output1 = {'execute.return_value': '''
        Router#show evpn ethernet-segment detail
        Tue Jun 25 14:17:09.610 EDT
        Legend:
        A- PBB-EVPN load-balancing mode and Access Protection incompatible,
        B- no Bridge Ports PBB-EVPN enabled,
        C- Backbone Source MAC missing,
        E- ESI missing,
        H- Interface handle missing,
        I- Interface name missing,
        M- Interface in Down state,
        O- BGP End of Download missing,
        P- Interface already Access Protected,
        Pf-Interface forced single-homed,
        R- BGP RID not received,
        S- Interface in redundancy standby state,
        X- ESI-extracted MAC Conflict

        Ethernet Segment Id      Interface      Nexthops                                
        ------------------------ -------------- ----------------------------------------
        0210.0300.9e00.0210.0000 Gi0/3/0/0      1.100.100.100                           
                                                2.100.100.100                           
        ES to BGP Gates   : Ready
        ES to L2FIB Gates : Ready
        Main port         :
            Interface name : GigabitEthernet0/3/0/0
            IfHandle       : 0x1800300
            State          : Up
            Redundancy     : Not Defined
        Source MAC        : 0001.ed9e.0001 (PBB BSA)
        Topology          :
            Operational    : MHN
            Configured     : A/A per service (default)
        Primary Services  : Auto-selection
        Secondary Services: Auto-selection
        Service Carving Results:
            Bridge ports   : 3
            Elected        : 0
            Not Elected    : 3
                I-Sid NE  :  1450101, 1650205, 1850309
        MAC Flushing mode : STP-TCN
        Peering timer     : 45 sec [not running]
        Recovery timer    : 20 sec [not running]
        Flushagain timer  : 60 sec

        be01.0300.be01.ce00.0001 BE1            1.100.100.100                           
                                                2.100.100.100                           
        ES to BGP Gates   : Ready
        ES to L2FIB Gates : Ready
        Main port         :
            Interface name : Bundle-Ether1
            IfHandle       : 0x000480
            State          : Up
            Redundancy     : Active
        Source MAC        : 0024.be01.ce00 (Local)
        Topology          :
            Operational    : MHN
            Configured     : A/A per flow (default)
        Primary Services  : Auto-selection
        Secondary Services: Auto-selection
        Service Carving Results:
            Bridge ports   : 3
            Elected        : 3
                I-Sid E   :  1450102, 1650206, 1850310
            Not Elected    : 0
        MAC Flushing mode : STP-TCN
        Peering timer     : 45 sec [not running]
        Recovery timer    : 20 sec [not running]
        Flushagain timer  : 60 sec
        '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowEvpnEthernetSegmentDetail(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output1)
        obj = ShowEvpnEthernetSegmentDetail(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output1)

# ============================================================
#  Unit test for 'show evpn ethernet-segment esi {esi} detail'
# ============================================================

class TestShowEvpnEthernetSegmentEsiDetail(unittest.TestCase):

    '''Unit test for 'show evpn ethernet-segment esi {esi} detail'''
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output1 = {
        'segment_id': {
            '0047.4700.0000.0000.2200': {
                'interface': {
                    'Bundle-Ether200': {
                        'next_hops': ['4.4.4.47', '4.4.4.48'],
                        'es_to_bgp_gates': 'Ready',
                        'es_to_l2fib_gates': 'Ready',
                        'main_port': {
                            'interface': 'Bundle-Ether100',
                            'interface_mac': '119b.1755.e9ee',
                            'if_handle': '0x0900001c',
                            'state': 'Up',
                            'redundancy': 'Not Defined',
                        },
                        'esi': {
                            'type': 0,
                            'value': '47.4811.1111.1111.2211',
                        },
                        'es_import_rt': '4748.1111.1111 (from ESI)',
                        'source_mac': '1111.1111.1111 (N/A)',
                        'topology': {
                            'operational': 'MH, All-active',
                            'configured': 'All-active (AApF) (default)',
                        },
                        'service_carving': 'Auto-selection',
                        'peering_details': ['4.4.4.47[MOD:P:00]', '4.4.4.48[MOD:P:00]'],
                        'service_carving_results': {
                            'forwarders': 1,
                            'permanent': 0,
                            'elected': {
                                'num_of_total': 1,
                            },
                            'not_elected': {
                                'num_of_total': 0,
                            },
                        },
                        'mac_flushing_mode': 'STP-TCN',
                        'peering_timer': '3 sec [not running]',
                        'recovery_timer': '30 sec [not running]',
                        'carving_timer': '0 sec [not running]',
                        'local_shg_label': '75116',
                        'remote_shg_labels': {
                            '1': {
                                'label': {
                                    '75116': {
                                        'nexthop': '4.4.4.48',
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    golden_output1 = {'execute.return_value': '''
        show evpn ethernet-segment esi 0047.4700.0000.0000.2200 detail

        Legend:

        B   - No Forwarders EVPN-enabled,

        C   - Backbone Source MAC missing (PBB-EVPN),

        RT  - ES-Import Route Target missing,

        E   - ESI missing,

        H   - Interface handle missing,

        I   - Name (Interface or Virtual Access) missing,

        M   - Interface in Down state,

        O   - BGP End of Download missing,

        P   - Interface already Access Protected,

        Pf  - Interface forced single-homed,

        R   - BGP RID not received,

        S   - Interface in redundancy standby state,

        X   - ESI-extracted MAC Conflict

        SHG - No local split-horizon-group label allocated

        

        Ethernet Segment Id      Interface                          Nexthops

        ------------------------ ---------------------------------- --------------------

        0047.4700.0000.0000.2200 BE200                              4.4.4.47

                                                                    4.4.4.48

        ES to BGP Gates   : Ready

        ES to L2FIB Gates : Ready

        Main port         :

            Interface name : Bundle-Ether100

            Interface MAC  : 119b.1755.e9ee

            IfHandle       : 0x0900001c

            State          : Up

            Redundancy     : Not Defined

        ESI type          : 0

            Value          : 47.4811.1111.1111.2211

        ES Import RT      : 4748.1111.1111 (from ESI)

        Source MAC        : 1111.1111.1111 (N/A)

        Topology          :

            Operational    : MH, All-active

            Configured     : All-active (AApF) (default)

        Service Carving   : Auto-selection

        Peering Details   : 4.4.4.47[MOD:P:00] 4.4.4.48[MOD:P:00]

        Service Carving Results:

            Forwarders     : 1

            Permanent      : 0

            Elected        : 1

            Not Elected    : 0

        MAC Flushing mode : STP-TCN

        Peering timer     : 3 sec [not running]

        Recovery timer    : 30 sec [not running]

        Carving timer     : 0 sec [not running]

        Local SHG label   : 75116

        Remote SHG labels : 1

                    75116 : nexthop 4.4.4.48
        '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowEvpnEthernetSegmentEsiDetail(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse(esi='0047.4700.0000.0000.2200')

    def test_golden1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output1)
        obj = ShowEvpnEthernetSegmentEsiDetail(device=self.device)
        parsed_output = obj.parse(esi='0047.4700.0000.0000.2200')
        self.assertEqual(parsed_output,self.golden_parsed_output1)

# ===================================================
#  Unit test for 'show evpn internal-label'
# ===================================================
class TestShowEvpnInternalLabel(unittest.TestCase):

    '''Unit test for 'show evpn internal-label'''
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}
    
    golden_parsed_output1 = {
        'evi': {
            1000: {
                'ethernet_segment_id': {
                    '0000.0102.0304.0506.07aa': {
                        'index': {
                            1: {
                                'ether_tag': '0',
                                'label': 'None',
                            },
                            2: {
                                'ether_tag': '200',
                                'label': '24011',
                            },
                        },
                    },
                },
            },
        },
    }

    golden_output1 = {'execute.return_value': '''
        EVI     Ethernet    Segment Id                 EtherTag Label
        ----- --------------------------------------- -------- --------
        1000    0000.0102.0304.0506.07aa                0       None
        1000    0000.0102.0304.0506.07aa                200     24011
        '''}

    golden_parsed_output2 = {
        'evi': {
            1: {
                'ethernet_segment_id': {
                    '0055.5555.5555.5555.5555': {
                        'index': {
                            1: {
                                'ether_tag': '0',
                                'label': 'None',
                                'encap': 'MPLS',
                            },
                            2: {
                                'ether_tag': '1',
                                'label': '29348',
                                'encap': 'MPLS',
                                'summary_pathlist': {
                                    'index': {
                                        1: {
                                            'tep_id': '0xffffffff',
                                            'df_role': '(P)',
                                            'nexthop': '192.168.0.3',
                                            'label': '29213',
                                        },
                                    },
                                },
                            },
                            3: {
                                'ether_tag': '3',
                                'label': '29352',
                                'encap': 'MPLS',
                                'summary_pathlist': {
                                    'index': {
                                        2: {
                                            'tep_id': '0xffffffff',
                                            'df_role': '(P)',
                                            'nexthop': '192.168.0.3',
                                            'label': '29224',
                                        },
                                    },
                                },
                            },
                        },
                    },
                    '0088.8888.8888.8888.8888': {
                        'index': {
                            1: {
                                'ether_tag': '0',
                                'label': 'None',
                                'encap': 'MPLS',
                            },
                            2: {
                                'ether_tag': '1',
                                'label': '29350',
                                'encap': 'MPLS',
                                'summary_pathlist': {
                                    'index': {
                                        3: {
                                            'tep_id': '0xffffffff',
                                            'df_role': '(P)',
                                            'nexthop': '192.168.0.4',
                                            'label': '29340',
                                        },
                                    },
                                },
                            },
                            3: {
                                'ether_tag': '2',
                                'label': '29349',
                                'encap': 'MPLS',
                                'summary_pathlist': {
                                    'index': {
                                        4: {
                                            'tep_id': '0xffffffff',
                                            'df_role': '(P)',
                                            'nexthop': '192.168.0.3',
                                            'label': '29216',
                                        },
                                        5: {
                                            'tep_id': '0x00000000',
                                            'df_role': '(B)',
                                            'nexthop': '192.168.0.4',
                                            'label': '29341',
                                        },
                                    },
                                },
                            },
                            4: {
                                'ether_tag': '3',
                                'label': '29355',
                                'encap': 'MPLS',
                                'summary_pathlist': {
                                    'index': {
                                        6: {
                                            'tep_id': '0xffffffff',
                                            'df_role': '(P)',
                                            'nexthop': '192.168.0.4',
                                            'label': '29352',
                                        },
                                    },
                                },
                            },
                            5: {
                                'ether_tag': '4',
                                'label': '29354',
                                'encap': 'MPLS',
                                'summary_pathlist': {
                                    'index': {
                                        7: {
                                            'tep_id': '0xffffffff',
                                            'df_role': '(P)',
                                            'nexthop': '192.168.0.3',
                                            'label': '29226',
                                        },
                                        8: {
                                            'tep_id': '0x00000000',
                                            'df_role': '(B)',
                                            'nexthop': '192.168.0.4',
                                            'label': '29353',
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    golden_output2 = {'execute.return_value': '''
    Device#show evpn internal-label
    Fri Jun 28 13:42:20.616 EST

    VPN-ID     Encap  Ethernet Segment Id         EtherTag     Label
    ---------- ------ --------------------------- ----------   --------
    1          MPLS   0055.5555.5555.5555.5555    0            None

    1          MPLS   0055.5555.5555.5555.5555    1            29348
    Summary pathlist:
    0xffffffff (P) 192.168.0.3                              29213

    1          MPLS   0055.5555.5555.5555.5555    3            29352
    Summary pathlist:
    0xffffffff (P) 192.168.0.3                              29224

    1          MPLS   0088.8888.8888.8888.8888    0            None

    1          MPLS   0088.8888.8888.8888.8888    1            29350
    Summary pathlist:
    0xffffffff (P) 192.168.0.4                              29340

    1          MPLS   0088.8888.8888.8888.8888    2            29349
    Summary pathlist:
    0xffffffff (P) 192.168.0.3                              29216
    0x00000000 (B) 192.168.0.4                              29341

    1          MPLS   0088.8888.8888.8888.8888    3            29355
    Summary pathlist:
    0xffffffff (P) 192.168.0.4                              29352

    1          MPLS   0088.8888.8888.8888.8888    4            29354
    Summary pathlist:
    0xffffffff (P) 192.168.0.3                              29226
    0x00000000 (B) 192.168.0.4                              29353
    '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowEvpnInternalLabel(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output1)
        obj = ShowEvpnInternalLabel(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output1)
    
    def test_golden2(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output2)
        obj = ShowEvpnInternalLabel(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output2)

# ===================================================
#  Unit test for 'show evpn ethernet-segment private'
# ===================================================
class TestSShowEvpnEthernetSegmentPrivate(unittest.TestCase):

    '''Unit test for 'show evpn ethernet-segment private'''
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output1 = {
        'segment_id': {
            '0001.0000.aaab.0000.0003': {
                'interface': {
                    'Bundle-Ether3': {
                        'next_hops': ['67.70.219.84<'],
                        'es_to_bgp_gates': 'M',
                        'es_to_l2fib_gates': 'Ready',
                        'main_port': {
                            'interface': 'Bundle-Ether3',
                            'interface_mac': '00c1.6428.7cec',
                            'if_handle': '0x080002a0',
                            'state': 'Down',
                            'redundancy': 'Not Defined',
                        },
                        'esi': {
                            'type': 0,
                            'value': '01.0000.aaab.0000.0003',
                        },
                        'es_import_rt': 'aaab.0000.0003 (Local)',
                        'source_mac': '0000.0000.0000 (N/A)',
                        'topology': {
                            'operational': 'SH',
                            'configured': 'All-active (AApF) (default)',
                        },
                        'service_carving': 'Auto-selection',
                        'peering_details': ['67.70.219.84[MOD:P:00][1]'],
                        'service_carving_results': {
                            'forwarders': 1,
                            'permanent': 0,
                            'elected': {
                                'num_of_total': 0,
                            },
                            'not_elected': {
                                'num_of_total': 1,
                            },
                        },
                        'mac_flushing_mode': 'STP-TCN',
                        'peering_timer': '3    (global)',
                        'recovery_timer': '30   (global)',
                        'carving_timer': '0    (global)',
                        'local_shg_label': '100564',
                        'remote_shg_labels': {
                            '0': {
                            },
                        },
                        'object': {
                            'EVPN ES': {
                                'base_info': {
                                    'version': '0xdbdb0007',
                                    'flags': '0x0',
                                    'type': 7,
                                    'reserved': 0,
                                },
                                'num_events': 55,
                                'event_history': {
                                    1: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'ES DB Bind',
                                        'flag_1': '00000000',
                                        'flag_2': '00000001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    2: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Create',
                                        'flag_1': '00000000',
                                        'flag_2': '00000001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    3: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API Config Ifname Add',
                                        'flag_1': '00000000',
                                        'flag_2': '00000001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    4: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Peering Sequence',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    5: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API Config Local RT',
                                        'flag_1': '00000000',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    6: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'ES DB Bind',
                                        'flag_1': '00000000',
                                        'flag_2': '00010001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    7: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action L2FIB Instance Upd',
                                        'flag_1': '00000000',
                                        'flag_2': 'c1400000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    8: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Peering Sequence',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    9: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API Config ESI complete',
                                        'flag_1': '00000000',
                                        'flag_2': '00000003',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    10: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API Provision',
                                        'flag_1': '00000000',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    11: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    12: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    13: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    14: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    15: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    16: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    17: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    18: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    19: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    20: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    21: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    22: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    23: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    24: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    25: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    26: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    27: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    28: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    29: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    30: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    31: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    32: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    33: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    34: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    35: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    36: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    37: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    38: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    39: {
                                        'time': 'Aug 27 09:46:04.160',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c014',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    40: {
                                        'time': 'Aug 27 09:46:04.160',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0140000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    41: {
                                        'time': 'Aug 27 09:49:15.648',
                                        'event': 'ES DB Unbind - tid',
                                        'flag_1': '00100001',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    42: {
                                        'time': 'Aug 27 09:49:15.648',
                                        'event': 'Action Create RT',
                                        'flag_1': '00000000',
                                        'flag_2': 'aaab0000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    43: {
                                        'time': 'Aug 27 09:49:15.648',
                                        'event': 'Action Advertise RT',
                                        'flag_1': '00000000',
                                        'flag_2': '00010001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    44: {
                                        'time': 'Aug 27 09:49:15.648',
                                        'event': 'Action Peering Sequence',
                                        'flag_1': '00000000',
                                        'flag_2': 'c8040000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    45: {
                                        'time': 'Aug 27 09:49:15.648',
                                        'event': 'API BP Ifname update',
                                        'flag_1': '00000000',
                                        'flag_2': '03e803e8',
                                        'code_1': 'M',
                                        'code_2': '-',
                                    },
                                    46: {
                                        'time': 'Aug 27 09:49:15.648',
                                        'event': 'Action Peering Sequence',
                                        'flag_1': '00000000',
                                        'flag_2': 'c8040000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    47: {
                                        'time': 'Aug 27 09:49:15.648',
                                        'event': 'API BGP RID update',
                                        'flag_1': 'a5138011',
                                        'flag_2': '00011043',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    48: {
                                        'time': 'Aug 27 09:49:16.160',
                                        'event': 'Action EAD/EVI',
                                        'flag_1': '00000add',
                                        'flag_2': '000103e8',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    49: {
                                        'time': 'Aug 27 09:49:16.160',
                                        'event': 'Action Peering Sequence',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0040000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    50: {
                                        'time': 'Aug 27 09:49:16.160',
                                        'event': 'API Recv LSD Local SHGLabel',
                                        'flag_1': '00000000',
                                        'flag_2': '000188d4',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    51: {
                                        'time': 'Aug 27 09:49:16.160',
                                        'event': 'Action EAD/EVI',
                                        'flag_1': '00000add',
                                        'flag_2': '000103e8',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    52: {
                                        'time': 'Aug 27 09:49:16.160',
                                        'event': 'Action Peering Sequence',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0040000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    53: {
                                        'time': 'Aug 27 09:49:16.160',
                                        'event': 'API BGP mark / sweep',
                                        'flag_1': '00de1e7e',
                                        'flag_2': '00000001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    54: {
                                        'time': 'Aug 27 09:49:37.152',
                                        'event': 'Action L2FIB MP Info Upd',
                                        'flag_1': '00000000',
                                        'flag_2': '00000001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    55: {
                                        'time': 'Aug 27 09:49:37.152',
                                        'event': 'API L2FIB Replay',
                                        'flag_1': '00000000',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                },
                            },
                        },
                        'es_statistics': {
                            'RT': {
                                'adv_cnt': 1,
                                'adv_last_time': '27/08 09:49:15.582',
                                'adv_last_arg': '00000000',
                                'wdw_cnt': 0,
                                'wdw_last_arg': '00000000',
                            },
                            'LocalBMAC': {
                                'adv_cnt': 0,
                                'adv_last_arg': '00000000',
                                'wdw_cnt': 0,
                                'wdw_last_arg': '00000000',
                            },
                            'ESI': {
                                'adv_cnt': 0,
                                'adv_last_arg': '00000000',
                                'wdw_cnt': 0,
                                'wdw_last_arg': '00000000',
                            },
                            'EAD/ES': {
                                'adv_cnt': 0,
                                'adv_last_arg': '00000000',
                                'wdw_cnt': 0,
                                'wdw_last_arg': '00000000',
                            },
                            'EAD/EVI': {
                                'adv_cnt': 2,
                                'adv_last_time': '27/08 09:49:16.091',
                                'adv_last_arg': '000003e8',
                                'wdw_cnt': 0,
                                'wdw_last_arg': '00000000',
                            },
                            'MST-AG VPW': {
                                'adv_cnt': 0,
                                'adv_last_arg': '00000000',
                                'wdw_cnt': 0,
                                'wdw_last_arg': '00000000',
                            },
                            'DF ElectFW': {
                                'adv_cnt': 1,
                                'adv_last_time': '27/08 09:49:15.582',
                                'adv_last_arg': '00000000',
                            },
                            'UpdateMAC': {
                                'adv_cnt': 0,
                                'adv_last_arg': '00000000',
                            },
                            'MacFlushPE': {
                                'adv_cnt': 0,
                                'adv_last_arg': '00000000',
                            },
                            'MacFlushCE': {
                                'adv_cnt': 0,
                                'adv_last_arg': '00000000',
                            },
                            'Instance': {
                                'adv_cnt': 0,
                                'adv_last_arg': '00000000',
                                'wdw_cnt': 0,
                                'wdw_last_arg': '00000000',
                            },
                            'MP Info': {
                                'adv_cnt': 1,
                                'adv_last_time': '27/08 09:49:37.024',
                                'adv_last_arg': '00000000',
                                'wdw_cnt': 0,
                                'wdw_last_arg': '00000000',
                            },
                        },
                        'diagnostic_esi': 'N/A',
                        'interface_name': 'N/A',
                        'diagnostic_ifh': '0x00000000',
                        'diagnostic_flag': '0x00000043',
                        'diagnosticesrt': '0000.0000.0000',
                        'port_key': '0x000088d4',
                        'mac_winner': 1,
                        'number_of_evis': 1,
                        'rt_advertised': 1,
                        'esi_advertised': 0,
                        'msti_state_mask': '0x0000',
                        'hrw_msti_set': '0x3',
                        'es_ead_pulse': 0,
                        'mp_advertised': 1,
                        'nve_anycastvtep': 0,
                        'nve_ingrreplic': 0,
                        'peering_done': 0,
                        'carving_done': 1,
                        'inval/redundfwd': '0x00000000/0x00000000',
                        'inval/redund_nh': '0x00000000/0x00000000',
                        'chkpt_objid': '0x0',
                        'es_ead_update': {
                            'num_rds': 0,
                        },
                    },
                },
            },
            '0001.0000.aaab.0000.0004': {
                'interface': {
                    'Bundle-Ether4': {
                        'next_hops': ['67.70.219.84<'],
                        'es_to_bgp_gates': 'Ready',
                        'es_to_l2fib_gates': 'Ready',
                        'main_port': {
                            'interface': 'Bundle-Ether4',
                            'interface_mac': '00c1.6428.7ceb',
                            'if_handle': '0x080002e0',
                            'state': 'Up',
                            'redundancy': 'Not Defined',
                        },
                        'esi': {
                            'type': 0,
                            'value': '01.0000.aaab.0000.0004',
                        },
                        'es_import_rt': 'aaab.0000.0004 (Local)',
                        'source_mac': '0000.0000.0000 (N/A)',
                        'topology': {
                            'operational': 'SH',
                            'configured': 'All-active (AApF) (default)',
                        },
                        'service_carving': 'Auto-selection',
                        'peering_details': ['67.70.219.84[MOD:P:00][1]'],
                        'service_carving_results': {
                            'forwarders': 1,
                            'permanent': 0,
                            'elected': {
                                'num_of_total': 1,
                            },
                            'not_elected': {
                                'num_of_total': 0,
                            },
                        },
                        'mac_flushing_mode': 'STP-TCN',
                        'peering_timer': '3    (global)',
                        'recovery_timer': '30   (global)',
                        'carving_timer': '0    (global)',
                        'local_shg_label': '100565',
                        'remote_shg_labels': {
                            '0': {
                            },
                        },
                        'object': {
                            'EVPN ES': {
                                'base_info': {
                                    'version': '0xdbdb0007',
                                    'flags': '0x0',
                                    'type': 7,
                                    'reserved': 0,
                                },
                                'num_events': 64,
                                'event_history': {
                                    56: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API Config Ifname Add',
                                        'flag_1': '00000000',
                                        'flag_2': '00000001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    57: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Peering Sequence',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    58: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API Config Local RT',
                                        'flag_1': '00000000',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    59: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'ES DB Bind',
                                        'flag_1': '00000000',
                                        'flag_2': '00010001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    60: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action L2FIB Instance Upd',
                                        'flag_1': '00000000',
                                        'flag_2': 'c1400000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    61: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Peering Sequence',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    62: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API Config ESI complete',
                                        'flag_1': '00000000',
                                        'flag_2': '00000003',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    63: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API Provision',
                                        'flag_1': '00000000',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    64: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    65: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    66: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    67: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    68: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    69: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    70: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    71: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    72: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    73: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    74: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    75: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    76: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    77: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    78: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    79: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    80: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    81: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    82: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    83: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    84: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    85: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    86: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    87: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    88: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    89: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    90: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c016',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    91: {
                                        'time': 'Aug 27 09:44:15.616',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0160000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    92: {
                                        'time': 'Aug 27 09:46:04.160',
                                        'event': 'Action Advertise MAC',
                                        'flag_1': '00000000',
                                        'flag_2': '0000c014',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    93: {
                                        'time': 'Aug 27 09:46:04.160',
                                        'event': 'API BGP Replay',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0140000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    94: {
                                        'time': 'Aug 27 09:49:15.648',
                                        'event': 'ES DB Unbind - tid',
                                        'flag_1': '00100001',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    95: {
                                        'time': 'Aug 27 09:49:15.648',
                                        'event': 'Action Create RT',
                                        'flag_1': '00000000',
                                        'flag_2': 'aaab0000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    96: {
                                        'time': 'Aug 27 09:49:15.648',
                                        'event': 'Action Advertise RT',
                                        'flag_1': '00000000',
                                        'flag_2': '00010001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    97: {
                                        'time': 'Aug 27 09:49:15.648',
                                        'event': 'Action Peering Sequence',
                                        'flag_1': '00000000',
                                        'flag_2': 'c8040000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    98: {
                                        'time': 'Aug 27 09:49:15.648',
                                        'event': 'API BP Ifname update',
                                        'flag_1': '00000000',
                                        'flag_2': '03e803e8',
                                        'code_1': 'M',
                                        'code_2': '-',
                                    },
                                    99: {
                                        'time': 'Aug 27 09:49:15.648',
                                        'event': 'Action Peering Sequence',
                                        'flag_1': '00000000',
                                        'flag_2': 'c8040000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    100: {
                                        'time': 'Aug 27 09:49:15.648',
                                        'event': 'API BGP RID update',
                                        'flag_1': 'a5138011',
                                        'flag_2': '00011043',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    101: {
                                        'time': 'Aug 27 09:49:16.160',
                                        'event': 'Action EAD/EVI',
                                        'flag_1': '00000add',
                                        'flag_2': '000103e8',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    102: {
                                        'time': 'Aug 27 09:49:16.160',
                                        'event': 'Action Peering Sequence',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0040000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    103: {
                                        'time': 'Aug 27 09:49:16.160',
                                        'event': 'API Recv LSD Local SHGLabel',
                                        'flag_1': '00000000',
                                        'flag_2': '000188d5',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    104: {
                                        'time': 'Aug 27 09:49:16.160',
                                        'event': 'Action EAD/EVI',
                                        'flag_1': '00000add',
                                        'flag_2': '000103e8',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    105: {
                                        'time': 'Aug 27 09:49:16.160',
                                        'event': 'Action Peering Sequence',
                                        'flag_1': '00000000',
                                        'flag_2': 'c0040000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    106: {
                                        'time': 'Aug 27 09:49:16.160',
                                        'event': 'API BGP mark / sweep',
                                        'flag_1': '00de1e7e',
                                        'flag_2': '00000001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    107: {
                                        'time': 'Aug 27 09:49:37.152',
                                        'event': 'Action L2FIB MP Info Upd',
                                        'flag_1': '00000000',
                                        'flag_2': '00000001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    108: {
                                        'time': 'Aug 27 09:49:37.152',
                                        'event': 'API L2FIB Replay',
                                        'flag_1': '00000000',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    109: {
                                        'time': 'Aug 27 09:49:41.760',
                                        'event': 'Action L2FIB Instance Upd',
                                        'flag_1': '000f0001',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    110: {
                                        'time': 'Aug 27 09:49:41.760',
                                        'event': 'Action L2FIB MP Info Upd',
                                        'flag_1': '00000000',
                                        'flag_2': '00000001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    111: {
                                        'time': 'Aug 27 09:49:41.760',
                                        'event': 'Action Advertise ESI',
                                        'flag_1': '00000000',
                                        'flag_2': '00010001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    112: {
                                        'time': 'Aug 27 09:49:41.760',
                                        'event': 'Action EAD/ES',
                                        'flag_1': '00000001',
                                        'flag_2': '000188d5',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    113: {
                                        'time': 'Aug 27 09:49:41.760',
                                        'event': 'Action EAD/EVI',
                                        'flag_1': '00000add',
                                        'flag_2': '000103e8',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    114: {
                                        'time': 'Aug 27 09:49:41.760',
                                        'event': 'Action Peering Sequence',
                                        'flag_1': '00000000',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    115: {
                                        'time': 'Aug 27 09:49:41.760',
                                        'event': 'API IM MP | AToM state',
                                        'flag_1': '00000000',
                                        'flag_2': '00320002',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    116: {
                                        'time': 'Aug 27 09:49:41.760',
                                        'event': 'Action EAD/ES',
                                        'flag_1': '00000add',
                                        'flag_2': '000b89d5',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    117: {
                                        'time': 'Aug 27 09:49:44.832',
                                        'event': 'Action L2FIB Instance Upd',
                                        'flag_1': '000f7fff',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    118: {
                                        'time': 'Aug 27 09:49:44.832',
                                        'event': 'Action L2FIB MP Info Upd',
                                        'flag_1': '00000000',
                                        'flag_2': '00000001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    119: {
                                        'time': 'Aug 27 09:49:44.832',
                                        'event': 'API Peer Timer Expiry',
                                        'flag_1': '00000000',
                                        'flag_2': '00000001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                },
                            },
                        },
                        'es_statistics': {
                            'RT': {
                                'adv_cnt': 1,
                                'adv_last_time': '27/08 09:49:15.582',
                                'adv_last_arg': '00000000',
                                'wdw_cnt': 0,
                                'wdw_last_arg': '00000000',
                            },
                            'LocalBMAC': {
                                'adv_cnt': 0,
                                'adv_last_arg': '00000000',
                                'wdw_cnt': 0,
                                'wdw_last_arg': '00000000',
                            },
                            'ESI': {
                                'adv_cnt': 1,
                                'adv_last_time': '27/08 09:49:41.604',
                                'adv_last_arg': '00000001',
                                'wdw_cnt': 0,
                                'wdw_last_arg': '00000000',
                            },
                            'EAD/ES': {
                                'adv_cnt': 1,
                                'adv_last_time': '27/08 09:49:41.606',
                                'adv_last_arg': '0000000a',
                                'wdw_cnt': 0,
                                'wdw_last_arg': '00000000',
                            },
                            'EAD/EVI': {
                                'adv_cnt': 3,
                                'adv_last_time': '27/08 09:49:41.604',
                                'adv_last_arg': '000003e8',
                                'wdw_cnt': 0,
                                'wdw_last_arg': '00000000',
                            },
                            'MST-AG VPW': {
                                'adv_cnt': 0,
                                'adv_last_arg': '00000000',
                                'wdw_cnt': 0,
                                'wdw_last_arg': '00000000',
                            },
                            'DF ElectFW': {
                                'adv_cnt': 1,
                                'adv_last_time': '27/08 09:49:15.582',
                                'adv_last_arg': '00000000',
                            },
                            'UpdateMAC': {
                                'adv_cnt': 0,
                                'adv_last_arg': '00000000',
                            },
                            'MacFlushPE': {
                                'adv_cnt': 0,
                                'adv_last_arg': '00000000',
                            },
                            'MacFlushCE': {
                                'adv_cnt': 0,
                                'adv_last_arg': '00000000',
                            },
                            'Instance': {
                                'adv_cnt': 2,
                                'adv_last_time': '27/08 09:49:44.606',
                                'adv_last_arg': '00007fff',
                                'wdw_cnt': 0,
                                'wdw_last_arg': '00000000',
                            },
                            'MP Info': {
                                'adv_cnt': 3,
                                'adv_last_time': '27/08 09:49:44.606',
                                'adv_last_arg': '00000000',
                                'wdw_cnt': 0,
                                'wdw_last_arg': '00000000',
                            },
                        },
                        'diagnostic_esi': 'N/A',
                        'interface_name': 'N/A',
                        'diagnostic_ifh': '0x00000000',
                        'diagnostic_flag': '0x00000043',
                        'diagnosticesrt': '0000.0000.0000',
                        'port_key': '0x000088d5',
                        'mac_winner': 1,
                        'number_of_evis': 1,
                        'rt_advertised': 1,
                        'esi_advertised': 1,
                        'msti_state_mask': '0x7fff',
                        'hrw_msti_set': '0x3',
                        'es_ead_pulse': 0,
                        'mp_advertised': 1,
                        'nve_anycastvtep': 0,
                        'nve_ingrreplic': 0,
                        'peering_done': 1,
                        'carving_done': 1,
                        'inval/redundfwd': '0x00000000/0x00000000',
                        'inval/redund_nh': '0x00000000/0x00000000',
                        'chkpt_objid': '0x40002f18',
                        'msti_mask': '0x7fff',
                        'es_ead_update': {
                            'num_rds': 1,
                            'rd': {
                                '67.70.219.84:1': {
                                    'num_rts': 1,
                                    'rt_list': '4:1000',
                                },
                            },
                        },
                    },
                },
            },
            'N/A': {
                'interface': {
                    'GigabitEthernet0/0/0/12': {
                        'next_hops': ['67.70.219.84<'],
                        'es_to_bgp_gates': 'Ready',
                        'es_to_l2fib_gates': 'Ready',
                        'main_port': {
                            'interface': 'GigabitEthernet0/0/0/12',
                            'interface_mac': '00c1.641f.6048',
                            'if_handle': '0x000005c0',
                            'state': 'Up',
                            'redundancy': 'Not Defined',
                        },
                        'esi_type': 'Invalid',
                        'es_import_rt': '0000.0000.0000 (Incomplete Configuration)',
                        'source_mac': '00c1.6428.7ce8 (PBB BSA, no ESI)',
                        'topology': {
                            'operational': 'SH',
                            'configured': 'Single-active (AApS) (default)',
                        },
                        'service_carving': 'Auto-selection',
                        'peering_details': ['67.70.219.84[MOD:P:00][1]'],
                        'service_carving_results': {
                            'forwarders': 1,
                            'permanent': 1,
                            'elected': {
                                'num_of_total': 0,
                            },
                            'not_elected': {
                                'num_of_total': 0,
                            },
                        },
                        'mac_flushing_mode': 'STP-TCN',
                        'peering_timer': '3    (global)',
                        'recovery_timer': '30   (global)',
                        'carving_timer': '0    (global)',
                        'local_shg_label': 'None',
                        'remote_shg_labels': {
                            '0': {
                            },
                        },
                        'object': {
                            'EVPN ES': {
                                'base_info': {
                                    'version': '0xdbdb0007',
                                    'flags': '0x0',
                                    'type': 7,
                                    'reserved': 0,
                                },
                                'num_events': 20,
                                'event_history': {
                                    120: {
                                        'time': 'Aug 27 09:49:15.648',
                                        'event': 'ES DB Bind',
                                        'flag_1': '00000000',
                                        'flag_2': '00000001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    121: {
                                        'time': 'Aug 27 09:49:15.648',
                                        'event': 'Create',
                                        'flag_1': '00000000',
                                        'flag_2': '00000001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    122: {
                                        'time': 'Aug 27 09:49:15.648',
                                        'event': 'Action L2FIB Instance Upd',
                                        'flag_1': '000f7fff',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    123: {
                                        'time': 'Aug 27 09:49:15.648',
                                        'event': 'Action Advertise RT',
                                        'flag_1': 'a5138016',
                                        'flag_2': '0000ffff',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    124: {
                                        'time': 'Aug 27 09:49:15.648',
                                        'event': 'Action L2FIB MP Info Upd',
                                        'flag_1': '00000000',
                                        'flag_2': '00000001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    125: {
                                        'time': 'Aug 27 09:49:15.648',
                                        'event': 'Action Peering Sequence',
                                        'flag_1': '00000000',
                                        'flag_2': '00008001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    126: {
                                        'time': 'Aug 27 09:49:15.648',
                                        'event': 'API BP Ifname update',
                                        'flag_1': '00000000',
                                        'flag_2': '08400000',
                                        'code_1': 'M',
                                        'code_2': '-',
                                    },
                                    127: {
                                        'time': 'Aug 27 09:49:15.648',
                                        'event': 'Action Advertise RT',
                                        'flag_1': 'a5138016',
                                        'flag_2': '0000ffff',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    128: {
                                        'time': 'Aug 27 09:49:15.648',
                                        'event': 'Action L2FIB MP Info Upd',
                                        'flag_1': '00000000',
                                        'flag_2': '00000001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    129: {
                                        'time': 'Aug 27 09:49:15.648',
                                        'event': 'Action Peering Sequence',
                                        'flag_1': '00000000',
                                        'flag_2': '00008001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    130: {
                                        'time': 'Aug 27 09:49:15.648',
                                        'event': 'API BGP RID update',
                                        'flag_1': 'a5138011',
                                        'flag_2': '00010040',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    131: {
                                        'time': 'Aug 27 09:49:16.160',
                                        'event': 'Action L2FIB MP Info Upd',
                                        'flag_1': '00000000',
                                        'flag_2': '00000001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    132: {
                                        'time': 'Aug 27 09:49:16.160',
                                        'event': 'API L2FIB Replay',
                                        'flag_1': '00000000',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    133: {
                                        'time': 'Aug 27 09:49:16.160',
                                        'event': 'API BGP mark / sweep',
                                        'flag_1': '00de1e7e',
                                        'flag_2': '00000001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    134: {
                                        'time': 'Aug 27 09:49:18.720',
                                        'event': 'Action L2FIB Instance Upd',
                                        'flag_1': '000f7fff',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    135: {
                                        'time': 'Aug 27 09:49:18.720',
                                        'event': 'Action L2FIB MP Info Upd',
                                        'flag_1': '00000000',
                                        'flag_2': '00000001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    136: {
                                        'time': 'Aug 27 09:49:18.720',
                                        'event': 'API Peer Timer Expiry',
                                        'flag_1': '00000000',
                                        'flag_2': '00000001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    137: {
                                        'time': 'Aug 27 09:49:37.152',
                                        'event': 'Action L2FIB Instance Upd',
                                        'flag_1': '000f7fff',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    138: {
                                        'time': 'Aug 27 09:49:37.152',
                                        'event': 'Action L2FIB MP Info Upd',
                                        'flag_1': '00000000',
                                        'flag_2': '00000001',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                    139: {
                                        'time': 'Aug 27 09:49:37.152',
                                        'event': 'API L2FIB Replay',
                                        'flag_1': '00000000',
                                        'flag_2': '00000000',
                                        'code_1': '-',
                                        'code_2': '-',
                                    },
                                },
                            },
                        },
                        'es_statistics': {
                            'RT': {
                                'adv_cnt': 2,
                                'adv_last_time': '27/08 09:49:15.583',
                                'adv_last_arg': 'a5138016',
                                'wdw_cnt': 0,
                                'wdw_last_arg': '00000000',
                            },
                            'LocalBMAC': {
                                'adv_cnt': 0,
                                'adv_last_arg': '00000000',
                                'wdw_cnt': 0,
                                'wdw_last_arg': '00000000',
                            },
                            'ESI': {
                                'adv_cnt': 0,
                                'adv_last_arg': '00000000',
                                'wdw_cnt': 0,
                                'wdw_last_arg': '00000000',
                            },
                            'EAD/ES': {
                                'adv_cnt': 0,
                                'adv_last_arg': '00000000',
                                'wdw_cnt': 0,
                                'wdw_last_arg': '00000000',
                            },
                            'EAD/EVI': {
                                'adv_cnt': 0,
                                'adv_last_arg': '00000000',
                                'wdw_cnt': 0,
                                'wdw_last_arg': '00000000',
                            },
                            'MST-AG VPW': {
                                'adv_cnt': 0,
                                'adv_last_arg': '00000000',
                                'wdw_cnt': 0,
                                'wdw_last_arg': '00000000',
                            },
                            'DF ElectFW': {
                                'adv_cnt': 0,
                                'adv_last_arg': '00000000',
                            },
                            'UpdateMAC': {
                                'adv_cnt': 0,
                                'adv_last_arg': '00000000',
                            },
                            'MacFlushPE': {
                                'adv_cnt': 0,
                                'adv_last_arg': '00000000',
                            },
                            'MacFlushCE': {
                                'adv_cnt': 0,
                                'adv_last_arg': '00000000',
                            },
                            'Instance': {
                                'adv_cnt': 3,
                                'adv_last_time': '27/08 09:49:37.025',
                                'adv_last_arg': '00007fff',
                                'wdw_cnt': 0,
                                'wdw_last_arg': '00000000',
                            },
                            'MP Info': {
                                'adv_cnt': 5,
                                'adv_last_time': '27/08 09:49:37.025',
                                'adv_last_arg': '00000000',
                                'wdw_cnt': 0,
                                'wdw_last_arg': '00000000',
                            },
                        },
                        'diagnostic_esi': 'N/A',
                        'interface_name': 'N/A',
                        'diagnostic_ifh': '0x00000000',
                        'diagnostic_flag': '0x00000040',
                        'diagnosticesrt': '0000.0000.0000',
                        'port_key': '0x00000001',
                        'mac_winner': 1,
                        'number_of_evis': 1,
                        'rt_advertised': 0,
                        'esi_advertised': 0,
                        'msti_state_mask': '0x7fff',
                        'hrw_msti_set': '0x3',
                        'es_ead_pulse': 0,
                        'mp_advertised': 1,
                        'nve_anycastvtep': 0,
                        'nve_ingrreplic': 0,
                        'peering_done': 1,
                        'carving_done': 1,
                        'inval/redundfwd': '0x00000000/0x00000000',
                        'inval/redund_nh': '0x00000000/0x00000000',
                        'chkpt_objid': '0x40002f58',
                        'msti_mask': '0x7fff',
                        'es_ead_update': {
                            'num_rds': 0,
                        },
                    },
                },
            },
        },
    }

    golden_output1 = {'execute.return_value': '''
        +++ Router: executing command 'show evpn ethernet-segment private' +++
        show evpn ethernet-segment private

        Mon Oct  7 16:18:27.805 EDT
        Legend:
        B   - No Forwarders EVPN-enabled,
        C   - Backbone Source MAC missing (PBB-EVPN),
        RT  - ES-Import Route Target missing,
        E   - ESI missing,
        H   - Interface handle missing,
        I   - Name (Interface or Virtual Access) missing,
        M   - Interface in Down state,
        O   - BGP End of Download missing,
        P   - Interface already Access Protected,
        Pf  - Interface forced single-homed,
        R   - BGP RID not received,
        S   - Interface in redundancy standby state,
        X   - ESI-extracted MAC Conflict
        SHG - No local split-horizon-group label allocated

        Ethernet Segment Id      Interface                          Nexthops (*stale)   
        ------------------------ ---------------------------------- --------------------
        0001.0000.aaab.0000.0003 BE3                                67.70.219.84<
        ES to BGP Gates   : M
        ES to L2FIB Gates : Ready
        Main port         :
            Interface name : Bundle-Ether3
        Interface MAC  : 00c1.6428.7cec
            IfHandle       : 0x080002a0
            State          : Down
            Redundancy     : Not Defined
        ESI type          : 0
            Value          : 01.0000.aaab.0000.0003
        ES Import RT      : aaab.0000.0003 (Local)
        Source MAC        : 0000.0000.0000 (N/A)
        Topology          :
            Operational    : SH
            Configured     : All-active (AApF) (default)
        Service Carving   : Auto-selection
        Peering Details   : 67.70.219.84[MOD:P:00][1]
        Service Carving Results:
            Forwarders     : 1
            Permanent      : 0
            Elected        : 0
            Not Elected    : 1
        MAC Flushing mode : STP-TCN
        Peering timer     : 3 sec [not running]
        Recovery timer    : 30 sec [not running]
        Carving timer     : 0 sec [not running]
        Local SHG label   : 100564
        Remote SHG labels : 0

        Object: EVPN ES
        Base info: version=0xdbdb0007, flags=0x0, type=7, reserved=0
        EVPN ES event history  [Num events: 55]
        ----------------------------------------------------------------------------
            Time                Event                         Flags      Flags      
            ====                =====                         =====      =====      
            Aug 27 09:44:15.616  ES DB Bind                   00000000, 00000001 -  - 
            Aug 27 09:44:15.616  Create                       00000000, 00000001 -  - 
            Aug 27 09:44:15.616 API Config Ifname Add         00000000, 00000001 -  - 
            Aug 27 09:44:15.616  Action Peering Sequence      00000000, c0160000 -  - 
            Aug 27 09:44:15.616 API Config Local RT           00000000, 00000000 -  - 
            Aug 27 09:44:15.616  ES DB Bind                   00000000, 00010001 -  - 
            Aug 27 09:44:15.616  Action L2FIB Instance Upd    00000000, c1400000 -  - 
            Aug 27 09:44:15.616  Action Peering Sequence      00000000, c0160000 -  - 
            Aug 27 09:44:15.616 API Config ESI complete       00000000, 00000003 -  - 
            Aug 27 09:44:15.616 API Provision                 00000000, 00000000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
            Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
            Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
        Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
            Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
            Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
            Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
            Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
            Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
            Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
            Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
            Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
            Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
            Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
            Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
        Aug 27 09:46:04.160  Action Advertise MAC         00000000, 0000c014 -  - 
            Aug 27 09:46:04.160 API BGP Replay                00000000, c0140000 -  - 
            Aug 27 09:49:15.648  ES DB Unbind - tid           00100001, 00000000 -  - 
            Aug 27 09:49:15.648  Action Create RT             00000000, aaab0000 -  - 
            Aug 27 09:49:15.648  Action Advertise RT          00000000, 00010001 -  - 
            Aug 27 09:49:15.648  Action Peering Sequence      00000000, c8040000 -  - 
            Aug 27 09:49:15.648 API BP Ifname update          00000000, 03e803e8 M  - 
            Aug 27 09:49:15.648  Action Peering Sequence      00000000, c8040000 -  - 
            Aug 27 09:49:15.648 API BGP RID update            a5138011, 00011043 -  - 
            Aug 27 09:49:16.160  Action EAD/EVI               00000add, 000103e8 -  - 
            Aug 27 09:49:16.160  Action Peering Sequence      00000000, c0040000 -  - 
            Aug 27 09:49:16.160 API Recv LSD Local SHGLabel   00000000, 000188d4 -  - 
            Aug 27 09:49:16.160  Action EAD/EVI               00000add, 000103e8 -  - 
            Aug 27 09:49:16.160  Action Peering Sequence      00000000, c0040000 -  - 
            Aug 27 09:49:16.160 API BGP mark / sweep          00de1e7e, 00000001 -  - 
            Aug 27 09:49:37.152  Action L2FIB MP Info Upd     00000000, 00000001 -  - 
            Aug 27 09:49:37.152 API L2FIB Replay              00000000, 00000000 -  - 
        ----------------------------------------------------------------------------
        EVPN ES Statistics
                    |Adv                             |Wdw                             
                    | Cnt Last Time          Last Arg| Cnt Last Time          Last Arg
                RT|   1 27/08 09:49:15.582 00000000|   0                    00000000
            LocalBMAC|   0                    00000000|   0                    00000000
            ESI|   0                    00000000|   0                    00000000
            EAD/ES|   0                    00000000|   0                    00000000
            EAD/EVI|   2 27/08 09:49:16.091 000003e8|   0                    00000000
        MST-AG VPW|   0                    00000000|   0                    00000000
        DF ElectFW|   1 27/08 09:49:15.582 00000000|
            UpdateMAC|   0                    00000000|
        MacFlushPE|   0                    00000000|
        MacFlushCE|   0                    00000000|
            Instance|   0                    00000000|   0                    00000000
            MP Info|   1 27/08 09:49:37.024 00000000|   0                    00000000
        ----------------------------------------------------------------------------
        Diagnostic ESI : N/A                     Interface Name : N/A
        Diagnostic Ifh : 0x00000000
        Diagnostic Flag: 0x00000043              DiagnosticES-RT: 0000.0000.0000
        Port Key       : 0x000088d4              MAC winner     : 1
        Number of EVIs : 1
        Recovery Timer : 30   (global)           Peering Timer  : 3    (global)  
        Carving Timer  : 0    (global)  
        RT Advertised  : 1                       ESI Advertised : 0
        MSTi state mask: 0x0000                  HRW MSTi Set   : 0x3
        ES EAD Pulse   : 0                       MP Advertised  : 1
        NVE AnycastVTEP: 0                       NVE Ingr-Replic: 0
        Peering Done   : 0                       Carving Done   : 1
            Inval/RedundFWD: 0x00000000/0x00000000
        Inval/Redund NH: 0x00000000/0x00000000
        Chkpt ObjId    : 0x0
        ES EAD Update     :
            Num RDs:       : 0

        0001.0000.aaab.0000.0004 BE4                                67.70.219.84<
        ES to BGP Gates   : Ready
        ES to L2FIB Gates : Ready
        Main port         :
            Interface name : Bundle-Ether4
            Interface MAC  : 00c1.6428.7ceb
            IfHandle       : 0x080002e0
            State          : Up
            Redundancy     : Not Defined
        ESI type          : 0
            Value          : 01.0000.aaab.0000.0004
        ES Import RT      : aaab.0000.0004 (Local)
        Source MAC        : 0000.0000.0000 (N/A)
        Topology          :
            Operational    : SH
            Configured     : All-active (AApF) (default)
        Service Carving   : Auto-selection
        Peering Details   : 67.70.219.84[MOD:P:00][1]
        Service Carving Results:
            Forwarders     : 1
            Permanent      : 0
            Elected        : 1
            Not Elected    : 0
        MAC Flushing mode : STP-TCN
        Peering timer     : 3 sec [not running]
        Recovery timer    : 30 sec [not running]
        Carving timer     : 0 sec [not running]
        Local SHG label   : 100565
        Remote SHG labels : 0

        Object: EVPN ES
        Base info: version=0xdbdb0007, flags=0x0, type=7, reserved=0
        EVPN ES event history  [Num events: 64]
        ----------------------------------------------------------------------------
            Time                Event                         Flags      Flags      
            ====                =====                         =====      =====      
            Aug 27 09:44:15.616 API Config Ifname Add         00000000, 00000001 -  - 
            Aug 27 09:44:15.616  Action Peering Sequence      00000000, c0160000 -  - 
            Aug 27 09:44:15.616 API Config Local RT           00000000, 00000000 -  - 
            Aug 27 09:44:15.616  ES DB Bind                   00000000, 00010001 -  - 
        Aug 27 09:44:15.616  Action L2FIB Instance Upd    00000000, c1400000 -  - 
            Aug 27 09:44:15.616  Action Peering Sequence      00000000, c0160000 -  - 
            Aug 27 09:44:15.616 API Config ESI complete       00000000, 00000003 -  - 
            Aug 27 09:44:15.616 API Provision                 00000000, 00000000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
            Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
            Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
            Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
            Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
            Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
            Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
            Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
            Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
            Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
        Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
            Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
            Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
            Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:44:15.616  Action Advertise MAC         00000000, 0000c016 -  - 
            Aug 27 09:44:15.616 API BGP Replay                00000000, c0160000 -  - 
            Aug 27 09:46:04.160  Action Advertise MAC         00000000, 0000c014 -  - 
            Aug 27 09:46:04.160 API BGP Replay                00000000, c0140000 -  - 
            Aug 27 09:49:15.648  ES DB Unbind - tid           00100001, 00000000 -  - 
            Aug 27 09:49:15.648  Action Create RT             00000000, aaab0000 -  - 
            Aug 27 09:49:15.648  Action Advertise RT          00000000, 00010001 -  - 
            Aug 27 09:49:15.648  Action Peering Sequence      00000000, c8040000 -  - 
            Aug 27 09:49:15.648 API BP Ifname update          00000000, 03e803e8 M  - 
            Aug 27 09:49:15.648  Action Peering Sequence      00000000, c8040000 -  - 
            Aug 27 09:49:15.648 API BGP RID update            a5138011, 00011043 -  - 
            Aug 27 09:49:16.160  Action EAD/EVI               00000add, 000103e8 -  - 
            Aug 27 09:49:16.160  Action Peering Sequence      00000000, c0040000 -  - 
            Aug 27 09:49:16.160 API Recv LSD Local SHGLabel   00000000, 000188d5 -  - 
            Aug 27 09:49:16.160  Action EAD/EVI               00000add, 000103e8 -  - 
            Aug 27 09:49:16.160  Action Peering Sequence      00000000, c0040000 -  - 
        Aug 27 09:49:16.160 API BGP mark / sweep          00de1e7e, 00000001 -  - 
            Aug 27 09:49:37.152  Action L2FIB MP Info Upd     00000000, 00000001 -  - 
            Aug 27 09:49:37.152 API L2FIB Replay              00000000, 00000000 -  - 
            Aug 27 09:49:41.760  Action L2FIB Instance Upd    000f0001, 00000000 -  - 
            Aug 27 09:49:41.760  Action L2FIB MP Info Upd     00000000, 00000001 -  - 
            Aug 27 09:49:41.760  Action Advertise ESI         00000000, 00010001 -  - 
            Aug 27 09:49:41.760  Action EAD/ES                00000001, 000188d5 -  - 
            Aug 27 09:49:41.760  Action EAD/EVI               00000add, 000103e8 -  - 
            Aug 27 09:49:41.760  Action Peering Sequence      00000000, 00000000 -  - 
            Aug 27 09:49:41.760 API IM MP | AToM state        00000000, 00320002 -  - 
            Aug 27 09:49:41.760  Action EAD/ES                00000add, 000b89d5 -  - 
            Aug 27 09:49:44.832  Action L2FIB Instance Upd    000f7fff, 00000000 -  - 
            Aug 27 09:49:44.832  Action L2FIB MP Info Upd     00000000, 00000001 -  - 
            Aug 27 09:49:44.832 API Peer Timer Expiry         00000000, 00000001 -  - 
        ----------------------------------------------------------------------------
        EVPN ES Statistics
                    |Adv                             |Wdw                             
                    | Cnt Last Time          Last Arg| Cnt Last Time          Last Arg
                RT|   1 27/08 09:49:15.582 00000000|   0                    00000000
            LocalBMAC|   0                    00000000|   0                    00000000
                ESI|   1 27/08 09:49:41.604 00000001|   0                    00000000
            EAD/ES|   1 27/08 09:49:41.606 0000000a|   0                    00000000
            EAD/EVI|   3 27/08 09:49:41.604 000003e8|   0                    00000000
            MST-AG VPW|   0                    00000000|   0                    00000000
        DF ElectFW|   1 27/08 09:49:15.582 00000000|
            UpdateMAC|   0                    00000000|
        MacFlushPE|   0                    00000000|
        MacFlushCE|   0                    00000000|
            Instance|   2 27/08 09:49:44.606 00007fff|   0                    00000000
            MP Info|   3 27/08 09:49:44.606 00000000|   0                    00000000
        ----------------------------------------------------------------------------
        Diagnostic ESI : N/A                     Interface Name : N/A
        Diagnostic Ifh : 0x00000000
        Diagnostic Flag: 0x00000043              DiagnosticES-RT: 0000.0000.0000
        Port Key       : 0x000088d5              MAC winner     : 1
        Number of EVIs : 1
        Recovery Timer : 30   (global)           Peering Timer  : 3    (global)  
        Carving Timer  : 0    (global)  
        RT Advertised  : 1                       ESI Advertised : 1
        MSTi state mask: 0x7fff                  HRW MSTi Set   : 0x3
        ES EAD Pulse   : 0                       MP Advertised  : 1
        NVE AnycastVTEP: 0                       NVE Ingr-Replic: 0
        Peering Done   : 1                       Carving Done   : 1
        Inval/RedundFWD: 0x00000000/0x00000000
        Inval/Redund NH: 0x00000000/0x00000000
        Chkpt ObjId    : 0x40002f18
            MSTi Mask      : 0x7fff
        ES EAD Update     :
            Num RDs:       : 1

            RD: 67.70.219.84:1, Num RTs: 1      RT List:
                4:1000, 
        N/A                      Gi0/0/0/12                         67.70.219.84<
        ES to BGP Gates   : Ready
        ES to L2FIB Gates : Ready
        Main port         :
            Interface name : GigabitEthernet0/0/0/12
            Interface MAC  : 00c1.641f.6048
            IfHandle       : 0x000005c0
            State          : Up
            Redundancy     : Not Defined
        ESI type          : Invalid
        ES Import RT      : 0000.0000.0000 (Incomplete Configuration)
        Source MAC        : 00c1.6428.7ce8 (PBB BSA, no ESI)
        Topology          :
            Operational    : SH
            Configured     : Single-active (AApS) (default)
        Service Carving   : Auto-selection
        Peering Details   : 67.70.219.84[MOD:P:00][1]
        Service Carving Results:
            Forwarders     : 1
            Permanent      : 1
            Elected        : 0
            Not Elected    : 0
        MAC Flushing mode : STP-TCN
        Peering timer     : 3 sec [not running]
        Recovery timer    : 30 sec [not running]
        Carving timer     : 0 sec [not running]
        Local SHG label   : None
        Remote SHG labels : 0

        Object: EVPN ES
        Base info: version=0xdbdb0007, flags=0x0, type=7, reserved=0
        EVPN ES event history  [Num events: 20]
        ----------------------------------------------------------------------------
            Time                Event                         Flags      Flags      
            ====                =====                         =====      =====      
            Aug 27 09:49:15.648  ES DB Bind                   00000000, 00000001 -  - 
            Aug 27 09:49:15.648  Create                       00000000, 00000001 -  - 
            Aug 27 09:49:15.648  Action L2FIB Instance Upd    000f7fff, 00000000 -  - 
            Aug 27 09:49:15.648  Action Advertise RT          a5138016, 0000ffff -  - 
            Aug 27 09:49:15.648  Action L2FIB MP Info Upd     00000000, 00000001 -  - 
        Aug 27 09:49:15.648  Action Peering Sequence      00000000, 00008001 -  - 
            Aug 27 09:49:15.648 API BP Ifname update          00000000, 08400000 M  - 
            Aug 27 09:49:15.648  Action Advertise RT          a5138016, 0000ffff -  - 
            Aug 27 09:49:15.648  Action L2FIB MP Info Upd     00000000, 00000001 -  - 
            Aug 27 09:49:15.648  Action Peering Sequence      00000000, 00008001 -  - 
            Aug 27 09:49:15.648 API BGP RID update            a5138011, 00010040 -  - 
            Aug 27 09:49:16.160  Action L2FIB MP Info Upd     00000000, 00000001 -  - 
            Aug 27 09:49:16.160 API L2FIB Replay              00000000, 00000000 -  - 
            Aug 27 09:49:16.160 API BGP mark / sweep          00de1e7e, 00000001 -  - 
            Aug 27 09:49:18.720  Action L2FIB Instance Upd    000f7fff, 00000000 -  - 
            Aug 27 09:49:18.720  Action L2FIB MP Info Upd     00000000, 00000001 -  - 
            Aug 27 09:49:18.720 API Peer Timer Expiry         00000000, 00000001 -  - 
            Aug 27 09:49:37.152  Action L2FIB Instance Upd    000f7fff, 00000000 -  - 
            Aug 27 09:49:37.152  Action L2FIB MP Info Upd     00000000, 00000001 -  - 
            Aug 27 09:49:37.152 API L2FIB Replay              00000000, 00000000 -  - 
        ----------------------------------------------------------------------------
        EVPN ES Statistics
                    |Adv                             |Wdw                             
                    | Cnt Last Time          Last Arg| Cnt Last Time          Last Arg
                RT|   2 27/08 09:49:15.583 a5138016|   0                    00000000
            LocalBMAC|   0                    00000000|   0                    00000000
                ESI|   0                    00000000|   0                    00000000
            EAD/ES|   0                    00000000|   0                    00000000
        EAD/EVI|   0                    00000000|   0                    00000000
        MST-AG VPW|   0                    00000000|   0                    00000000
        DF ElectFW|   0                    00000000|
            UpdateMAC|   0                    00000000|
        MacFlushPE|   0                    00000000|
        MacFlushCE|   0                    00000000|
            Instance|   3 27/08 09:49:37.025 00007fff|   0                    00000000
            MP Info|   5 27/08 09:49:37.025 00000000|   0                    00000000
        ----------------------------------------------------------------------------
        Diagnostic ESI : N/A                     Interface Name : N/A
        Diagnostic Ifh : 0x00000000
        Diagnostic Flag: 0x00000040              DiagnosticES-RT: 0000.0000.0000
        Port Key       : 0x00000001              MAC winner     : 1
        Number of EVIs : 1
        Recovery Timer : 30   (global)           Peering Timer  : 3    (global)  
        Carving Timer  : 0    (global)  
        RT Advertised  : 0                       ESI Advertised : 0
        MSTi state mask: 0x7fff                  HRW MSTi Set   : 0x3
        ES EAD Pulse   : 0                       MP Advertised  : 1
        NVE AnycastVTEP: 0                       NVE Ingr-Replic: 0
        Peering Done   : 1                       Carving Done   : 1
        Inval/RedundFWD: 0x00000000/0x00000000
        Inval/Redund NH: 0x00000000/0x00000000
            Chkpt ObjId    : 0x40002f58
        MSTi Mask      : 0x7fff
        ES EAD Update     :
            Num RDs:       : 0

        Router#
        '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowEvpnEthernetSegmentPrivate(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output1)
        obj = ShowEvpnEthernetSegmentPrivate(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output1)

if __name__ == '__main__':
    unittest.main()