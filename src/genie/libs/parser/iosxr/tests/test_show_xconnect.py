# Python
import unittest
from unittest.mock import Mock
from ats.topology import Device

from genie.metaparser.util.exceptions import SchemaEmptyParserError

from genie.libs.parser.iosxr.show_xconnect import (ShowL2vpnXconnect,
                                                   ShowL2vpnXconnectDetail)


# ==================================================
#  Unit test for 'show l2vpn xconnect'
# ==================================================

class test_show_l2vpn_xconnect(unittest.TestCase):
    """Unit test for 'show l2vpn xconnect' """

    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
        'groups': {
            'Test_XCONN_Group': {
                'name': {
                    '1000': {
                        'status': 'DN',
                        'segment1': {
                            'GigabitEthernet0/0/0/5.1000': {
                                'status': 'UP',
                                'segment2': {
                                    '10.4.1.206       1000': {
                                        'status': 'DN',
                                    },
                                },
                            },
                        },
                    },
                    '2000': {
                        'status': 'DN',
                        'segment1': {
                            'GigabitEthernet0/0/0/5.2000': {
                                'status': 'UP',
                                'segment2': {
                                    '10.4.1.206       2000': {
                                        'status': 'DN',
                                    },
                                },
                            },
                        },
                    },
                },
            },
            'Test_XCONN_Group2': {
                'name': {
                    '3000': {
                        'status': 'UR',
                        'segment1': {
                            'GigabitEthernet0/0/0/5.3000': {
                                'status': 'UR',
                                'segment2': {
                                    '10.4.1.206       3000': {
                                        'status': 'DN',
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    golden_output = {'execute.return_value': '''
    XRv01_NUC# show l2vpn xconnect
    Legend: ST = State, UP = Up, DN = Down, AD = Admin Down, UR = Unresolved,
            SB = Standby, SR = Standby Ready, (PP) = Partially Programmed
     XConnect                   Segment 1                       Segment 2                
    Group      Name     ST   Description       ST   Description            ST
    ----------------------   --------------------   ---------------------------
    Test_XCONN_Group
               1000     DN   Gi0/0/0/5.1000    UP   10.4.1.206       1000   DN
    ---------------------------------------------------------------------------
    Test_XCONN_Group
               2000     DN   Gi0/0/0/5.2000    UP   10.4.1.206       2000   DN    
    ---------------------------------------------------------------------------
    Test_XCONN_Group2
               3000     UR   Gi0/0/0/5.3000    UR   10.4.1.206       3000   DN
    ---------------------------------------------------------------------------
        '''}

    golden_parsed_output2 = {
        'groups': {
            'L2TPV3_V4_XC_GRP': {
                'name': {
                    'L2TPV3_P2P_1': {
                        'status': 'UP',
                        'segment1': {
                            'GigabitEthernet0/2/0/1.2': {
                                'status': 'UP',
                                'segment2': {
                                    '26.26.26.26     100': {
                                        'status': 'UP',
                                    },
                                },
                            },
                        },
                    },
                    'L2TPV3_P2P_2': {
                        'status': 'UP',
                        'segment1': {
                            'GigabitEthernet0/2/0/1.3': {
                                'status': 'UP',
                                'segment2': {
                                    '26.26.26.26     200': {
                                        'status': 'UP',
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
    RP/0/RSP0/CPU0:router# show l2vpn xconnect
    Wed May 21 09:06:47.944 UTC
    Legend: ST = State, UP = Up, DN = Down, AD = Admin Down, UR = Unresolved,
            SB = Standby, SR = Standby Ready, (PP) = Partially Programmed

    XConnect                   Segment 1                       Segment 2                
    Group      Name       ST   Description            ST       Description            ST    
    ------------------------   -----------------------------   ---------------------------
    L2TPV3_V4_XC_GRP
            L2TPV3_P2P_1
                        UP   Gi0/2/0/1.2            UP       26.26.26.26     100    UP    
    --------------------------------------------------------------------------------------
    L2TPV3_V4_XC_GRP
            L2TPV3_P2P_2
                        UP   Gi0/2/0/1.3            UP       26.26.26.26     200    UP    
    --------------------------------------------------------------------------------------
        '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowL2vpnXconnect(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        obj = ShowL2vpnXconnect(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)
    
    def test_golden2(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output2)
        obj = ShowL2vpnXconnect(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output2)


# ==================================================
#  Unit test for 'show l2vpn xconnect detail'
# ==================================================

class test_show_l2vpn_xconnect_detail(unittest.TestCase):
    """Unit test for 'show l2vpn xconnect detail' """

    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
        'group': {
            'siva_xc': {
                'xc': {
                    'siva_p2p': {
                        'state': 'down',
                        'interworking': 'none',
                        'monitor_session': {
                            'pw-span-test': {
                                'state': 'configured',
                            },
                        },
                        'ac': {
                            'GigabitEthernet0/4/0/1': {
                                'state': 'up',
                                'type': 'Ethernet',
                                'mtu': 1500,
                                'xc_id': '0x5000001',
                                'interworking': 'none',
                                'msti': 0,
                                'statistics': {
                                    'packet_totals': {
                                        'send': 98,
                                    },
                                    'byte_totals': {
                                        'send': 20798,
                                    },
                                },
                            },
                        },
                        'pw': {
                            'neighbor': {
                                '10.1.1.1': {
                                    'id': 1,
                                    'state': 'down ( local ready )',
                                    'pw_class': 'not set',
                                    'xc_id': '0x5000001',
                                    'encapsulation': 'MPLS',
                                    'protocol': 'LDP',
                                    'type': 'Ethernet',
                                    'control_word': 'enabled',
                                    'interworking': 'none',
                                    'backup_disable_delay': 0,
                                    'sequencing': 'not set',
                                    'mpls': {
                                        'label': {
                                            'local': '30005',
                                            'remote': 'unknown',
                                        },
                                        'group_id': {
                                            'local': '0x5000300',
                                            'remote': '0x0',
                                        },
                                        'interface': {
                                            'local': 'GigabitEthernet0/4/0/1',
                                            'remote': 'unknown',
                                            'monitor_interface': {
                                                'local': 'pw-span-test',
                                                'remote': 'GigabitEthernet0/3/0/1',
                                            },
                                        },
                                        'mtu': {
                                            'local': '1500',
                                            'remote': 'unknown',
                                        },
                                        'control_word': {
                                            'local': 'enabled',
                                            'remote': 'unknown',
                                        },
                                        'pw_type': {
                                            'local': 'Ethernet',
                                            'remote': 'unknown',
                                        },
                                        'vccv_cv_type': {
                                            'local': '0x2',
                                            'remote': '0x0',
                                            'local_type': ['LSP ping verification'],
                                            'remote_type': ['none'],
                                        },
                                        'vccv_cc_type': {
                                            'local': '0x3',
                                            'remote': '0x0',
                                            'local_type': ['control word', 'router alert label'],
                                            'remote_type': ['none'],
                                        },
                                    },
                                    'create_time': '20/11/2007 21:45:06 (00:53:31 ago)',
                                    'last_time_status_changed': '20/11/2007 22:38:14 (00:00:23 ago)',
                                    'statistics': {
                                        'packet_totals': {
                                            'receive': 0,
                                        },
                                        'byte_totals': {
                                            'receive': 0,
                                        },
                                    },
                                },
                            },
                        },
                        'backup_pw': {
                            'neighbor': {
                                '10.2.2.2': {
                                    'id': 2,
                                    'state': 'up ( established )',
                                    'pw_class': 'not set',
                                    'xc_id': '0x0',
                                    'encapsulation': 'MPLS',
                                    'protocol': 'LDP',
                                    'type': 'Ethernet',
                                    'control_word': 'enabled',
                                    'interworking': 'none',
                                    'backup_disable_delay': 0,
                                    'sequencing': 'not set',
                                    'mpls': {
                                        'label': {
                                            'local': '30006',
                                            'remote': '16003',
                                        },
                                        'group_id': {
                                            'local': 'unassigned',
                                            'remote': '0x5000400',
                                        },
                                        'interface': {
                                            'local': 'unknown',
                                            'remote': 'GigabitEthernet0/4/0/2',
                                        },
                                        'mtu': {
                                            'local': '1500',
                                            'remote': '1500',
                                        },
                                        'control_word': {
                                            'local': 'enabled',
                                            'remote': 'enabled',
                                        },
                                        'pw_type': {
                                            'local': 'Ethernet',
                                            'remote': 'Ethernet',
                                        },
                                        'vccv_cv_type': {
                                            'local': '0x2',
                                            'remote': '0x2',
                                            'local_type': ['LSP ping verification'],
                                            'remote_type': ['LSP ping verification'],
                                        },
                                        'vccv_cc_type': {
                                            'local': '0x3',
                                            'remote': '0x3',
                                            'local_type': ['control word', 'router alert label'],
                                            'remote_type': ['control word', 'router alert label'],
                                        },
                                    },
                                    'create_time': '20/11/2007 21:45:44 (00:52:54 ago)',
                                    'last_time_status_changed': '20/11/2007 21:45:48 (00:52:49 ago)',
                                    'statistics': {
                                        'packet_totals': {
                                            'receive': 0,
                                        },
                                        'byte_totals': {
                                            'receive': 0,
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

    golden_output = {'execute.return_value': '''
    Group siva_xc, XC siva_p2p, state is down; Interworking none
      Monitor-Session: pw-span-test, state is configured
    AC: GigabitEthernet0/4/0/1, state is up
        Type Ethernet
        MTU 1500; XC ID 0x5000001; interworking none; MSTi 0
        Statistics:
        packet totals: send 98
        byte totals: send 20798
    PW: neighbor 10.1.1.1, PW ID 1, state is down ( local ready )
        PW class not set, XC ID 0x5000001
        Encapsulation MPLS, protocol LDP
        PW type Ethernet, control word enabled, interworking none
        PW backup disable delay 0 sec
        Sequencing not set
            MPLS         Local                          Remote                        
        ------------ ------------------------------ -----------------------------
        Label        30005                          unknown                       
        Group ID     0x5000300                      0x0                           
        Interface    GigabitEthernet0/4/0/1         unknown   
            Interface        pw-span-test                GigabitEthernet0/3/0/1
        MTU          1500                           unknown                       
        Control word enabled                        unknown                       
        PW type      Ethernet                       unknown                       
        VCCV CV type 0x2                            0x0                           
                                                    (none)                        
                    (LSP ping verification)                                      
        VCCV CC type 0x3                            0x0                           
                                                    (none)                        
                        (control word)                                               
                    (router alert label)                                         
        ------------ ------------------------------ -----------------------------
        Create time: 20/11/2007 21:45:06 (00:53:31 ago)
        Last time status changed: 20/11/2007 22:38:14 (00:00:23 ago)
        Statistics:
        packet totals: receive 0
        byte totals: receive 0

    Backup PW:
    PW: neighbor 10.2.2.2, PW ID 2, state is up ( established )
        Backup for neighbor 10.1.1.1 PW ID 1 ( active )
        PW class not set, XC ID 0x0
        Encapsulation MPLS, protocol LDP
        PW type Ethernet, control word enabled, interworking none
        PW backup disable delay 0 sec
        Sequencing not set
            MPLS         Local                          Remote                        
        ------------ ------------------------------ -----------------------------
        Label        30006                          16003                         
        Group ID     unassigned                     0x5000400                     
        Interface    unknown                        GigabitEthernet0/4/0/2        
        MTU          1500                           1500                          
        Control word enabled                        enabled                       
        PW type      Ethernet                       Ethernet                      
        VCCV CV type 0x2                            0x2                           
                    (LSP ping verification)        (LSP ping verification)       
        VCCV CC type 0x3                            0x3                           
                        (control word)                 (control word)                
                    (router alert label)           (router alert label)          
        ------------ ------------------------------ -----------------------------
        Backup PW for neighbor 10.1.1.1 PW ID 1
        Create time: 20/11/2007 21:45:44 (00:52:54 ago)
        Last time status changed: 20/11/2007 21:45:48 (00:52:49 ago)
        Statistics:
        packet totals: receive 0
        byte totals: receive 0
        '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowL2vpnXconnectDetail(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        obj = ShowL2vpnXconnectDetail(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)

if __name__ == '__main__':
    unittest.main()