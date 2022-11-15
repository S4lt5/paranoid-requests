import paranoid_requests.requests_wrapper as noided_requests
import requests




# First, get my IP from ifconfig.co
host_addr = "http://ifconfig.co"

resp = requests.get(host_addr,headers={"Accept": "application/json"})
print("Default:\n\t",resp.json()['ip'])

#By default, paranoid proxy/user agents are only set when creating a new session
resp = noided_requests.get(host_addr,headers={"Accept": "application/json"})
print("Paranoid without session:\n\t",resp.json()['ip'])

sess = noided_requests.Session()

resp = sess.get(host_addr)
print("Paranoid WITH session:\n\t",resp.json()['ip'])
print("Configuring paranoid proxy lists...")
#...or I set new_identity_per_request=True like so
noided_requests.configure(new_identity_per_request=True)
print("Done.")
print("Paranoid Auto Session:\n")
for x in range(2):
    resp = noided_requests.get(host_addr,headers={"Accept": "application/json"})
    print("\t",resp.json()['ip'])
