# Import device connectivity libraries
# デバイスと接続を管理するライブラリーを取り込む
from netmiko import ConnectHandler
import paramiko

# Enable legacy SSH KEX required by devices in this project
# 本プロジェクトのデバイスが使用する旧式SSHキー交換アルゴリズムを有効化する
paramiko.Transport._preferred_kex = (
    "diffie-hellman-group14-sha1",
)

# Establish an SSH connection to a network device
# ネットワークデバイスへのSSH接続を確立する
def connect(device):
    connection = ConnectHandler(
        device_type=device["device_type"],
        host=device["host"],
        username=device["username"],
        password=device["password"],
    )

    return connection

# Send a network device command such as an IOS command through the established SSH connection
# SSH接続を使用してデバイスにIOSコマンドなどを送信する
def run_command(ssh_connection, command):
    return ssh_connection.send_command(command)