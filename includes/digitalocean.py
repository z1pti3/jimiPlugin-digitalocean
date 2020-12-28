import requests
import json
import time
from pathlib import Path

class _digitalocean():
    url = "https://api.digitalocean.com/v2"

    def __init__(self, apiToken, ca=None, requestTimeout=30):
        self.requestTimeout = requestTimeout
        self.apiToken = apiToken
        self.headers = {
            "Authorization" : "Bearer {0}".format(self.apiToken)
        }
        if ca:
            self.ca = Path(ca)
        else:
            self.ca = None

    # NOTE need to add paging support as currently the API will only handle a single page of results
    # NOTE need to handle rate limiting and credits
    def apiCall(self,endpoint,methord="GET",data=None):
        kwargs={}
        kwargs["timeout"] = self.requestTimeout
        kwargs["headers"] = self.headers
        if self.ca:
            kwargs["verify"] = self.ca
        try:
            url = "{0}/{1}".format(self.url,endpoint)
            if methord == "GET":
                response = requests.get(url, **kwargs)
            elif methord == "POST":
                kwargs["data"] = data
                response = requests.post(url, **kwargs)
            elif methord == "DELETE":
                response = requests.delete(url, **kwargs)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            return 0, "Connection Timeout"
        if response.status_code == 200 or response.status_code == 202:
            return json.loads(response.text)
        return None

    def listDroplets(self,name=None,summary=True):
        response = self.apiCall("droplets")["droplets"]
        if summary:
            result = []
            for droplet in response:
                resultItem = {}
                resultItem["id"] = getKey(droplet,"id")
                resultItem["name"] = getKey(droplet,"name")
                resultItem["locked"] = getKey(droplet,"locked")
                resultItem["status"] = getKey(droplet,"status")
                resultItem["created_at"] = getKey(droplet,"created_at")
                resultItem["region"] = getKey(droplet["region"],"name")
                resultItem["size"] = getKey(droplet["size"],"slug")
                resultItem["os"] = getKey(droplet["image"],"distribution")
                index = 0
                resultItem["ipv4_addresses"] = len(droplet["networks"]["v4"])
                for ipv4 in droplet["networks"]["v4"]:
                    resultItem["ipv4_address_{0}".format(index)] = getKey(ipv4,"ip_address")
                    resultItem["ipv4_netmask_{0}".format(index)] = getKey(ipv4,"netmask")
                    resultItem["ipv4_gateway_{0}".format(index)] = getKey(ipv4,"gateway")
                    resultItem["ipv4_type_{0}".format(index)] = getKey(ipv4,"type")
                    index+=1
                index = 0
                resultItem["ipv6_addresses"] = len(droplet["networks"]["v6"])
                for ipv4 in droplet["networks"]["v6"]:
                    resultItem["ipv6_address_{0}".format(index)] = getKey(ipv4,"ip_address")
                    resultItem["ipv6_netmask_{0}".format(index)] = getKey(ipv4,"netmask")
                    resultItem["ipv6_gateway_{0}".format(index)] = getKey(ipv4,"gateway")
                    resultItem["ipv6_type_{0}".format(index)] = getKey(ipv4,"type")
                    index+=1
                result.append(resultItem)
                if droplet["name"] == name:
                    return resultItem
            if not name:
                return result
            else:
                return { "msg" : "Not found", "error" : 404 }
        if name:
            for droplet in response:
                if droplet["name"] == name:
                    return droplet
            return { "msg" : "Not found", "error" : 404 }
        return response

    def getDroplet(self,dropletID,summary=True,network=False):
        response = self.apiCall("droplets/{0}".format(dropletID))["droplet"]
        if network:
            for ipv4 in response["networks"]["v4"]:
                if ipv4["type"] == "public":
                    return { "address" : ipv4["ip_address"], "netmask" : ipv4["netmask"], "gateway" : ipv4["gateway"] }
            for ipv6 in response["networks"]["v6"]:
                if ipv6["type"] == "public":
                    return { "address" : ipv4["ip_address"], "netmask" : ipv4["netmask"], "gateway" : ipv4["gateway"] }
        if summary:
            droplet = response
            resultItem = {}
            resultItem["id"] = getKey(droplet,"id")
            resultItem["name"] = getKey(droplet,"name")
            resultItem["locked"] = getKey(droplet,"locked")
            resultItem["status"] = getKey(droplet,"status")
            resultItem["created_at"] = getKey(droplet,"created_at")
            resultItem["region"] = getKey(droplet["region"],"name")
            resultItem["size"] = getKey(droplet["size"],"slug")
            resultItem["os"] = getKey(droplet["image"],"distribution")
            index = 0
            resultItem["ipv4_addresses"] = len(droplet["networks"]["v4"])
            for ipv4 in droplet["networks"]["v4"]:
                resultItem["ipv4_address_{0}".format(index)] = getKey(ipv4,"ip_address")
                resultItem["ipv4_netmask_{0}".format(index)] = getKey(ipv4,"netmask")
                resultItem["ipv4_gateway_{0}".format(index)] = getKey(ipv4,"gateway")
                resultItem["ipv4_type_{0}".format(index)] = getKey(ipv4,"type")
                index+=1
            index = 0
            resultItem["ipv6_addresses"] = len(droplet["networks"]["v6"])
            for ipv6 in droplet["networks"]["v6"]:
                resultItem["ipv6_address_{0}".format(index)] = getKey(ipv6,"ip_address")
                resultItem["ipv6_netmask_{0}".format(index)] = getKey(ipv6,"netmask")
                resultItem["ipv6_gateway_{0}".format(index)] = getKey(ipv6,"gateway")
                resultItem["ipv6_type_{0}".format(index)] = getKey(ipv6,"type")
                index+=1
            return resultItem
        return response

    # region ['ams2', 'ams3', 'blr1', 'fra1', 'lon1', 'nyc1', 'nyc2', 'nyc3', 'sfo1', 'sfo2', 'sfo3', 'sgp1', 'tor1']
    # size ['s-1vcpu-1gb', 's-1vcpu-2gb', 's-2vcpu-2gb', 's-2vcpu-4gb', 's-4vcpu-8gb', 'c-2', 'c2-2vcpu-4gb', 'g-2vcpu-8gb', 'gd-2vcpu-8gb', 's-8vcpu-16gb', 'm-2vcpu-16gb', 'c-4', 'c2-4vpcu-8gb', 'm3-2vcpu-16gb', 'g-4vcpu-16gb', 'so-2vcpu-16gb', 'm6-2vcpu-16gb', 'gd-4vcpu-16gb', 'so1_5-2vcpu-16gb', 'm-4vcpu-32gb', 'c-8', 'c2-8vpcu-16gb', 'm3-4vcpu-32gb', 'g-8vcpu-32gb', 'so-4vcpu-32gb', 'm6-4vcpu-32gb', 'gd-8vcpu-32gb', 'so1_5-4vcpu-32gb', 'm-8vcpu-64gb', 'c-16', 'c2-16vcpu-32gb', 'm3-8vcpu-64gb', 'g-16vcpu-64gb', 'so-8vcpu-64gb', 'm6-8vcpu-64gb', 'gd-16vcpu-64gb', 'so1_5-8vcpu-64gb', 'm-16vcpu-128gb', 'c-32', 'c2-32vpcu-64gb', 'm3-16vcpu-128gb', 'm-24vcpu-192gb', 'g-32vcpu-128gb', 'so-16vcpu-128gb', 'm6-16vcpu-128gb', 'gd-32vcpu-128gb', 'm3-24vcpu-192gb', 'g-40vcpu-160gb', 'so1_5-16vcpu-128gb', 'gd-40vcpu-160gb', 'so-24vcpu-192gb', 'm6-24vcpu-192gb', 'm3-32vcpu-256gb', 'so1_5-24vcpu-192gb', 'so-32vcpu-256gb', 'm6-32vcpu-256gb', 'so1_5-32vcpu-256gb']
    # image ubuntu-20-04-x86
    def createDroplet(self,name,region,image,size,ssh_keys):
        data = { "name" : name, "region" : region, "size" : size, "image" : image, "ssh_keys" : ssh_keys }
        response = self.apiCall("droplets",methord="POST",data=data)
        if response:
            return response["droplet"]["id"]
        return None

    def deleteDroplet(self,dropletID):
        response = self.apiCall("droplets/{0}".format(dropletID),methord="DELETE")
        return response

    def waitForDroplet(self,dropletID,timeout=300):
        startTime = time.time()
        while True:
            response = self.apiCall("droplets/{0}".format(dropletID))["droplet"]
            if response["status"] == "active":
                return True
            if time.time() - startTime > timeout:
                return False
            time.sleep(10)
        
    def listKeys(self,name=None):
        response = self.apiCall("account/keys")["ssh_keys"]
        if name:
            for key in response:
                if key["name"] == name:
                    response = key
                    break
            if type(response) is list:
                return {}
        return response


    def getMyBalance(self):
        response = self.apiCall("customers/my/balance")
        return response
        
def getKey(dictObj,key):
    try:
        return dictObj[key]
    except KeyError:
        return None

