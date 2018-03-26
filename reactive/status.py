from charmhelpers.core.hookenv import atexit

from charms import layer
from charms.layer import status


if layer.options('status')['patch-hookenv']:
    status._patch_hookenv()
atexit(status._finalize_status)
