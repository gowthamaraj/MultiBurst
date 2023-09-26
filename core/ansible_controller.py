import logging
import subprocess
import os
import json

os.environ['ANSIBLE_CONFIG'] = "ansible/ansible.cfg"

logger = logging.getLogger(__name__)

def configure_inventory(droplet_ips, logger):
    """Write the IP addresses of the droplets to the Ansible inventory file."""
    logger.info("Configuring Ansible inventory...")
    try:
        with open("ansible/inventory.ini", "w") as f:
            f.write("[droplets]")
            for ip in droplet_ips:
                f.write(f"\n{ip}")
        logger.info("Successfully configured Ansible inventory.")
    except Exception as e:
        logger.error(f"Failed to configure Ansible inventory: {e}")
        raise


def run_playbook(playbook_path, logger, extra_vars=None):
    """Run the specified Ansible playbook."""
    logger.info(f"Running Ansible playbook: {playbook_path}")
    try:
        cmd = ["ansible-playbook", "-i", "./ansible/inventory.ini",
               "-u", "root", "--private-key", "./keys/id_rsa", playbook_path]
        if extra_vars:
            cmd.append("--extra-vars")
            cmd.append(json.dumps(extra_vars))
        subprocess.run(cmd, check=False)
        logger.info(f"Successfully ran Ansible playbook: {playbook_path}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to run Ansible playbook: {e}")
        raise


