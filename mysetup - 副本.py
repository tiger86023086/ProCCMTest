#my setup.py
from distutils.core import setup
import py2exe
import sys

sys.argv.append('py2exe')

py2exe_options={
      "includes":["PyQt5.sip",
                  "appdirs",
                  "packaging.specifiers",
                  "packaging.requirements",
                  "can.interfaces.canalystii",
                  "pkg_resources.py2_warn",
                  "can.interfaces.ics_neovi",
                  "ics.structures.s_extended_data_flash_header",
                  "ics.structures.tag_options_open_neo_ex",
                  "ics.structures.tag_options_find_neo_ex",
                  "ics.structures.e_device_settings_type",
                  "ics.structures.e_disk_format",
                  "ics.structures.e_disk_layout",
                  "ics.structures.e_plasma_ion_vnet_channel_t",
                  "ics.structures.ethernet_network_status_t",
                  "ics.structures.s_phy_reg_pkt",
                  "ics.structures.s_phy_reg_pkt_clause22_mess",
                  "ics.structures.s_phy_reg_pkt_clause45_mess",
                  "ics.structures.s_phy_reg_pkt_hdr",
                  "ics.structures.s_pluto_avb_params_s",
                  "ics.structures.s_pluto_clock_sync_params_s",
                  "ics.structures.s_pluto_custom_params_s",
                  "ics.structures.s_pluto_l2_address_lookup_entry_s",
                  "ics.structures.s_pluto_l2_address_lookup_params_s",
                  "ics.structures.s_pluto_l2_forwarding_entry_s",
                  "ics.structures.s_pluto_l2_forwarding_entry_s",
                  "ics.structures.s_pluto_l2_policing_s",
                  "ics.structures.s_pluto_mac_config_s",
                  "ics.structures.s_pluto_ptp_params_s",
                  "ics.structures.s_pluto_retagging_entry_s"],
      "dll_excludes":["MSVCP90.dll",
                    "QT5CORE.DLL",
                    "PYTHON3.DLL",
                    "KERNEL32.DLL",
                    "VCRUNTIME140.DLL",
                    "icsneo40.dll"],
      "compressed":1,
      "optimize":2,
      "ascii":0,
      "bundle_files":3,
      }
setup(
      name = 'MainTest',
      version = '1.0',
      windows = [{'script':'MainTest 1.3.py','icon_resources':[(1,'car.ico')]}],
      #zipfile = None,
      options = {'py2exe':py2exe_options}
      )
#distutils.core.setup(windows=[{'script':'MainCreate.py','icon_resources':[(1,'timgCADXKVUY.ico')]}])