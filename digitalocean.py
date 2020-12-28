from core import plugin, model

class _digitalocean(plugin._plugin):
    version = 0.1

    def install(self):
        # Register models
        model.registerModel("digitaloceanListDroplets","_digitaloceanListDroplets","_action","plugins.digitalocean.models.action")
        model.registerModel("digitaloceanGetDropletByName","_digitaloceanGetDropletByName","_action","plugins.digitalocean.models.action")
        model.registerModel("digitaloceanGetDroplet","_digitaloceanGetDroplet","_action","plugins.digitalocean.models.action")
        model.registerModel("digitaloceanGetDropletPublicNetwork","_digitaloceanGetDropletPublicNetwork","_action","plugins.digitalocean.models.action")
        model.registerModel("digitaloceanCreateDroplet","_digitaloceanCreateDroplet","_action","plugins.digitalocean.models.action")
        model.registerModel("digitaloceanDeleteDroplet","_digitaloceanDeleteDroplet","_action","plugins.digitalocean.models.action")
        model.registerModel("digitaloceanWaitForDroplet","_digitaloceanWaitForDroplet","_action","plugins.digitalocean.models.action")
        model.registerModel("digitaloceanListKeys","_digitaloceanListKeys","_action","plugins.digitalocean.models.action")
        model.registerModel("digitaloceanGetKeyByName","digitaloceanGetKeyByName","_action","plugins.digitalocean.models.action")
        model.registerModel("digitaloceanMyBalance","_digitaloceanMyBalance","_action","plugins.digitalocean.models.action")
        return True

    def uninstall(self):
        # deregister models
        model.deregisterModel("digitaloceanListDroplets","_digitaloceanListDroplets","_action","plugins.digitalocean.models.action")
        model.deregisterModel("digitaloceanGetDropletByName","_digitaloceanGetDropletByName","_action","plugins.digitalocean.models.action")
        model.deregisterModel("digitaloceanGetDroplet","_digitaloceanGetDroplet","_action","plugins.digitalocean.models.action")
        model.deregisterModel("digitaloceanGetDropletPublicNetwork","_digitaloceanGetDropletPublicNetwork","_action","plugins.digitalocean.models.action")
        model.deregisterModel("digitaloceanCreateDroplet","_digitaloceanCreateDroplet","_action","plugins.digitalocean.models.action")
        model.deregisterModel("digitaloceanDeleteDroplet","_digitaloceanDeleteDroplet","_action","plugins.digitalocean.models.action")
        model.deregisterModel("digitaloceanWaitForDroplet","_digitaloceanWaitForDroplet","_action","plugins.digitalocean.models.action")
        model.deregisterModel("digitaloceanListKeys","_digitaloceanListKeys","_action","plugins.digitalocean.models.action")
        model.deregisterModel("digitaloceanGetKeyByName","digitaloceanGetKeyByName","_action","plugins.digitalocean.models.action")
        model.deregisterModel("digitaloceanMyBalance","_digitaloceanMyBalance","_action","plugins.digitalocean.models.action")
        return True

    def upgrade(self,LatestPluginVersion):
        pass
        #if self.version < 0.2:
