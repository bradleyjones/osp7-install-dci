__author__ = 'brdemers'

import step
import logging
import ncclient.manager as manager
import ncclient_snippets as snip

class SwitchConfigStep(step.Step):

    logger = logging.getLogger("switch_config_step")
    logger.setLevel(logging.DEBUG)

    def _edit_config(self, mgr_conn, command_snippet):
        confstr = snip.exec_conf_prefix + command_snippet + snip.exec_conf_postfix
        mgr_conn.edit_config(target='running', config=confstr)

    def execute(self, kargs):

        connection = manager.connect(host=kargs["switch_ssh_ip_address"],
                                     port=kargs["switch_ssh_port"],
                                     username=kargs["switch_username"],
                                     password=kargs["switch_password"],
                                     hostkey_verify=False,
                                     device_params={"name": "nexus"})
        try:
            for switchport in kargs["physical_ports"]:
                self._edit_config(connection, snip.cmd_port_trunk.format(type="ethernet",
                                                                         port=switchport['port'],
                                                                         native_vlan=switchport['native_vlan'],
                                                                         description=switchport['description'] ))
        finally:
            connection.close_session()


