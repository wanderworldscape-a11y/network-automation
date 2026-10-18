
# Display correlated OSPF neighbor relationships
# OSPFネイバーとの接続関係を表形式で表示する
def report_ospf_neighbors(correlated_ospf_neighbors):

    if not correlated_ospf_neighbors:
        print("No OSPF neighbors.")
        return

    columns = [
        ("Local Int", "local_interface", 12),
        ("Local IP", "local_ip", 16),
        ("", "connection", 13),
        ("Remote IP", "remote_ip", 16),
        ("Remote Int", "remote_interface", 12),
        ("Remote Device", "remote_device", 15),
    ]

    header = " | ".join(
        f"{title:<{width}}" for title, _, width in columns
    )

    separator = "-+-".join(
        "-" * width for _, _, width in columns
    )

    print(header)
    print(separator)

    for neighbor in correlated_ospf_neighbors:
        row = " | ".join(
            f"{str(neighbor.get(key, '<----------->')):<{width}}"
            for _, key, width in columns
        )
        print(row)
