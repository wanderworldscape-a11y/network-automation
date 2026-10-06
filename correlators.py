# Find trunk interfaces that allow a specific VLAN
# 特定したVLANの通信が許可されたトランクインターフェースを識別する
def filter_allowed_vlan(allowed_vlans, vlan_number):

    matching_interfaces = []

    for interface in allowed_vlans:
        if vlan_number in interface["allowed_vlans"]:
            matching_interfaces.append(interface)

    return matching_interfaces

# Correlate trunk interfaces with CDP neighbors
# 本デバイスのトランクインターフェースと一致するCDPローカルインターフェースを特定し、
# それに続いてCDPネイバーの接続関係を特定する
def correlate_trunks_with_cdp(trunks, cdp_neighbors):

    correlated_trunks = []

    for trunk in trunks:

        for cdp_neighbor in cdp_neighbors:

            if trunk["interface"] == cdp_neighbor["local_interface"]:

                correlated_trunk = {
                    "local_interface": trunk["interface"],
                    "remote_device": cdp_neighbor["remote_device"],
                    "remote_interface": cdp_neighbor["remote_interface"],
                }

                correlated_trunks.append(correlated_trunk)

    return correlated_trunks

# Identify the root device for each VLAN across all devices
# 各VLANのルートデバイスを特定する
def identify_stp_root_devices(all_spanning_trees):
    stp_root_devices = {}

    for device_name, spanning_tree in all_spanning_trees.items():
        for vlan in spanning_tree:
            vlan_number = vlan["vlan"]
            root_address = vlan["root_address"]

            for other_device_name, other_spanning_tree in all_spanning_trees.items():
                for other_vlan in other_spanning_tree:
                    if (
                        other_vlan["vlan"] == vlan_number
                        and other_vlan["bridge_address"] == root_address
                    ):
                        stp_root_devices[vlan_number] = other_device_name

    return stp_root_devices

# Correlate trunk connections with VLAN-specific STP port information
# 各VLANに対して、STPポートとトランクポート情報を照合し、関連付ける
def correlate_stp_with_trunks(spanning_tree, correlated_trunks):

    correlated_stp_trunks = []

    for vlan in spanning_tree:

        vlan_number = vlan["vlan"]

        for port in vlan["ports"]:

            for trunk in correlated_trunks:

                if port["interface"] == trunk["local_interface"]:

                    correlated_stp_trunk = {
                        "vlan": vlan_number,
                        "local_interface": port["interface"],
                        "role": port["role"],
                        "state": port["state"],
                        "remote_device": trunk["remote_device"],
                        "remote_interface": trunk["remote_interface"],
                    }

                    correlated_stp_trunks.append(correlated_stp_trunk)

    return correlated_stp_trunks

# Correlate OSPF neighbors with network-wide interface information
# 各デバイスからOSPFネイバー情報とインターフェース情報を照合し、
# OSPFが使用するIPアドレスとデバイスIDをインターフェースに関連付ける
def correlate_ospf_with_interfaces(
    ospf_neighbors,
    interfaces,
    interface_inventory,
):
    correlated_neighbors = []

    for neighbor in ospf_neighbors:
        local_ip = "Unknown"

        for interface in interfaces:
            if neighbor["local_interface"] == interface["interface"]:
                local_ip = interface["ip_address"]

        remote_device = neighbor["neighbor_id"]
        remote_interface = "Unknown Int:"

        for device_name, device_interfaces in interface_inventory.items():
            for interface in device_interfaces:
                if interface["ip_address"] == neighbor["remote_ip"]:
                    remote_device = device_name
                    remote_interface = interface["interface"]

        correlated_neighbor = {
            "neighbor_id": neighbor["neighbor_id"],
            "local_interface": neighbor["local_interface"],
            "local_ip": local_ip,
            "remote_ip": neighbor["remote_ip"],
            "remote_device": remote_device,
            "remote_interface": remote_interface,
        }

        correlated_neighbors.append(correlated_neighbor)

    return correlated_neighbors

# Correlate EtherChannels with remote Port-channels
# ネットワーク中のEtherChannelが使用するポートとCDPネイバーポートを両側から照合し、
# 各EtherChannelがどのデバイスとインターフェースに接続されているかを特定する
def correlate_etherchannels(
    etherchannel_inventory,
    cdp_inventory,
):
    correlated_etherchannels = []

    for device_name, etherchannels in etherchannel_inventory.items():
        for etherchannel in etherchannels:
            remote_devices = set()

            for port in etherchannel["ports"]:
                for cdp_neighbor in cdp_inventory[device_name]:
                    if cdp_neighbor["local_interface"] == port:
                        remote_devices.add(cdp_neighbor["remote_device"])

            for remote_device in remote_devices:
                for remote_etherchannel in etherchannel_inventory.get(remote_device, []):
                    if remote_etherchannel["port_channel"] == etherchannel["port_channel"]:
                        correlated_etherchannel = {
                            "local_device": device_name,
                            "local_port_channel": etherchannel["port_channel"],
                            "local_ports": etherchannel["ports"],
                            "remote_device": remote_device,
                            "remote_port_channel": remote_etherchannel["port_channel"],
                            "remote_ports": remote_etherchannel["ports"],
                        }
                        correlated_etherchannels.append(
                            correlated_etherchannel
                        )

    return correlated_etherchannels