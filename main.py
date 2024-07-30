import os
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

# Get a list of file names with .yml extension from the specified directory
file_names = []
for file in os.listdir(os.getenv('FILE_PATH')):
    if file.endswith(".yml"):
        file_names.append(file)

# Initialize the Portainer JSON format
portainer_json_format = '''
{
    "version": "2",
    "templates": []
}
'''
# Set the initial value of port
port = 1024

# Iterate through each file name and extract the required information
for file_name in file_names:
    # Initialize temporary variables
    title = ''
    image = ''

    # Extract the image name and service title from the YAML file
    with open(os.getenv('FILE_PATH') + file_name, 'r') as f:
        given_word = 'image:'
        for line in f:
            words_list = line.split()
            if given_word in words_list:
                title = temp_title
            temp_title = line
        title = title.replace(" ", "").replace('\n', '').replace(':', '')

        # Extract the image name
        f.seek(0)
        file_content = f.read()
        start_value = file_content.rfind("image:")
        end_value = file_content.find('\n', start_value + 6)
        image = file_content[start_value + 6:end_value].replace(" ", "").replace('\n', '')

    # Construct the Portainer JSON object for the service
    service_json = '''{
        "type": 1,
        "title": title,
        "name": f"{title}.bit.lan",
        "platform": "linux",
        "administrator_only": False,
        "image": image,
        "hostname": title,
        "restart_policy": "always",
        "ports": [f"{port}/tcp"],
        "volumes": [
            {
                "container": f"/{title}/data",
                "bind": f"/srv/{title}.bit.lan/docker/data",
                "readonly": False
            },
            {
                "container": f"/{title}/config",
                "bind": f"/srv/{title}.bit.lan/docker/config",
                "readonly": False
            },
            {
                "container": f"/{title}/log",
                "bind": f"/srv/{title}.bit.lan/docker/log",
                "readonly": False
            }
        ],
        "labels": [
            {"name": "com.centurylinklabs.watchtower.enable", "value": "true"}
        ]
    }
    '''
    # Append the service JSON object to the list of templates
    portainer_json_format["templates"].append(service_json)

    # Increment the port number
    port += 1

# Write the final Portainer JSON object to a file
with open("portainer_json_formatput.json", 'w') as f:
    f.write(str(portainer_json_format))