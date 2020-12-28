from core.models import action
from core import auth, db, helpers

from plugins.digitalocean.includes import digitalocean

class _digitaloceanListDroplets(action._action):
    apiToken = str()

    def run(self,data,persistentData,actionResult):
        apiToken = auth.getPasswordFromENC(self.apiToken)

        result = digitalocean._digitalocean(apiToken).listDroplets()
        if result:
            actionResult["result"] = True
            actionResult["rc"] = 0
            actionResult["droplets"] = result
        else:
            actionResult["result"] = False
            actionResult["rc"] = 404
            actionResult["msg"] = "Failed to get a valid response from virustotal API"
        return actionResult 

    def setAttribute(self,attr,value,sessionData=None):
        if attr == "apiToken" and not value.startswith("ENC "):
            if db.fieldACLAccess(sessionData,self.acl,attr,accessType="write"):
                self.apiToken = "ENC {0}".format(auth.getENCFromPassword(value))
                return True
            return False
        return super(_digitaloceanListDroplets, self).setAttribute(attr,value,sessionData=sessionData)

class _digitaloceanGetDropletByName(action._action):
    apiToken = str()
    dropletName = str()

    def run(self,data,persistentData,actionResult):
        apiToken = auth.getPasswordFromENC(self.apiToken)
        dropletName = helpers.evalString(self.dropletName,{"data" : data})

        result = digitalocean._digitalocean(apiToken).listDroplets(name=dropletName)
        if result:
            if "error" in result:
                actionResult["result"] = False
                actionResult["msg"] = result["msg"]
                actionResult["rc"] = result["error"]
            else:
                actionResult["result"] = True
                actionResult["rc"] = 0
                actionResult["droplet"] = result
        else:
            actionResult["result"] = False
            actionResult["rc"] = 500
            actionResult["msg"] = "Unable to get droplet by name, it likely does not exist"
        return actionResult 

    def setAttribute(self,attr,value,sessionData=None):
        if attr == "apiToken" and not value.startswith("ENC "):
            if db.fieldACLAccess(sessionData,self.acl,attr,accessType="write"):
                self.apiToken = "ENC {0}".format(auth.getENCFromPassword(value))
                return True
            return False
        return super(_digitaloceanGetDropletByName, self).setAttribute(attr,value,sessionData=sessionData)

class _digitaloceanGetDroplet(action._action):
    apiToken = str()
    dropletID = str()

    def run(self,data,persistentData,actionResult):
        apiToken = auth.getPasswordFromENC(self.apiToken)
        dropletID = helpers.evalString(self.dropletID,{"data" : data})

        result = digitalocean._digitalocean(apiToken).getDroplet(dropletID)
        if result:
            actionResult["result"] = True
            actionResult["rc"] = 0
            actionResult["droplet"] = result
        else:
            actionResult["result"] = False
            actionResult["rc"] = 500
            actionResult["msg"] = "Failed to get a valid response from API"
        return actionResult 

    def setAttribute(self,attr,value,sessionData=None):
        if attr == "apiToken" and not value.startswith("ENC "):
            if db.fieldACLAccess(sessionData,self.acl,attr,accessType="write"):
                self.apiToken = "ENC {0}".format(auth.getENCFromPassword(value))
                return True
            return False
        return super(_digitaloceanGetDroplet, self).setAttribute(attr,value,sessionData=sessionData)

class _digitaloceanGetDropletPublicNetwork(action._action):
    apiToken = str()
    dropletID = str()

    def run(self,data,persistentData,actionResult):
        apiToken = auth.getPasswordFromENC(self.apiToken)
        dropletID = helpers.evalString(self.dropletID,{"data" : data})

        result = digitalocean._digitalocean(apiToken).getDroplet(dropletID,network=True)
        if result:
            actionResult["result"] = True
            actionResult["rc"] = 0
            actionResult["droplet"] = result
        else:
            actionResult["result"] = False
            actionResult["rc"] = 500
            actionResult["msg"] = "Failed to get a valid response from API"
        return actionResult 

    def setAttribute(self,attr,value,sessionData=None):
        if attr == "apiToken" and not value.startswith("ENC "):
            if db.fieldACLAccess(sessionData,self.acl,attr,accessType="write"):
                self.apiToken = "ENC {0}".format(auth.getENCFromPassword(value))
                return True
            return False
        return super(_digitaloceanGetDropletPublicNetwork, self).setAttribute(attr,value,sessionData=sessionData)


class _digitaloceanCreateDroplet(action._action):
    apiToken = str()
    dropletName = str()
    region = str()
    image = str()
    size = str()
    ssh_key = str()

    def run(self,data,persistentData,actionResult):
        apiToken = auth.getPasswordFromENC(self.apiToken)
        dropletName = helpers.evalString(self.dropletName,{"data" : data})
        region = helpers.evalString(self.region,{"data" : data})
        image = helpers.evalString(self.image,{"data" : data})
        size = helpers.evalString(self.size,{"data" : data})
        ssh_key = int(helpers.evalString(self.ssh_key,{"data" : data}))

        result = digitalocean._digitalocean(apiToken).createDroplet(dropletName,region,image,size,[ssh_key])
        if result:
            actionResult["result"] = True
            actionResult["rc"] = 0
            actionResult["dropletID"] = result
        else:
            actionResult["result"] = False
            actionResult["rc"] = 500
            actionResult["msg"] = "Failed to get a valid response from API"
        return actionResult 

    def setAttribute(self,attr,value,sessionData=None):
        if attr == "apiToken" and not value.startswith("ENC "):
            if db.fieldACLAccess(sessionData,self.acl,attr,accessType="write"):
                self.apiToken = "ENC {0}".format(auth.getENCFromPassword(value))
                return True
            return False
        return super(_digitaloceanCreateDroplet, self).setAttribute(attr,value,sessionData=sessionData)

