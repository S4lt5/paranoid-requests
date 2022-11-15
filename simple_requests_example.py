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
http_proxies = ["http://95.216.136.105:8888"]
https_proxies = ["https://95.216.136.105:8888","https://135.181.254.248:8888"]
noided_requests.configure(new_identity_per_request=False,http_proxy_list=http_proxies,https_proxy_list=https_proxies)
resp = sess.get(host_addr,headers={"Accept": "application/json"})
print("Paranoid WITH session:\n\t",resp.json()['ip'])

#You can manually specify here, or automatically crawl public proxies (not a great idea if you care about speed/security)
http_proxies = ["http://95.216.136.105:8888","http://135.181.254.248:8888"]
https_proxies = ["https://95.216.136.105:8888","https://135.181.254.248:8888"]
noided_requests.configure(new_identity_per_request=True,http_proxy_list=http_proxies,https_proxy_list=https_proxies)
print("Paranoid Auto Session:\n")
for x in range(2):
    resp = noided_requests.get(host_addr,headers={"Accept": "application/json"})    
    print("\t",resp.json()['ip'])

#We can try completely automatic setup and try our luck against the public proxy list
noided_requests.configure(new_identity_per_request=True)
print("Paranoid Auto Session with public proxy list:\n")
for x in range(2):
    resp = noided_requests.get(host_addr,headers={"Accept": "application/json"})    
    print("\t",resp.json()['ip'])