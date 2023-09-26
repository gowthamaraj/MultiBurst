# multiburst.py
import logging
from core import ansible_controller
from core.droplet_controller import DropletController
from core.terraform_controller import TerraformController
from core.utils import generate_ssh_key, merge_files
import json
import os
import argparse
import yaml
import time
from datetime import datetime

# Set up logging
# Check if the 'logs' directory exists
if not os.path.exists('logs'):
    # If not, create it
    os.makedirs('logs')
log_filename = datetime.now().strftime('logs/%Y-%m-%d_%H-%M-%S.log')
logging.basicConfig(filename=log_filename, level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    try:
        logger.info('main function started')
        parser = argparse.ArgumentParser(description='MutliBurst v1.0')
        parser.add_argument('command', type=str, choices=['build', 'run', 'show', 'merge', 'destroy', 'clean'],
                            help='The command to execute (build, run, show, merge, destroy, clean)')
        args = parser.parse_args()

        # Initialize DropletController and TerraformController
        logger.info('Initializing DropletController and TerraformController')
        d_controller = DropletController(logger)
        t_controller = TerraformController(logger)

        config = ''
        with open('multiburst.yml') as f:
            config = yaml.safe_load(f)

        # Log the multiburst.yml config details
        logger.info(f"Config details: {config}")

        if args.command == 'build':
            logger.info('Command: build')
            # This command will build the infrastructure

            generate_ssh_key("./keys/id_rsa")

            # Generate Terraform files
            logger.info('Generating Terraform files')
            d_controller.generate_terraform_files()

            # Initialize Terraform
            logger.info('Initializing Terraform')
            t_controller.init()

            # Create infrastructure with Terraform
            logger.info('Creating infrastructure with Terraform')
            t_controller.apply()

            # Get list of droplet IPs from Terraform output
            logger.info('Getting list of droplet IPs from Terraform output')
            droplet_ips = t_controller.output()

            # Configure Ansible inventory with droplet IPs
            droplet_ips = json.loads(droplet_ips)["droplet_ips"]["value"]

            # Distribute workload with Ansible
            logger.info('Configuring Ansible inventory with droplet IPs')
            ansible_controller.configure_inventory(droplet_ips, logger)
            logger.info('Running Ansible playbook')
            start_time = time.time()
            ansible_controller.run_playbook(
                './ansible/playbook_build.yml', logger, config)
            end_time = time.time()
            logger.info(f"Time taken to run playbook_build: {end_time - start_time} seconds")

        elif args.command == 'show':
            logger.info('Command: show')
            # This command will show the current state of the infrastructure
            # Get list of droplet IPs from Terraform output
            droplet_ips = t_controller.output()
            try:
                droplet_ips = json.loads(droplet_ips)["droplet_ips"]["value"]
            except KeyError:
                print("The droplets have not been built yet. Please use `multiburst.py build`.")
                logger.error(f"The droplets have not been built yet.")
                return

            # Print droplet IPs and SSH key
            print("Droplets:")
            for ip in droplet_ips:
                # Replace with actual SSH key
                print(f"> ssh root@{ip} -i keys/id_rsa")

        elif args.command == 'run':
            logger.info('Command: run')
            droplet_ips = t_controller.output()
            if "droplet_ips" not in droplet_ips:
                print("The infrastructure has not been built yet. Please run 'multiburst.py build' first.")
                logger.error(f"The droplets have not been built yet.")
                return
            # This command will run the playbook
            start_time = time.time()
            ansible_controller.run_playbook(
                './ansible/playbook_run.yml', logger, config)
            end_time = time.time()
            logger.info(f"Time taken to run playbook_run: {end_time - start_time} seconds")

        elif args.command == 'merge':
            logger.info('Command: merge')
            # This command will merge the output files
            merge_files("output",config["output_file"])

        elif args.command == 'clean':
            logger.info('Command: clean')
            # This command will clean the infrastructure
            start_time = time.time()
            ansible_controller.run_playbook(
                './ansible/playbook_clean.yml', logger, config)
            end_time = time.time()
            logger.info(f"Time taken to run playbook_clean: {end_time - start_time} seconds")

        elif args.command == 'destroy':
            logger.info('Command: destroy')
            # This command will destroy the infrastructure
            # Destroy infrastructure with Terraform
            t_controller.destroy()

        else:
            print(f"Unknown command: {args.command}")
            print("Available commands: build, show, destroy, clean")
    except Exception as e:
            print(f"Error: {e}")
            logger.error(f"Error: {e}")


if __name__ == "__main__":
    main()





