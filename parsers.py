# Parse raw OSPF neighbor information
# 生のOSPF隣接情報からネイバーのデバイスID、リモートIP、ローカルインターフェースを解析し、
# 利用できるデータ構造に整形する
def parse_ospf_neighbors(ospf_output):

    neighbors = []

    lines = ospf_output.splitlines()

    for line in lines[2:]:
        sections = line.split()

        if len(sections) >= 6:
            neighbor = {
                "neighbor_id": sections[0],
                "remote_ip": sections[4],
                "local_interface": sections[5].replace("GigabitEthernet", "Gi"),
            }

            neighbors.append(neighbor)

    return neighbors


# Parse raw interface information
# 生のインターフェースデータからインターフェースIDとIPアドレスを解析し、
# 利用できるデータ構造に整形する
def parse_interfaces(interface_output):

    interfaces = []

    lines = interface_output.splitlines()

    for line in lines[1:]:
        sections = line.split()

        if len(sections) >= 6:
            interface = {
                "interface": sections[0].replace("GigabitEthernet", "Gi"),
                "ip_address": sections[1],
            }

            interfaces.append(interface)

    return interfaces


# Parse raw VLAN information
# 生のVLANデータからVLANのID、VLAN名、状態、アクセスポートを解析し、
# 利用できるデータ構造に整形する
def parse_vlan_information(vlan_output):
    
    vlans = []

    lines = vlan_output.splitlines()

    for line in lines[4:-4]:
        sections = line.split()
        vlan = {
            "vlan": sections[0],
            "name": sections[1],
            "status": sections[2],
            "ports": sections[3:],
        }

        vlans.append(vlan)
    return vlans


# Parse raw trunk interface information
# 生のTRUNKデータからトランクインターフェースの状態とネイティブVLANを解析し、
# 利用できるデータ構造に整形する
def parse_trunks(trunk_output):

    trunks = []

    lines = trunk_output.splitlines()

    for line in lines:
        sections = line.split()

        if len(sections) >= 5 and sections[3] == "trunking":
            trunk = {
                "interface": sections[0],
                "status": sections[3],
                "native_vlan": sections[4],
            }

            trunks.append(trunk)

    return trunks


# Parse raw allowed VLAN information on trunk interfaces
# 生のTRUNKデータからトランクインターフェースに通信を許可されているVLANを解析し、
# 利用できるデータ構造に整形する
def parse_allowed_vlans(trunk_output):

    allowed_vlans = []

    lines = trunk_output.splitlines()

    for index, line in enumerate(lines):

        if line.startswith("Port        Vlans allowed on trunk"):
            allowed_vlan_start = index + 1
            while lines[allowed_vlan_start] != "":
                sections = lines[allowed_vlan_start].split()

                allowed_vlan = {
                    "interface": sections[0],
                    "allowed_vlans": sections[1].split(","),
                }

                allowed_vlans.append(allowed_vlan)

                allowed_vlan_start += 1

    return allowed_vlans


# Parse raw CDP neighbor information
# 生のCDPデータからCDPのネイバーデバイスとそのネイバーに接続する
# ローカルインターフェースを解析し、利用できるデータ構造に整形する
def parse_cdp_neighbors(cdp_output):

    cdp_neighbors = []

    lines = cdp_output.splitlines()

    for line in lines:
        sections = line.split()

        if len(sections) >= 8 and sections[0].endswith(".lab.local"):

            cdp_neighbor = {
                "remote_device": sections[0].replace(".lab.local", ""),
                "local_interface": (sections[1] + sections[2]).replace("Gig", "Gi"),
                "remote_interface": (sections[-2] + sections[-1]).replace("Gig", "Gi"),
            }

            cdp_neighbors.append(cdp_neighbor)

    return cdp_neighbors


# Parse raw spanning-tree VLAN root and port information
# 生のSTPデータから各VLANのルート情報とポート状態を解析し、
# 利用できるデータ構造に整形する
def parse_spanning_tree(spanning_tree_output):

    spanning_tree = []

    lines = spanning_tree_output.splitlines()

    reading_root_id = False
    reading_bridge_id = False
    reading_ports = False

    for line in lines:

        if line.startswith("VLAN"):
            vlan = int(line.replace("VLAN", ""))

            current_vlan = {
                "vlan": vlan,
                "ports": []
            }

            spanning_tree.append(current_vlan)

        if line.strip().startswith("Interface") and "Role" in line:
            reading_ports = True
        
        if reading_ports and line.strip().startswith(("Gi", "Po")) and len(line.split()) >= 3:
            sections = line.split()

            interface = sections[0]
            role = sections[1]
            state = sections[2]

            current_vlan["ports"].append({
                "interface": interface,
                "role": role,
                "state": state
            })
        
        if line.strip().startswith("Root ID"):
            reading_root_id = True
            reading_ports = False

            sections = line.split()
            root_priority = sections[3]
            current_vlan["root_priority"] = int(root_priority)


        if line.strip().startswith("Bridge ID"):
            reading_root_id = False
            reading_bridge_id = True

            sections = line.split()
            bridge_priority = sections[3]
            current_vlan["bridge_priority"] = int(bridge_priority)

        if reading_bridge_id and line.strip().startswith("Address"):
            bridge_address = line.split()[1]
            current_vlan["bridge_address"] = bridge_address

        if reading_root_id and line.strip().startswith("Address"):
            root_address = line.split()[1]
            current_vlan["root_address"] = root_address
        
        if reading_root_id and line.strip().startswith("Cost"):
            root_cost = line.split()[1]
            current_vlan["root_cost"] = int(root_cost)

        if reading_root_id and line.strip().startswith("Port"):
            sections = line.split()
            root_port = sections[2].strip("()").replace("GigabitEthernet", "Gi")
            current_vlan["root_port"] = root_port

    return spanning_tree


# Parse raw EtherChannel summary information
# 生のEtherChannelデータからEtherChannelの構成とメンバーポートを解析し、
# 利用できるデータ構造に整形する
def parse_etherchannel_summary(etherchannel_output):
    etherchannels = []
    lines = etherchannel_output.splitlines()

    for line in lines:
        sections = line.split()

        if (
            len(sections) >= 4
            and sections[0].isdigit()
            and sections[1].startswith("Po")
            ):
            etherchannel = {
                "group": sections[0],
                "port_channel": sections[1].split("(")[0],
                "protocol": sections[2],
                "ports": [
                    port.split("(")[0]
                    for port in sections[3:]
                ],
            }
            etherchannels.append(etherchannel)

    return etherchannels