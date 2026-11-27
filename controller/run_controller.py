from os_ken.base import app_manager

app_manager.AppManager.run_apps([
    'controller.controller',
    'os_ken.controller.ofp_handler'
])
