from config.system.system_config import *
from config.runtime.runtime_config import *
from config.workers.worker_config import *
from config.security.security_config import *
from config.core.core_config import *

print({
    "system": SYSTEM_NAME,
    "mode": SYSTEM_MODE,
    "runtime": RUNTIME_MODE,
    "workers": MAX_WORKERS,
    "firewall": FIREWALL_MODE,
    "core": CORE_MODE
})
