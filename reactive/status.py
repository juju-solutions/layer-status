from charms import layer
from charmhelpers.core.hookenv import atexit


if layer.options('status')['patch-hookenv']:
    layer.status._patch_hookenv()
atexit(layer.status._finalize_status)
