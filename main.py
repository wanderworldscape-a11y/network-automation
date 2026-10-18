# Import device inventory
# デバイス情報を取り込む
from inventory import devices

# Import STP root devices and EtherChannel relations
# STPのルートブリッジとEtherChannel関係機能を取り込む
from correlators import (
    identify_stp_root_devices,
    correlate_etherchannels,
)

# Import network state collection
# ネットワーク状態を収集する機能を取り込む
from network_state import (
    collect_spanning_trees,
    collect_interface_inventory,
    collect_etherchannel_inventory,
    collect_cdp_inventory,
    build_device_state,
)

# Import OSPF neighbor display
# OSPFネイバー表示機能を取り込む
from ospf import report_ospf_neighbors

# Import VLAN display
# VLAN情報表示の機能を取り込む
from vlan import report_vlans

# Import EtherChannel display
# EtherChannel情報表示の機能を取り込む
from ether import report_etherchannels

# Collect network information before processing individual devices
# # 各デバイスのデータを処理する前にネットワーク状態のデータを一度収集する
all_spanning_trees = collect_spanning_trees(devices)
interface_inventory = collect_interface_inventory(devices)
etherchannel_inventory = collect_etherchannel_inventory(devices)
cdp_inventory = collect_cdp_inventory(devices)
correlated_etherchannels = correlate_etherchannels(
    etherchannel_inventory,
    cdp_inventory,
)

stp_root_devices = identify_stp_root_devices(all_spanning_trees)

# Main loop to process each device and its relation to the network
# 各デバイスのプロファイルとネットワークに関連する情報を処理するメインループ
for device in devices:

    # Collect current network state for this device
    # 本デバイスに関するネットワーク状態を収集する
    device_state = build_device_state(
        device,
        all_spanning_trees,
        interface_inventory,
        cdp_inventory,
    )
    
    neighbors = device_state["neighbors"]
    correlated_ospf_neighbors = device_state["correlated_ospf_neighbors"]
    vlans = device_state["vlans"]
    trunks = device_state["trunks"]
    allowed_vlans = device_state["allowed_vlans"]
    correlated_stp_trunks = device_state["correlated_stp_trunks"]
    spanning_tree = device_state["spanning_tree"]

    # Display this device summary
    # 本デバイスの概要を表示する
    print(f"{'=' * 109}")
    print(f"\n{device['name']} : {device['device_id']}")
    print(f"Neighbor count: {len(neighbors)}")
    if device["role"] == "firewall":
        interfaces = interface_inventory[device["name"]]
        assigned_interfaces = [
            interface for interface in interfaces
            if interface["ip_address"] != "unassigned"
        ]
        print(f"Interfaces: {len(interfaces)} | IP-assigned: {len(assigned_interfaces)}")
    else:
        access_port_count = sum(len(vlan["ports"]) for vlan in vlans)
        print(
            f"VLANs: {len(vlans)} | Trunks: {len(trunks)} "
            f"| Access Ports: {access_port_count}"
        )
    print(f"{'-' * 99}")

    # Display OSPF relationships for this device
    # 本デバイスのOSPFネイバーとの接続関係を表示する
    report_ospf_neighbors(correlated_ospf_neighbors)

    # Display EtherChannel relationships for this device
    # 本デバイスのEtherChannelとリモート側との接続関係を表示する
    report_etherchannels(
        correlated_etherchannels,
        device["name"],
    )

    # Display VLAN information for this device
    # 本デバイスのVLAN情報とリモート側との接続関係を表示する
    if device["role"] != "firewall":
        report_vlans(
            device,
            vlans,
            trunks,
            allowed_vlans,
            correlated_stp_trunks,
            correlated_etherchannels,
            spanning_tree,
            stp_root_devices,
        )
