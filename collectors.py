# Import run command capability from connection module
# connectionモジュールからSSHを通してコマンドをデバイスへ送信する機能を取り込む
from connection import run_command

# Collect raw OSPF neighbor information
# OSPFネイバー状態の生データを各デバイスから収集する
def collect_ospf_neighbors(ssh_connection):

    if ssh_connection.device_type == "cisco_asa":
        command = "show ospf neighbor"
    else:
        command = "show ip ospf neighbor"

    return run_command(ssh_connection, command)

# Collect raw interface information
# インターフェース状態の生データを各デバイスから収集する
def collect_interfaces(ssh_connection):

    if ssh_connection.device_type == "cisco_asa":
        command = "show interface ip brief"
    else:
        command = "show ip interface brief"

    return run_command(
        ssh_connection,
        command
    )


# Collect ASA logical interface names (nameif)
# ファイヤーウォールのインターフェース情報を収集する
def collect_asa_nameif(ssh_connection):
    return run_command(
        ssh_connection,
        "show nameif"
    )


# Collect raw VLAN information
# VLAN状態の生データを各デバイスから収集する
def collect_vlan_information(ssh_connection):

    return run_command(
        ssh_connection,
        "show vlan brief"
    )

# Collect raw trunk interface information
# トランクインターフェース状態の生データを各デバイスから収集する
def collect_trunks(ssh_connection):

    return run_command(
        ssh_connection,
        "show interface trunk"
    )

# Collect raw CDP neighbor information
# CDPネイバー状態の生データを各デバイスから収集する
def collect_cdp_information(ssh_connection):

    return run_command(
        ssh_connection,
        "show cdp neighbors"
    )

# Collect raw spanning-tree information
# STP状態の生データを各デバイスから収集する
def collect_spanning_tree(ssh_connection):

    return run_command(
        ssh_connection,
        "show spanning-tree"
    )

# Collect raw EtherChannel information
# EtherChannel状態の生データを各デバイスから収集する
def collect_etherchannel_summary(ssh_connection):
    return run_command(
        ssh_connection,
        "show etherchannel summary"
    )