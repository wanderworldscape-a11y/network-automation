# Import VLAN related data
# VLANに関するデータを取り込む
from correlators import (
    filter_allowed_vlan,
)

from ether import report_etherchannel_vlans

# Display VLAN, trunk, and STP information
# VLAN、トランク、STP情報を表示する
def report_vlans(
    device,
    vlans,
    trunks,
    allowed_vlans,
    correlated_stp_trunks,
    correlated_etherchannels,
    spanning_tree,
    stp_root_devices,
):

    for vlan in vlans:

        vlan_number = vlan["vlan"]

        # Find trunk interfaces that allow this VLAN
        # 本VLANの通信が許可されたトランクインターフェースを特定する
        matching_interfaces = filter_allowed_vlan(
            allowed_vlans,
            vlan_number
        )

        print(f"{'-' * 99}")

        # Find the STP root bridge for this VLAN
        # 本VLANのSTPルートブリッジを特定する
        root_bridge = stp_root_devices.get(int(vlan_number), "Unknown")

        # Print VLAN header
        # 本VLANヘッダーを表示する
        if device["name"] == root_bridge:
            print(f"VLAN {vlan_number} TRUNK PORTS | This is the root bridge")
        else:
            print(f"VLAN {vlan_number} TRUNK PORTS | Root Bridge - {root_bridge}")

        # Print trunk ports for this VLAN
        # 本VLANのトランクポートを表示する
        print(f"{'-' * 99}")
        print(
            f"{'Local Int':<18} | "
            f"{'Role':<8} | "
            f"{'State':<8} | "
            f"{'':<13} | "
            f"{'Remote Int':<12} | "
            f"{'Remote Device':<15}"
        )
        print(
            f"{'-' * 18}-+-"
            f"{'-' * 8}-+-"
            f"{'-' * 8}-+-"
            f"{'-' * 13}-+-"
            f"{'-' * 12}-+-"
            f"{'-' * 15}"
        )


        # Look for interfaces associated with this VLAN
        # 本VLANに関連する各インターフェースを探す
        for matching_interface in matching_interfaces:

            interface = matching_interface["interface"]

            # Default to access unless the interface is identified as a trunk
            # TRUNKであると特定するまでアクセスポートとして指定する
            port_type = "access"

            # Check whether the interface is a trunk
            # 本インターフェースがトランクか確認する
            for trunk in trunks:

                # Match the interface to the trunk interface
                # 本インターフェースとトランクインターフェースを照合する
                if trunk["interface"] == interface:
                    port_type = "trunk"

            # Process the interface details if it is a trunk
            # 本インターフェースがトランクであると特定した場合はTRUNKの詳細情報を処理する
            if port_type == "trunk":

                # Find STP state and remote device for this trunk
                # 本トランクのSTP状態とリモート側のデバイスを特定する
                for correlated_stp_trunk in correlated_stp_trunks:

                    if (
                        correlated_stp_trunk["vlan"] == int(vlan_number)
                        and correlated_stp_trunk["local_interface"] == interface
                    ):

                        print(
                            f"{interface:<18} | "
                            f"{correlated_stp_trunk['role']:<8} | "
                            f"{correlated_stp_trunk['state']:<8} | "
                            f"<-----------> | "
                            f"{correlated_stp_trunk['remote_interface']:<12} | "
                            f"{correlated_stp_trunk['remote_device']:<15}"
                        )

        
        # Display EtherChannel VLAN relationships
        # EtherChannelのVLAN関係を表示する
        report_etherchannel_vlans(
            correlated_etherchannels,
            device["name"],
            matching_interfaces,
            vlan_number,
            spanning_tree,
        )

        # Print access ports title for this VLAN
        # VLANのアクセスポートヘッダーを表示する
        print(f"{'-' * 99}")
        print(f"VLAN {vlan_number} ACCESS PORTS:")
        
        # Get access ports for the VLAN
        # 本VLANのアクセスポートを取得する
        access_ports = vlan["ports"]

        # Print None if no access ports are found
        # アクセスポートがない場合はNoneを表示する
        if access_ports:

            for access_port in access_ports:
                print(f"{access_port}")

        else:

            print("    None")