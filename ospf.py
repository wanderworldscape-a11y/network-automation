# Display correlated OSPF neighbor relationships
# OSPFネイバーとの接続関係を表示する
def report_ospf_neighbors(correlated_ospf_neighbors):

    for neighbor in correlated_ospf_neighbors:

        print(
            f"{neighbor['local_interface']} "
            f"({neighbor['local_ip']}) "
            f"<-----------> ({neighbor['remote_ip']}) "
            f"{neighbor['remote_interface']} "
            f"({neighbor['remote_device']})\n"
            
        )