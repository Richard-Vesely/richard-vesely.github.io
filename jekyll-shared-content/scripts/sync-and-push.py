import subprocess
import shutil
import os
import yaml


def load_paths_config(config_path):
    """Load paths from the YAML configuration file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

# Assuming _paths_for_scripts.yml is two directory levels up from the script
script_dir = os.path.dirname(__file__)
paths_config_path = os.path.join(script_dir, '..', '..', '_paths_for_scripts.yml')
paths_config_path = os.path.normpath(paths_config_path)  # Normalize the path to resolve properly



# Load the paths
paths_config = load_paths_config(paths_config_path)


# Use the paths from the YAML file
blog_path = paths_config['blog_path']
jekyll_shared_content_path = paths_config['jekyll_shared_content_path']

_site_path = os.path.join(blog_path, "_site")


def run_command(commands, cwd=None):
    """Run a command using subprocess."""
    try:
        subprocess.run(commands, cwd=cwd, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        if "git commit" in commands:
            print("No changes to commit.")
        else:
            raise e  # Re-raise the exception for other errors

def copy_directory_contents(src_dir, dest_dir):
    """Copy contents of one directory to another."""
    print(f"Starting to copy contents from {src_dir} to {dest_dir}")
    if not os.path.exists(dest_dir):
        print(f"Destination directory {dest_dir} does not exist. Creating it.")
        os.makedirs(dest_dir)
    for item in os.listdir(src_dir):
        s = os.path.join(src_dir, item)
        d = os.path.join(dest_dir, item)
        try:
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
        except Exception as e:
            print(f"Failed to copy {s} to {d}. Error: {e}")

def run_jekyll_build():
    """Run the Jekyll build command with specific configuration files."""
    os.chdir(blog_path)
    command = f"jekyll build --config _config.yml, config-lang.yml"
    run_command(command, cwd=blog_path)
    print("Jekyll build completed.")

def copy_cname_to_site(blog_path, site_path):
    """Copy the CNAME file from the blog directory to the _site directory."""
    cname_src = os.path.join(blog_path, "CNAME")
    cname_dest = os.path.join(site_path, "CNAME")
    if os.path.exists(cname_src):
        shutil.copy2(cname_src, cname_dest)
        print("CNAME file copied to _site directory.")
    else:
        print("CNAME file does not exist in the blog directory.")

# Function to perform git add, commit, and push in a given directory
def git_commit_push(directory, commit_message):
    """Run git add, commit, and push commands in the specified directory."""
    try:
        os.chdir(directory)
        subprocess.check_call(["git", "add", "."])
        subprocess.check_call(["git", "commit", "-m", commit_message])
        subprocess.check_call(["git", "push"])
        print(f"Changes in {directory} pushed to GitHub successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while pushing to GitHub: {e}")



# Shared directories and files to sync
shared_content = [
    "_includes",
    "_layouts",
    "assets",  # Assuming it's "_assets" and not "_assetsm"
    "_plugins",
    "_sass",
    "_config.yml",
]

commit_message = input("Enter commit message\n")

# Add, commit, and push changes in the blog-en directory
git_commit_push(blog_path, commit_message)


run_jekyll_build()
copy_cname_to_site(blog_path, _site_path)
git_commit_push(_site_path, commit_message)



# Step B: Sync shared content and push in the jekyll-shared-content
for content in shared_content:
    source_path = os.path.join(blog_path, content)
    dest_path = os.path.join(jekyll_shared_content_path, content)
    if os.path.isdir(source_path):
        copy_directory_contents(source_path, dest_path)
    else:  # For single file like _config.yml
        shutil.copy2(source_path, dest_path)


git_commit_push(jekyll_shared_content_path, commit_message)
