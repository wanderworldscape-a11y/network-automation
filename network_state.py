from connection import connect

# Import raw data 
# 生データを取り込む
from collectors import (
    collect_spanning_tree,
    collect_ospf_neighbors,
    collect_interfaces,
    collect_vlan_information,
    collect_trunks,
    collect_cdp_information,
    collect_etherchannel_summary,
)

# Import parsing functions
# 利用できるデータ構造に整形する関数を取り込む
from parsers import (
    parse_spanning_tree,
    parse_ospf_neighbors,
    parse_interfaces,
    parse_vlan_information,
    parse_trunks,
    parse_allowed_vlans,
    parse_cdp_neighbors,
    parse_etherchannel_summary,
)

# Import correlators
# 各デバイスから得たデータの関係を識別する関数を取り込む
from correlators import (
    correlate_trunks_with_cdp,
    correlate_ospf_with_interfaces,
    correlate_stp_with_trunks,
)

# Collect spanning-tree information for all devices
# 各デバイスからSTP状態の生データを収集する
def collect_spanning_trees(devices):
 
    all_spanning_trees = {}

    for device in devices:
        ssh_connection = connect(device)

        try:
            spanning_tree_output = collect_spanning_tree(ssh_connection)
            spanning_tree = parse_spanning_tree(spanning_tree_output)

            all_spanning_trees[device["name"]] = spanning_tree

        finally:
            ssh_connection.disconnect()

    return all_spanning_trees


# Collect interface information for all devices
# 各デバイスのインターフェース設定情報を収集する
def collect_interface_inventory(devices):

    interface_inventory = {}

    for device in devices:
        ssh_connection = connect(device)

        try:
            interface_output = collect_interfaces(ssh_connection)
            interfaces = parse_interfaces(interface_output)

            interface_inventory[device["name"]] = interfaces

        finally:
            ssh_connection.disconnect()

    return interface_inventory

# Collect EtherChannel information for all devices
# 各デバイスからEtherChannelの設定情報を収集する
def collect_etherchannel_inventory(devices):
    etherchannel_inventory = {}

    for device in devices:
        ssh_connection = connect(device)
        try:
            etherchannel_output = collect_etherchannel_summary(ssh_connection)
            etherchannels = parse_etherchannel_summary(etherchannel_output)
            etherchannel_inventory[device["name"]] = etherchannels
        finally:
            ssh_connection.disconnect()

    return etherchannel_inventory


# Collect CDP neighbor information for all devices
# 各デバイスからCDPネイバー状態のデータを収集する
def collect_cdp_inventory(devices):
    cdp_inventory = {}

    for device in devices:
        ssh_connection = connect(device)
        try:
            cdp_output = collect_cdp_information(ssh_connection)
            cdp_neighbors = parse_cdp_neighbors(cdp_output)
            cdp_inventory[device["name"]] = cdp_neighbors
        finally:
            ssh_connection.disconnect()

    return cdp_inventory

# Build device state from collected network data
# 生データの処理と連携を行い、ネットワーク状態を反映するデータに整形する
def build_device_state(
    device,
    all_spanning_trees,
    interface_inventory,
    cdp_inventory,
):

    ssh_connection = connect(device)

    try:
        # Collect and parse OSPF neighbor information
        # 生のOSPFデータを利用できる構造に整形する
        ospf_output = collect_ospf_neighbors(ssh_connection)
        neighbors = parse_ospf_neighbors(ospf_output)

        # Collect and parse VLAN information
        # 生のVLANデータを利用できる構造に整形する
        vlan_output = collect_vlan_information(ssh_connection)
        vlans = parse_vlan_information(vlan_output)

        # Collect and parse trunk information
        # 生のTRUNKデータを利用できる構造に整形する
        trunk_output = collect_trunks(ssh_connection)
        trunks = parse_trunks(trunk_output)

        # Parse allowed VLAN information on trunk interfaces
        # TRUNKの利用が許可されたVLANを特定し、利用できる構造に整形する
        allowed_vlans = parse_allowed_vlans(trunk_output)

        # Use the collected CDP neighbor information
        # 収集したCDPネイバー情報を利用する
        cdp_neighbors = cdp_inventory[device["name"]]

        # Correlate trunk interfaces with CDP neighbors
        # 本デバイスのトランクインターフェースと一致するCDPローカルインターフェースを特定し、
        # それに続いてCDPネイバーの接続関係を特定する
        correlated_trunks = correlate_trunks_with_cdp(
            trunks,
            cdp_neighbors,
        )

        # Correlate OSPF neighbors with interface information
        # 各デバイスからOSPFネイバー情報とインターフェース情報を照合し、
        # OSPFが使用するIPアドレスとデバイスIDをインターフェースに関連付ける
        correlated_ospf_neighbors = correlate_ospf_with_interfaces(
            neighbors,
            interface_inventory[device["name"]],
            interface_inventory,
        )

        # Correlate STP port information with trunk connections
        # STPポート情報とトランク接続関係を照合し、関連付ける
        spanning_tree = all_spanning_trees[device["name"]]

        correlated_stp_trunks = correlate_stp_with_trunks(
            spanning_tree,
            correlated_trunks,
        )
        
        return {
            "neighbors": neighbors,
            "correlated_ospf_neighbors": correlated_ospf_neighbors,
            "vlans": vlans,
            "trunks": trunks,
            "allowed_vlans": allowed_vlans,
            "spanning_tree": spanning_tree,
            "correlated_stp_trunks": correlated_stp_trunks,
        }

    finally:
        ssh_connection.disconnect()