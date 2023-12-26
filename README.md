Cloudmesh Command vbox
=====================

[![GitHub Repo](https://img.shields.io/badge/github-repo-green.svg)](https://github.com/cloudmesh/cloudmesh-vbox)
[![image](https://img.shields.io/pypi/pyversions/cloudmesh-vbox.svg)](https://pypi.org/project/cloudmesh-vbox)
[![image](https://img.shields.io/pypi/v/cloudmesh-vbox.svg)](https://pypi.org/project/cloudmesh-vbox/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[![General badge](https://img.shields.io/badge/Status-Production-<COLOR>.svg)](https://shields.io/)
[![GitHub issues](https://img.shields.io/github/issues/cloudmesh/cloudmesh-vbox.svg)](https://github.com/cloudmesh/cloudmesh-vbox/issues)
[![Contributors](https://img.shields.io/github/contributors/cloudmesh/cloudmesh-vbox.svg)](https://github.com/cloudmesh/cloudmesh-vbox/graphs/contributors)
[![General badge](https://img.shields.io/badge/Other-repos-<COLOR>.svg)](https://github.com/cloudmesh/cloudmesh)


[![Linux](https://img.shields.io/badge/OS-Linux-orange.svg)](https://www.linux.org/)
[![macOS](https://img.shields.io/badge/OS-macOS-lightgrey.svg)](https://www.apple.com/macos)
[![Windows](https://img.shields.io/badge/OS-Windows-blue.svg)](https://www.microsoft.com/windows)


* https://github.com/cloudmesh/cloudmesh.cmd5

The cloudmesh command vbox is a sample command so you can see how easy it is to generate a command. You can clone is and replace the "vbox" with the command name you like.

However there is an easier way, with 

    pip install cloudmesh-sys

Now you need to clone the cloudmesh-common repo

    git clone ...

Next you can generate comands in directories with 

    cms sys generate xyz

which will create a directory cloudmesh-xyz, where the new command xyz is defined.
You can cd into that command and install it with 

    make local




## Manual Page

<!-- START-MANUAL -->
```
Command vbox
============

::

  Usage:
        vbox --file=FILE
        vbox list
        vbox [--parameter=PARAMETER] [--experiment=EXPERIMENT] [COMMAND...]

  This command does some useful things.

  Arguments:
      FILE   a file name
      PARAMETER  a parameterized parameter of the form "a[0-3],a5"

  Options:
      -f      specify the file

  Description:

    > cms vbox --parameter="a[1-2,5],a10"
    >    example on how to use Parameter.expand. See source code at
    >      https://github.com/cloudmesh/cloudmesh-vbox/blob/main/cloudmesh/vbox/command/vbox.py
    >    prints the expanded parameter as a list
    >    ['a1', 'a2', 'a3', 'a4', 'a5', 'a10']

    > vbox exp --experiment=a=b,c=d
    > example on how to use Parameter.arguments_to_dict. See source code at
    >      https://github.com/cloudmesh/cloudmesh-vbox/blob/main/cloudmesh/vbox/command/vbox.py
    > prints the parameter as dict
    >   {'a': 'b', 'c': 'd'}

```
<!-- STOP-MANUAL -->