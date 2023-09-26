import yaml
import jinja2
import os
from envparse import env
import logging

env.read_envfile('.env')

class DropletController:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        with open('multiburst.yml') as f:
            self.config = yaml.safe_load(f)
            self.config['do_token'] = env('DO_TOKEN')
            self.logger.info("DropletController initialized.")

    def generate_terraform_files(self):
        self.logger.info("Generating Terraform files...")
        try:
            loader = jinja2.FileSystemLoader(searchpath="./terraform/templates/")
            environment = jinja2.Environment(loader=loader)
            for filename in os.listdir("./terraform/templates/"):
                template = environment.get_template(filename)
                output = template.render(self.config)
                with open(f"terraform/{filename.rsplit('.', 1)[0]}", "w") as f:
                    f.write(output)
            self.logger.info("Successfully created Terraform templates.")
        except Exception as e:
            self.logger.error(f"Failed to create Terraform templates: {e}")
            raise