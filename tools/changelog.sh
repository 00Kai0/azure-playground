#!/bin/bash

mode=$1
swaggerName=$2
packageName=$3
lastVersion=$4
path=/_/azure-sdk-for-python

echo "Autorest start..."
if [ $mode == "multi" ]
then
    echo "multi"
    autorest --version=3.0.6318 --python --track2 --use=@autorest/python@5.4.3 --python-sdks-folder=/_/azure-sdk-for-python/sdk/ --multiapi  /_/azure-rest-api-specs/specification/$swaggerName/resource-manager/readme.md
else
    echo "single"
    autorest --version=3.0.6318 --python --track2 --use=@autorest/python@5.4.3 --python-sdks-folder=/_/azure-sdk-for-python/sdk/ --python-mode=update  /_/azure-rest-api-specs/specification/$swaggerName/resource-manager/readme.md
fi

echo "Changelog start..."
cd /_/azure-sdk-for-python
python /_/azure-sdk-for-python/scripts/dev_setup.py -p azure-mgmt-$packageName
python -m packaging_tools.code_report --last-pypi azure-mgmt-$packageName
python -m packaging_tools.code_report azure-mgmt-$packageName

if [ $mode == "multi" ]
then
    echo "multi"
    python -m packaging_tools.change_log $path/sdk/$packageName/azure-mgmt-$packageName/code_reports/$4/merged_report.json $path/sdk/$packageName/azure-mgmt-$packageName/code_reports/latest/merged_report.json
else
    echo "single"
    python -m packaging_tools.change_log $path/sdk/$packageName/azure-mgmt-$packageName/code_reports/$4/report.json $path/sdk/$packageName/azure-mgmt-$packageName/code_reports/latest/report.json
fi
