#!/bin/bash bash
pathToVirtualEnv=$PWD
interpreter=/usr/bin/python3.6
pipInstaller=/usr/bin/pip3

. $pathToVirtualEnv/bin/activate
$pipInstaller install flask
$pipInstaller install requests
$pipInstaller install matplotlib
$pipInstaller install pandas
$pipInstaller install datetime
