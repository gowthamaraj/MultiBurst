import subprocess
import logging

class TerraformController:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def init(self):
        self.logger.info("Initializing Terraform...")
        try:
            subprocess.run(["terraform", "init"], check=True, cwd='terraform/')
            self.logger.info("Terraform initialized successfully.")
        except Exception as e:
            self.logger.error(f"Failed to initialize Terraform: {e}")
            raise

    def apply(self):
        self.logger.info("Applying Terraform...")
        try:
            subprocess.run(["terraform", "apply", "-auto-approve"], check=True, cwd='terraform/')
            self.logger.info("Terraform applied successfully.")
        except Exception as e:
            self.logger.error(f"Failed to apply Terraform: {e}")
            raise

    def output(self):
        self.logger.info("Obtaining Terraform output...")
        try:
            result = subprocess.run(["terraform", "output", "-json"], check=True, capture_output=True, text=True, cwd='terraform/')
            self.logger.info("Terraform output obtained successfully.")
            return result.stdout
        except Exception as e:
            self.logger.error(f"Failed to get Terraform output: {e}")
            raise

    def destroy(self):
        self.logger.info("Destroying the infrastructure...")
        try:
            subprocess.run(["terraform", "destroy", "-auto-approve"], check=True, cwd='terraform/')
            self.logger.info("Successfully destroyed the infrastructure.")
        except Exception as e:
            self.logger.error(f"Failed to destroy the infrastructure: {e}")
            raise