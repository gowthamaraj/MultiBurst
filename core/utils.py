import logging
import subprocess
import os
import stat

logger = logging.getLogger(__name__)

def merge_files(directory, output_file):
    """Merge all files in a directory into a single file, removing duplicates and sorting by status code and message."""
        # Check if the directory exists
    if not os.path.isdir(directory):
        print(f"The directory '{directory}' does not exist.")
        logger.error((f"The directory '{directory}' does not exist."))
        return
    
    logger.info('Merging files in directory: %s', directory)
    seen_lines = set()
    lines = []
    for filename in os.listdir(directory):
        if filename == output_file:
            # Don't read the output file if it exists
            continue
        with open(os.path.join(directory, filename), "r") as infile:
            for line in infile:
                if line not in seen_lines:
                    seen_lines.add(line)
                    # Split the line into status code, message, and the rest
                    status_code, msg, rest = line.split(maxsplit=2)
                    # Add the line to the list as a tuple for easy sorting
                    lines.append(((status_code), msg, line))

    # Sort the lines by status code and message
    lines.sort()

    # Write the sorted lines to the output file
    with open(os.path.join(directory, output_file), "w") as outfile:
        for _, _, line in lines:
            outfile.write(line)
    logger.info('Merged files written to: %s', output_file)

def generate_ssh_key(key_path):
    """Generate an SSH key pair at the specified path."""
    logger.info('Generating SSH key at path: %s', key_path)
    
    # Create the directory for key_path if it does not exist
    os.makedirs(os.path.dirname(key_path), exist_ok=True)
    
    if not os.path.exists(key_path):
        subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "4096", "-C", "multiburst@fuffsec.hack", "-f", key_path, "-N", ""], check=True)
        os.chmod(key_path, stat.S_IRUSR | stat.S_IWUSR)
    logger.info('SSH key generated at: %s', key_path)