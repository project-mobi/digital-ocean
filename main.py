import requests
import os, sys
import settings
import digitalocean

TOKEN = os.getenv("DIGITALOCEAN_ACCESS_TOKEN")
print(TOKEN)

URL = "https://api.digitalocean.com/v2"

class Droplet(digitalocean.Droplet):
    pass

company_id = 1234
company_name = 'Name'
ssh_key = '1234'
size = '512mb'

droplet_dict = {
    'company_id': company_id,
    'company_name': company_name,
    'ssh_key': ssh_key,
    'size': size,
    'droplet_name': "test-api-droplet-1",
    'droplet_region': "fra1",
    'droplet_image': 'Base Image'
}


def get_sizes():
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    r = requests.get('https://api.digitalocean.com/v2/sizes', headers=headers)
    return r.json()

def create(droplet_dict):
    droplet = digitalocean.Droplet(token=TOKEN,
                               name=droplet_dict['droplet_name'],
                               region=droplet_dict['droplet_region'], # New York 2
                               image='ubuntu-20-04-x64', # Ubuntu 20.04 x64
                               size_slug=droplet_dict['size'],  # 1GB RAM, 1 vCPU
                               backups=False)
    droplet.create()
    return droplet

def get_status(droplet):
    actions = droplet.get_actions()
    for action in actions:
        action.load()
        # Once it shows "completed", droplet is up and running
        action.status
        if action.status == 'completed':
            return action.status
        else:
            return get_status(droplet)


def destroy():
    pass

sizes = get_sizes()
for size in sizes['sizes']:
    #size_dict = sizes[size]
    print(f"{size['slug']}\t\t {size['memory']}\t {size['vcpus']}\t {size['regions']}")
manager = digitalocean.Manager(token=TOKEN)
droplets = manager.get_all_droplets()
for droplet in droplets:
    print(droplet)

droplet = create(droplet_dict)
status = get_status(droplet)
print(status)



""" 
def post_droplet(droplet):

    data = {
        "name": "New Droplet",
        "region": "nyc3",
        "size": "",
        "image": ""
    }

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    r = requests.get(f"{URL}/droplets", headers=headers, data=data)
    return r """

"""

headers = {"Authorization": f"Bearer {TOKEN}"}

r = requests.get(f"{URL}/droplets", headers=headers)
response = r.json()

print(response['droplets'])




if __name__ == "__main__":
    droplet = {}
    new_droplet = post_droplet(droplet).json()
    print(new_droplet) """

