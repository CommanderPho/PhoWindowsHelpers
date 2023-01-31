import subprocess as sub
import re
import os
#modified from https://github.com/conda/conda/issues/5165

## Can use `mamba install conda-minify -c jamespreed`

def setup_conda_minify():
    original_dir = os.getcwd()
    libs_directory = "libs" #change to your preferred directory location
    if not os.path.exists(libs_directory):
        os.makedirs(libs_directory)
    os.chdir(libs_directory)
    sub.check_call(" ".join(['git','clone','https://github.com/jamespreed/conda-minify.git']),shell=True)
    os.chdir("conda-minify")
    # can be called using: python -m conda_minify
    os.chdir(original_dir) # restore original dir

# setup_conda_minify()


# create list of current environments
sub.check_call(" ".join(['conda','env','list','>','envs.txt']),shell=True)

# load and parse environment names
envs = {}
with open("envs.txt", 'r') as f:
    lines = f.read().splitlines()
    lines = [l.replace("*","") for l in lines] #get rid of asterix which denotes active environment
    for line in lines[2:]:
        line_match = re.findall(r'(\w*)\s+(C:.*)',line)
        if line_match:
            name,directory = line_match[0]
        if not name:
            local_name = directory.split("\\")[-1]
            print(f"Environment {local_name} is not installed in default conda environment directory.")
            print(f"The environment name will be appended with '_not_in_default_path'")
            envs[f"{local_name}_not_in_default_path"] = directory
        else:
            envs[name] = directory

# write environment packages out
# creates a directory named "exported_conda_envs" in the working folder by default, and writes the environments out there
export_directory = "exported_conda_envs" #change to your preferred directory location
if not os.path.exists(export_directory):
    os.makedirs(export_directory)
os.chdir(export_directory)
for env_name, env_directory in envs.items():
    print("Backing up...",env_name)
    if "_not_in_default_path" in env_name:
        cmd = f"conda env export --no-build --p {env_directory} > {env_name}.yml"
    else:
        cmd = f"conda env export --no-build --name {env_name} > {env_name}.yml"
    sub.check_call(cmd,shell=True)