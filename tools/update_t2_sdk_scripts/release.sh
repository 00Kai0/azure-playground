#!/bin/bash

function check_status() {
	if [ $? != 0 ]
	then
		echo " Failed."
	fi
}

mode=$1
swaggerName=$2
sdkSetName=$3
packageName=$4
version=$5
lastVersion=$6
path=/_/azure-sdk-for-python

if [ $# != 6 ]
then
	echo "release.sh [mode] [swaggerName] [sdkSetName] [packageName] [version] [lastVersion]
Args:
  mode - mode value: single, multi
Example:
  ./release.sh single resoucegraph resources resourcegraph 1.0.0 1.0.0b1"
    exit 1
fi

echo "Update Autorest"
npm install -g autorest
check_status

echo "Autorest start..."
if [ $mode == "multi" ]
then
    echo "multi"
    autorest --version=3.0.6339 --python --track2 --use=@autorest/python@5.5.0 --use=@autorest/modelerfour@4.15.443 --python-sdks-folder=$path/sdk/ --multiapi  /_/azure-rest-api-specs/specification/$swaggerName/resource-manager/readme.md
else
    echo "single"
    autorest --version=3.0.6318 --python --track2 --use=@autorest/python@5.4.3 --use=@autorest/modelerfour@4.15.443 --python-sdks-folder=$path/sdk/ --python-mode=update  /_/azure-rest-api-specs/specification/$swaggerName/resource-manager/readme.md
fi
check_status

echo "Update version..."
echo ""
echo "# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

VERSION = \"$version\"" > $path/sdk/$sdkSetName/azure-mgmt-$packageName/azure/mgmt/$packageName/_version.py
check_status

echo "Setup..."
cd /_/azure-sdk-for-python
python /_/azure-sdk-for-python/scripts/dev_setup.py -p azure-mgmt-$packageName
check_status
echo ""

echo "Mini test"
python -c "import azure.mgmt.$packageName"
check_status
echo ""

echo "Changelog comparing..."
python -m packaging_tools.code_report --last-pypi azure-mgmt-$packageName
check_status
python -m packaging_tools.code_report azure-mgmt-$packageName
check_status

if [ $mode == "multi" ]
then
    echo "multi"
    python -m packaging_tools.change_log $path/sdk/$sdkSetName/azure-mgmt-$packageName/code_reports/$lastVersion/merged_report.json $path/sdk/$sdkSetName/azure-mgmt-$packageName/code_reports/latest/merged_report.json > temp_change.md
else
    echo "single"
    python -m packaging_tools.change_log $path/sdk/$sdkSetName/azure-mgmt-$packageName/code_reports/$lastVersion/report.json $path/sdk/$sdkSetName/azure-mgmt-$packageName/code_reports/latest/report.json > temp_change.md
fi
check_status


# TODO: compare latest version in changelog, if match, do not update changelog again.
echo "Update changelog.."
changelog_path=$path/sdk/$sdkSetName/azure-mgmt-$packageName/CHANGELOG.md
sed -i '1d' $changelog_path
old_changes=`cat $changelog_path`

sed -i '1d' temp_change.md

changes=`cat temp_change.md`
today=`date '+%Y-%m-%d'`

echo "# Release History

## $version ($today)

$changes
$old_changes" > $changelog_path

echo "Done."
