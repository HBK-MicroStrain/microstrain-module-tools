import os

c.JupyterLabTemplates.template_dirs = [os.path.join(os.path.dirname(__file__), "templates")]
c.JupyterLabTemplates.include_default = False

# Shut down kernels automatically when the browser tab is closed.
# cull_connected=False means only kernels with no active connections are eligible.
# After closing a tab, the WebSocket drops and the kernel is culled after cull_idle_timeout seconds.
c.MappingKernelManager.cull_idle_timeout = 5
c.MappingKernelManager.cull_interval = 5
c.MappingKernelManager.cull_connected = False
c.MappingKernelManager.buffer_offline_messages = False

# Shut down the server process once all kernels are gone and no browser connections remain.
c.ServerApp.shutdown_no_activity_timeout = 5
