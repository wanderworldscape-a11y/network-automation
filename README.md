# Automatic Network State Reporter

A Python-based network automation project built around a GNS3 Cisco networking lab.

The project connects to multiple network devices over SSH, collects raw network state, parses the device output, correlates information from multiple sources, and produces a network-wide view of device relationships.

Rather than treating each command output independently, the project combines information from OSPF, CDP, VLAN, trunk, STP, interface, and EtherChannel data to identify relationships between devices and interfaces.　- A task that traditionally requires extensive time.  

## Project Goals

This project was built to practice and demonstrate:

- Network device automation using Python and Netmiko
- SSH-based collection of Cisco IOS data
- Parsing semi-structured CLI output
- Correlating information collected from different network sources
- Identifying physical and logical network relationships
- Working with OSPF neighbor relationships
- Identifying VLAN and trunk relationships
- Correlating STP state with trunk connections
- Identifying EtherChannel relationships between devices
- Building a reusable network-state representation

## Architecture

The project follows a four-stage data flow:

    Collect → Parse → Correlate → Report

### 1. Collect

Raw information is collected from the network devices through SSH.

Examples include:

- OSPF neighbor information
- Interface information
- VLAN information
- Trunk information
- CDP neighbor information
- Spanning-tree information
- EtherChannel information

### 2. Parse

The raw Cisco IOS command output is converted into structured Python data.

This separates device-specific CLI output from the rest of the application.

### 3. Correlate

Information from different sources is combined to identify relationships that are not directly available from a single command.

For example:

- OSPF neighbors are correlated with interface information.
- Trunk interfaces are correlated with CDP neighbors.
- STP port information is correlated with trunk connections.
- EtherChannel member ports are correlated with remote CDP information to identify the remote Port-channel.

### 4. Report

The correlated network state is presented on a per-device basis, including device summaries and network relationships.

## Project Structure

```text
network-automation/
├── ansible/
│   └── playbooks/
├── collectors.py
├── connection.py
├── correlators.py
├── ether.py
├── inventory.py
├── main.py
├── network_state.py
├── ospf.py
├── parsers.py
├── vlan.py
├── .env
├── .gitignore
└── .venv/
```

### Python Modules

| File | Purpose |
|---|---|
| `connection.py` | Establishes SSH connections and sends commands to network devices |
| `collectors.py` | Collects raw network information from devices |
| `parsers.py` | Converts raw Cisco IOS command output into structured data |
| `correlators.py` | Correlates information from different network data sources |
| `network_state.py` | Builds the network state for individual devices from collected and correlated data |
| `inventory.py` | Defines the network device inventory and loads credentials from environment variables |
| `main.py` | Controls the overall collection, processing, and reporting workflow |
| `ospf.py` | Displays correlated OSPF neighbor relationships |
| `vlan.py` | Displays VLAN, trunk, and STP relationships |
| `ether.py` | Displays EtherChannel relationships and VLAN/STP associations |

## Requirements

This project was developed and tested in a Linux environment with the following components:

- Python 3
- Netmiko
- Paramiko
- python-dotenv
- GNS3
- Cisco IOS-based network devices

The project uses a Python virtual environment to isolate its dependencies from the system Python installation.

## Configuration

Network device credentials are stored in environment variables rather than directly in the Python source code.

The project uses a `.env` file containing:

```text
NETWORK_USERNAME=<username>
NETWORK_PASSWORD=<password>
```

The `.env` file is excluded from version control through `.gitignore`.

Device-specific information is defined in `inventory.py`, while login credentials are loaded from the environment at runtime.

## Running the Project

### 1. Activate the virtual environment

From the project directory:

```bash
source .venv/bin/activate
```

The `source` command loads the virtual environment's activation script into the current shell session.

When activated, the shell prompt should show:

```text
(.venv)
```

### 2. Configure credentials

Create a `.env` file in the project root containing the required network login credentials:

```text
NETWORK_USERNAME=<username>
NETWORK_PASSWORD=<password>
```
 
### 3. Run the program

From the project directory:

```bash
python main.py
```

The program connects to the devices defined in `inventory.py`, collects network information, processes the collected data, and displays the resulting network state and device relationships.

### Example Workflow

```text
Cisco IOS devices
        │
        ▼
      SSH
        │
        ▼
   Raw CLI data
        │
        ▼
     Parsing
        │
        ▼
   Correlation
        │
        ▼
 Network state
        │
        ▼
     Report
```

## Network Relationships

The program combines information from multiple Cisco IOS data sources to identify relationships across the network.

### OSPF

The program identifies OSPF neighbor relationships and correlates the neighbor information with the interface inventory.

The report can show:

- Local device
- Local interface
- OSPF neighbor device
- Remote IP address
- Associated interface information

### VLAN, Trunk, and STP

For each VLAN, the program correlates:

- VLAN information
- Trunk interfaces
- Allowed VLANs
- STP root bridge
- STP port state
- Remote device relationships

This allows the report to show how a VLAN is carried through the network and how STP is treating the associated ports.

### EtherChannel

EtherChannel relationships are correlated using EtherChannel member-port information and CDP neighbor information.

The report identifies:

- Local Port-channel
- Local member interfaces
- Remote Port-channel
- Remote member interfaces
- Remote device

EtherChannel relationships are also included in the VLAN and STP reporting where applicable.

### Network-Wide Correlation

Network-wide information is collected once and stored in memory before individual device reports are generated.

This allows relationships between devices to be identified without repeatedly collecting the same information from the network.

## Example Output

The program produces a per-device report containing network state and correlated relationships.

For example, the EtherChannel relationship discovered between the distribution switches is reported as:

```text
EtherChannel Relationships:
Po1 (Gi0/1, Gi1/2) <----------> (Gi0/2, Gi1/2) Po1 (DS2)
```

VLAN reporting includes STP and trunk relationships:

```text
VLAN 10 | Root Bridge - DS2
  Trunk Ports:
    Po1 - Root / FWD - DS2
```

OSPF relationships are reported separately:

```text
OSPF Neighbors:
  Local Interface: Vlan50
  Remote IP: 10.10.50.2
  Remote Device: DS2
```

The complete output contains these relationships for each device in the lab.

## Lab Environment

The project was developed and tested against a Cisco network lab running in GNS3.

The lab contains multiple routers and switches with OSPF, VLANs, trunk links, spanning tree, CDP, and EtherChannel relationships.

The automation server runs Ubuntu and connects to the lab devices through SSH.

The project is intentionally designed around the lab's actual network state rather than simulated data. Network relationships are discovered from information collected directly from the devices.

### Network Technologies Used

- Cisco IOS
- OSPF
- VLANs
- 802.1Q trunking
- Spanning Tree Protocol
- EtherChannel / LACP
- CDP
- SSH
- Python
- Netmiko
- Paramiko

## Future Development

Possible future additions to the project include:

- Additional network-state collectors and parsers
- Expanded network relationship correlation
- Additional automation using Ansible
- Improved reporting and visualization
- Integration with network monitoring and observability platforms
- Expansion of the lab topology to support additional routing and switching scenarios
