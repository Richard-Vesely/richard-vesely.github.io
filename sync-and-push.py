import subprocess
import shutil
import os

def run_command(commands, cwd=None):
    """Run a command using subprocess."""
    subprocess.run(commands, cwd=cwd, check=True, shell=True)

def copy_directory_contents(src_dir, dest_dir):
    """Copy contents of one directory to another."""
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    for item in os.listdir(src_dir):
        s = os.path.join(src_dir, item)
        d = os.path.join(dest_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
# Function to perform git add, commit, and push in a given directory
def git_commit_push(directory, commit_message):
    """Run git add, commit, and push commands in the specified directory."""
    os.chdir(directory)
    run_command(['git', 'add', '.'])
    run_command(['git', 'commit', '-m', commit_message])
    run_command(['git', 'push'])

# Configure paths
blog_en_path = r"C:\Users\risav\personal_blog_inc_full_project\jekyll-shared-content"
jekyll_shared_content_path = r"C:\Users\risav\personal_blog_inc_full_project"
_site_path = os.path.join(blog_en_path, "_site")

# Shared directories and files to sync
shared_content = [
    "_includes",
    "_layouts",
    "_assets",  # Assuming it's "_assets" and not "_assetsm"
    "_plugins",
    "_sass",
    "_config.yml",
]

commit_message = input("Enter commit message")

# Add, commit, and push changes in the blog-en directory
git_commit_push(blog_en_path, commit_message)

git_commit_push(_site_path, commit_message)



# Step B: Sync shared content and push in the jekyll-shared-content
for content in shared_content:
    source_path = os.path.join(blog_en_path, content)
    dest_path = os.path.join(jekyll_shared_content_path, content)
    if os.path.isdir(source_path):
        copy_directory_contents(source_path, dest_path)
    else:  # For single file like _config.yml
        shutil.copy2(source_path, dest_path)


git_commit_push(jekyll_shared_content_path, commit_message)