class _digitaloceanDeleteDroplet(action._action):
    apiToken = str()
    dropletID = str()

    def run(self,data,persistentData,actionResult):
        apiToken = auth.getPasswordFromENC(self.apiToken)
        dropletID = helpers.evalString(self.dropletID,{"data" : data})

        result = digitalocean._digitalocean(apiToken).deleteDroplet(dropletID)
        if result:
            actionResult["result"] = True
            actionResult["rc"] = 0
        else:
            actionResult["result"] = False
            actionResult["rc"] = 500
            actionResult["msg"] = "Failed to get a valid response from API"
        return actionResult 

    def setAttribute(self,attr,value,sessionData=None):
        if attr == "apiToken" and not value.startswith("ENC "):
            if db.fieldACLAccess(sessionData,self.acl,attr,accessType="write"):
                self.apiToken = "ENC {0}".format(auth.getENCFromPassword(value))
                return True
            return False
        return super(_digitaloceanDeleteDroplet, self).setAttribute(attr,value,sessionData=sessionData)

class _digitaloceanWaitForDroplet(action._action):
    apiToken = str()
    dropletID = str()
    timeout = int()

    def run(self,data,persistentData,actionResult):
        apiToken = auth.getPasswordFromENC(self.apiToken)
        dropletID = helpers.evalString(self.dropletID,{"data" : data})

        timeout = 300
        if self.timeout > 0:
            timeout = self.timeout

        result = digitalocean._digitalocean(apiToken).waitForDroplet(dropletID,timeout=timeout)
        actionResult["result"] = result
        actionResult["rc"] = 0
        return actionResult 

    def setAttribute(self,attr,value,sessionData=None):
        if attr == "apiToken" and not value.startswith("ENC "):
            if db.fieldACLAccess(sessionData,self.acl,attr,accessType="write"):
                self.apiToken = "ENC {0}".format(auth.getENCFromPassword(value))
                return True
            return False
        return super(_digitaloceanWaitForDroplet, self).setAttribute(attr,value,sessionData=sessionData)

class _digitaloceanListKeys(action._action):
    apiToken = str()

    def run(self,data,persistentData,actionResult):
        apiToken = auth.getPasswordFromENC(self.apiToken)

        result = digitalocean._digitalocean(apiToken).listKeys()
        if result:
            actionResult["result"] = True
            actionResult["rc"] = 0
            actionResult["keys"] = result
        else:
            actionResult["result"] = False
            actionResult["rc"] = 500
            actionResult["msg"] = "Failed to get a valid response from API"
        return actionResult 

    def setAttribute(self,attr,value,sessionData=None):
        if attr == "apiToken" and not value.startswith("ENC "):
            if db.fieldACLAccess(sessionData,self.acl,attr,accessType="write"):
                self.apiToken = "ENC {0}".format(auth.getENCFromPassword(value))
                return True
            return False
        return super(_digitaloceanListKeys, self).setAttribute(attr,value,sessionData=sessionData)

class _digitaloceanGetKeyByName(action._action):
    apiToken = str()
    keyName = str()

    def run(self,data,persistentData,actionResult):
        apiToken = auth.getPasswordFromENC(self.apiToken)
        keyName = helpers.evalString(self.keyName,{"data" : data})


        result = digitalocean._digitalocean(apiToken).listKeys(name=keyName)
        if result:
            actionResult["result"] = True
            actionResult["rc"] = 0
            actionResult["key"] = result
        else:
            actionResult["result"] = False
            actionResult["rc"] = 500
            actionResult["msg"] = "Failed to get a valid response from API"
        return actionResult 

    def setAttribute(self,attr,value,sessionData=None):
        if attr == "apiToken" and not value.startswith("ENC "):
            if db.fieldACLAccess(sessionData,self.acl,attr,accessType="write"):
                self.apiToken = "ENC {0}".format(auth.getENCFromPassword(value))
                return True
            return False
        return super(_digitaloceanGetKeyByName, self).setAttribute(attr,value,sessionData=sessionData)


class _digitaloceanMyBalance(action._action):
    apiToken = str()

    def run(self,data,persistentData,actionResult):
        apiToken = auth.getPasswordFromENC(self.apiToken)

        result = digitalocean._digitalocean(apiToken).getMyBalance()
        if result:
            actionResult["result"] = True
            actionResult["rc"] = 0
            actionResult["balance"] = result
        else:
            actionResult["result"] = False
            actionResult["rc"] = 500
            actionResult["msg"] = "Failed to get a valid response from API"
        return actionResult 

    def setAttribute(self,attr,value,sessionData=None):
        if attr == "apiToken" and not value.startswith("ENC "):
            if db.fieldACLAccess(sessionData,self.acl,attr,accessType="write"):
                self.apiToken = "ENC {0}".format(auth.getENCFromPassword(value))
                return True
            return False
        return super(_digitaloceanMyBalance, self).setAttribute(attr,value,sessionData=sessionData)