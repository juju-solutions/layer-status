# Overview

This layer provides helpers for managing charm status and ensuring that status
set by different layers are resolved in a reasonable way.

# Usage

The layer library provides helpers to make setting status a bit more friendly:

```python
from charms.reactive import when_not

from charms.layer import status
from charms.layer import foo as charm_lib


@when('config.set.required-config')
@when_not('charm.foo.installed')
def install():
    status.maintenance('installing foo')
    charm_lib.do_install()
    status.active('foo is ready')


@when_not('config.set.required-config')
def missing_required_config():
    status.blocked('missing required-config')
```

More details can be found in the [docs](docs/status.md).

More importantly, status can be set by different layers without worrying about
conflicting with each other.  For instance, if one layer (or the charm) sets
the status to blocked and another layer sets the status to waiting or active,
the status will end up with whichever was set most recently.  This is further
exacerbated by the fact that the order in which reactive handlers are invoked
can be non-determinate and / or hard to reason about, especially across layers.

With this layer, blocked status takes precedence over waiting, which takes
precedence over active, and competing statuses of the same level are handled
in a consistent way based on the layer that set it.  More specifically,
conflicting statuses are resolved in the following way:

* Maintenance status is always set immediately
* Other statuses are queued to be set at the end of the hook execution
* Blocked status will override waiting or active
* Waiting status will override active
* If a given status is set more than once, such as by different layers,
  then the charm layer will take precedence, or the layer latest in the
  built charm's `includes` list will take precedence, or the most recently
  set will be used (i.e., current behavior).  (Note: The name of the layer
  setting the status will be determined by the name of the file containing
  the call, as per the convention of naming reactive or library files after
  the layer that contains them.)

To ensure that layers which use `charmhelpers.core.hookenv.status_set` function
directly work well with this layer, it will be patched to go transparently go
through this layer.  On the off chance that the patching causes issues with
some other layer, you can disable this behavior with the `patch-hookenv` layer
option:

```yaml
includes: ['layer:basic', 'layer:status', ...]
options:
  status:
    patch-hookenv: false
```
