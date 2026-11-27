from os_ken.base import app_manager
from os_ken.controller import ofp_event
from os_ken.controller.handler import CONFIG_DISPATCHER
from os_ken.controller.handler import MAIN_DISPATCHER
from os_ken.controller.handler import set_ev_cls
from os_ken.ofproto import ofproto_v1_3


class AdaptiveController(app_manager.OSKenApp):

    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(AdaptiveController, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.primary = True

    def add_flow(self, dp, priority, match, out_port):

        parser = dp.ofproto_parser

        actions = [
            parser.OFPActionOutput(out_port)
        ]

        instructions = [
            parser.OFPInstructionActions(
                dp.ofproto.OFPIT_APPLY_ACTIONS,
                actions
            )
        ]

        flow = parser.OFPFlowMod(
            datapath=dp,
            priority=priority,
            match=match,
            instructions=instructions
        )

        dp.send_msg(flow)

    def clear_flows(self, dp):

        parser = dp.ofproto_parser
        ofproto = dp.ofproto

        match = parser.OFPMatch()

        delete = parser.OFPFlowMod(
            datapath=dp,
            command=ofproto.OFPFC_DELETE,
            out_port=ofproto.OFPP_ANY,
            out_group=ofproto.OFPG_ANY,
            match=match
        )

        dp.send_msg(delete)

        actions = [
            parser.OFPActionOutput(
                ofproto.OFPP_CONTROLLER,
                ofproto.OFPCML_NO_BUFFER
            )
        ]

        instructions = [
            parser.OFPInstructionActions(
                ofproto.OFPIT_APPLY_ACTIONS,
                actions
            )
        ]

        miss = parser.OFPFlowMod(
            datapath=dp,
            priority=0,
            match=match,
            instructions=instructions
        )

        dp.send_msg(miss)

    def install_rules(self):

        for dp in self.datapaths.values():
            self.clear_flows(dp)

        if self.primary:
            self.logger.info("Installing PRIMARY path")
        else:
            self.logger.info("Installing BACKUP path")

        # S1
        dp = self.datapaths.get(1)

        if dp:
            self.add_flow(
                dp, 100,
                dp.ofproto_parser.OFPMatch(
                    eth_type=0x0806,
                    arp_spa="10.0.0.1",
                    arp_tpa="10.0.0.2"
                ),
                2 if self.primary else 3
            )

            self.add_flow(
                dp, 100,
                dp.ofproto_parser.OFPMatch(
                    eth_type=0x0800,
                    ipv4_src="10.0.0.1",
                    ipv4_dst="10.0.0.2"
                ),
                2 if self.primary else 3
            )

            self.add_flow(
                dp, 100,
                dp.ofproto_parser.OFPMatch(
                    eth_type=0x0806,
                    arp_spa="10.0.0.2",
                    arp_tpa="10.0.0.1"
                ),
                1
            )

            self.add_flow(
                dp, 100,
                dp.ofproto_parser.OFPMatch(
                    eth_type=0x0800,
                    ipv4_src="10.0.0.2",
                    ipv4_dst="10.0.0.1"
                ),
                1
            )

        # S2
        dp = self.datapaths.get(2)

        if dp and self.primary:
            self.add_flow(
                dp, 100,
                dp.ofproto_parser.OFPMatch(
                    eth_type=0x0806,
                    arp_spa="10.0.0.1",
                    arp_tpa="10.0.0.2"
                ),
                2
            )

            self.add_flow(
                dp, 100,
                dp.ofproto_parser.OFPMatch(
                    eth_type=0x0800,
                    ipv4_src="10.0.0.1",
                    ipv4_dst="10.0.0.2"
                ),
                2
            )

            self.add_flow(
                dp, 100,
                dp.ofproto_parser.OFPMatch(
                    eth_type=0x0806,
                    arp_spa="10.0.0.2",
                    arp_tpa="10.0.0.1"
                ),
                1
            )

            self.add_flow(
                dp, 100,
                dp.ofproto_parser.OFPMatch(
                    eth_type=0x0800,
                    ipv4_src="10.0.0.2",
                    ipv4_dst="10.0.0.1"
                ),
                1
            )

        # S3 - backup path
        dp = self.datapaths.get(3)

        if dp and not self.primary:
            self.add_flow(
                dp, 100,
                dp.ofproto_parser.OFPMatch(
                    eth_type=0x0806,
                    arp_spa="10.0.0.1",
                    arp_tpa="10.0.0.2"
                ),
                2
            )

            self.add_flow(
                dp, 100,
                dp.ofproto_parser.OFPMatch(
                    eth_type=0x0800,
                    ipv4_src="10.0.0.1",
                    ipv4_dst="10.0.0.2"
                ),
                2
            )

            self.add_flow(
                dp, 100,
                dp.ofproto_parser.OFPMatch(
                    eth_type=0x0806,
                    arp_spa="10.0.0.2",
                    arp_tpa="10.0.0.1"
                ),
                1
            )

            self.add_flow(
                dp, 100,
                dp.ofproto_parser.OFPMatch(
                    eth_type=0x0800,
                    ipv4_src="10.0.0.2",
                    ipv4_dst="10.0.0.1"
                ),
                1
            )

        # S4
        dp = self.datapaths.get(4)

        if dp:
            in_port = 1 if self.primary else 2

            self.add_flow(
                dp, 100,
                dp.ofproto_parser.OFPMatch(
                    eth_type=0x0806,
                    arp_spa="10.0.0.1",
                    arp_tpa="10.0.0.2"
                ),
                3
            )

            self.add_flow(
                dp, 100,
                dp.ofproto_parser.OFPMatch(
                    eth_type=0x0800,
                    ipv4_src="10.0.0.1",
                    ipv4_dst="10.0.0.2"
                ),
                3
            )

            self.add_flow(
                dp, 100,
                dp.ofproto_parser.OFPMatch(
                    eth_type=0x0806,
                    arp_spa="10.0.0.2",
                    arp_tpa="10.0.0.1"
                ),
                in_port
            )

            self.add_flow(
                dp, 100,
                dp.ofproto_parser.OFPMatch(
                    eth_type=0x0800,
                    ipv4_src="10.0.0.2",
                    ipv4_dst="10.0.0.1"
                ),
                in_port
            )

    @set_ev_cls(
        ofp_event.EventOFPSwitchFeatures,
        CONFIG_DISPATCHER
    )
    def switch_features_handler(self, ev):

        dp = ev.msg.datapath
        self.datapaths[dp.id] = dp

        self.logger.info(
            "Switch %s connected",
            dp.id
        )

        if len(self.datapaths) == 4:
            self.install_rules()

    @set_ev_cls(
        ofp_event.EventOFPPortStatus,
        MAIN_DISPATCHER
    )
    def port_status_handler(self, ev):

        dp = ev.msg.datapath
        port = ev.msg.desc.port_no
        state = ev.msg.desc.state

        if dp.id == 2 and port == 2:
            if state & dp.ofproto.OFPPS_LINK_DOWN:
                if self.primary:
                    self.primary = False
                    self.logger.info(
                        "S2-S4 FAILED - switching to BACKUP path"
                    )
                    self.install_rules()

            else:
                if not self.primary:
                    self.primary = True
                    self.logger.info(
                        "S2-S4 RECOVERED - switching to PRIMARY path"
                    )
                    self.install_rules()
