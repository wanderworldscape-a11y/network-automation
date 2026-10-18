# Display EtherChannel relationships
# EtherChannelの接続関係を表示
def report_etherchannels(correlated_etherchannels, device_name):

    for etherchannel in correlated_etherchannels:

        if etherchannel["local_device"] != device_name:
            continue

        local_ports = ", ".join(etherchannel["local_ports"])
        remote_ports = ", ".join(etherchannel["remote_ports"])

        print(
            f"{etherchannel['local_port_channel']} "
            f"({local_ports}) <----------> "
            f"({remote_ports}) "
            f"{etherchannel['remote_port_channel']} "
            f"({etherchannel['remote_device']})"
        )

# Display EtherChannel VLAN/STP relationships
# EtherChannelのVLAN/STP接続関係を表示
def report_etherchannel_vlans(
    correlated_etherchannels,
    device_name,
    matching_interfaces,
    vlan_number,
    spanning_tree,
):
    for etherchannel in correlated_etherchannels:
        if etherchannel["local_device"] != device_name:
            continue

        local_port_channel = etherchannel["local_port_channel"]

        if local_port_channel not in [
            interface["interface"]
            for interface in matching_interfaces
        ]:
            continue

        for stp_vlan in spanning_tree:
            if stp_vlan["vlan"] != int(vlan_number):
                continue

            for stp_port in stp_vlan["ports"]:
                if stp_port["interface"] != local_port_channel:
                    continue

                print(
                    f"{local_port_channel:<18} | "
                    f"{stp_port['role']:<8} | "
                    f"{stp_port['state']:<8} | "
                    f"<-----------> | "
                    f"{etherchannel['remote_port_channel']:<12} | "
                    f"{etherchannel['remote_device']:<15}"
                )