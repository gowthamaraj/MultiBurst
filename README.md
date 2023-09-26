![MultiBurst Logo](images/Multiburst-logos.jpeg)

# MultiBurst v1.0

MultiBurst is a Python-based application designed to distribute workload across multiple servers using Ansible and Terraform. It leverages DigitalOcean's infrastructure to create droplets (virtual machines) and uses Ansible to configure these droplets and distribute tasks among them.

## Use Cases

1. **Large-Scale Scanning**: MultiBurst is designed to run a tool like a web directory scanner against a single target with a large payload or wordlist. This makes it an ideal tool for security researchers or penetration testers who need to conduct intensive scanning tasks. (Starting with Feroxbuster)

2. **Distributed Computing**: If you have a computationally intensive task that can be broken down into smaller tasks, MultiBurst can distribute these tasks across multiple servers to speed up the computation.

3. **Load Testing**: MultiBurst can generate high traffic from multiple servers to a single target, making it a useful tool for load testing.

4. **Automated Deployment**: If you need to deploy software to multiple servers, MultiBurst can automate this process.

## Features

- Distributes workload across multiple servers.
- Uses Ansible for configuration management.
- Uses Terraform for infrastructure management.
- Supports DigitalOcean droplets.

## Prerequisites

- Python 3.9 or higher
- Ansible 8.4.0 or higher
- Terraform 2.0 or higher
- DigitalOcean API token

## Installation

1. Install Poetry by following the instructions provided on the official Poetry documentation: https://python-poetry.org/docs/#installing-with-the-official-installer
2. Clone the MultiBurst repository from GitHub using the following command: `git clone https://github.com/gowthamaraj/MultiBurst.git`
3. Navigate into the cloned repository by executing: `cd MultiBurst`
4. Install the necessary dependencies specified in the `pyproject.toml` file by running: `poetry install`
5. Enter the virtual environment created by Poetry using the command: `poetry shell`
6. Create a `.env` file in the root directory of the project and add your DigitalOcean API Key in the following format:
```ini
DO_TOKEN=<Your_DigitalOcean_API_Key>
```
*Please replace `<Your_DigitalOcean_API_Key>` with your actual DigitalOcean API Key.*

### Optional Installation with requirements.txt

If you prefer not to use Poetry, you can install the necessary dependencies using a `requirements.txt` file.

1. Ensure you have Python 3.9 or higher installed on your system.
2. Clone the MultiBurst repository from GitHub using the following command: `git clone https://github.com/gowthamaraj/MultiBurst.git`
3. Navigate into the cloned repository by executing: `cd MultiBurst`
4. Install the necessary dependencies specified in the `requirements.txt` file by running: `pip install -r requirements.txt`
5. Create a `.env` file in the root directory of the project and add your DigitalOcean API Key in the following format:
```ini
DO_TOKEN=<Your_DigitalOcean_API_Key>
```
*Please replace `<Your_DigitalOcean_API_Key>` with your actual DigitalOcean API Key.*

## Usage

Run `multiburst.py --help` for a list of available commands.

The application is controlled via the `multiburst.py` script. It accepts the following commands:

- `build`: This command will build the infrastructure. It generates SSH keys, creates Terraform files, initializes Terraform, applies Terraform configuration, and configures Ansible inventory.
- `show`: This command will show the current state of the infrastructure. It prints droplet IPs and SSH key.
- `run`: This command will run the playbook. It runs the Ansible playbook specified in `ansible/playbook_run.yml`.
- `merge`: This command will merge the output files. It merges all output files into a single file, removing duplicates and sorting by status code and message.
- `clean`: This command will clean the infrastructure. It runs the Ansible playbook specified in `ansible/playbook_clean.yml` to clean the output files in the remote nodes.
- `destroy`: This command will destroy the infrastructure. It destroys the infrastructure with Terraform.

## Configuration

The application can be configured via the `multiburst.yml` file. Here you can specify the number of droplets, the image, region, size, URL, wordlist, timeout, threads, and output file.

## Test Results

Here are the timing results for single and multi instance:

Configuration:
```yml
droplet_count: <VARIABLE>
image: "ubuntu-22-04-x64"
region: "nyc3"
size: "s-2vcpu-2gb"
url: "http://testphp.vulnweb.com/"
wordlist: "/snap/seclists/current/Discovery/Web-Content/directory-list-lowercase-2.3-small.txt"
timeout: 7
threads: 100
output_file: "output_merged.txt"
```

Instance Type | Time Taken |
--------------|------------|
Single Instance (1 droplet)| 245.02327609062195 seconds |
Multi Instance (9 droplet)| 40.62388014793396 |

## To-Do

Here are some potential enhancements for the future:

- [ ] **Support for Other Cloud Providers**: Extend support to other cloud providers like AWS, Google Cloud, and Azure.
- [ ] **Integration with Additional Tools**: Expand the project's capabilities by integrating it with more security tools, particularly those that can benefit from distributed processing.
- [ ] **IP Rotation**: Implement a feature to rotate IP addresses. This could help to distribute requests more evenly across the network, avoid rate-limiting issues, and increase anonymity. This feature would require careful management of IP resources and may involve integrating with a proxy service or using a pool of available IP addresses.
- [ ] **GUI Interface**: Develop a graphical user interface for easier interaction.
- [x] ~~**Improved Error Handling and Logging**: Provide more detailed error messages and better handling of exceptions.~~
- [x] ~~**Performance Metrics**: Provide more detailed performance metrics.~~
- [ ] **Scalability Improvements**: Optimize the application to handle larger workloads.
- [ ] **Automated Updates and Maintenance**: Add features for automatic software updates and routine maintenance tasks.
- [ ] **Enhanced Security Features**: Implement additional security measures to protect data and ensure task integrity.

## Acknowledgments

* [Attack Range](https://github.com/splunk/attack_range) - For providing inspiration for this project.
* [Feroxbuster](https://github.com/epi052/feroxbuster)

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
