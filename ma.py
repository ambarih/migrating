import subprocess
import os

namespace = "acc"
source_pod_name = "sjenkins-57f55b945d-xmksc"  # Source Jenkins pod
destination_pod_name = "djenkins-65dbdc545d-6jq4b"  # Destination Jenkins pod

# Step 1: Ensure kubectl is in the PATH (for Jenkins pipeline environment)
kubectl_path = "/root/kubectl"  # Path to kubectl, update this as necessary
if not os.path.exists(kubectl_path):
    print(f"kubectl not found at {kubectl_path}. Please check kubectl installation.")
    exit(1)
os.environ["PATH"] = f"{os.environ['PATH']}:{kubectl_path}"

# Directory paths
source_directory = "/var/jenkins_home/jobs"
local_directory = "/tmp/jenkins_jobs"  # Local directory where the jobs will be copied

try:
    # Step 2: Copy jobs from the source Jenkins pod to local machine
    command_cp_from_pod = f"kubectl cp {namespace}/{source_pod_name}:{source_directory} {local_directory}"
    print(f"Running command: {command_cp_from_pod}")
    result_cp_from_pod = subprocess.run(command_cp_from_pod, shell=True, capture_output=True, text=True)

    if result_cp_from_pod.returncode == 0:
        print(f"Successfully copied jobs from {source_pod_name} to local directory {local_directory}")
    else:
        print(f"Error copying jobs from source pod: {result_cp_from_pod.stderr}")

    # Step 3: Copy the jobs directory from local machine to the destination pod at /var/jenkins_home/jobs
    command_cp_to_pod = f"kubectl cp {local_directory}/. {namespace}/{destination_pod_name}:{source_directory}"
    print(f"Running command: {command_cp_to_pod}")
    result_cp_to_pod = subprocess.run(command_cp_to_pod, shell=True, capture_output=True, text=True)

    if result_cp_to_pod.returncode == 0:
        print(f"Successfully copied jobs to {destination_pod_name} in the {namespace} namespace at {source_directory}")
    else:
        print(f"Error copying jobs to destination pod: {result_cp_to_pod.stderr}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
