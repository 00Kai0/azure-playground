# How to run sample in track2
Because track2 sdks haven't been released yet. We need run it in dev mode.

## 1. Create Dev enviroment for track2
run `install_env_track2.sh`(in linux)   
or you can install these packages from `track2_preview` by yourself

## 2. create env values
We need put app registration information into env values.   
For example in linux:
```bash
export AZURE_TENANT_ID=""
export AZURE_CLIENT_ID=""
export AZURE_CLIENT_SECRET=""
export SUBSCRIPTION_ID=""
```
About how to create app registration, see here: https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app

## 3. test sample
just run `track2.py` to test creating virtualmachine in track2 sdk.   
Atfter finish script, you can find your virtualmachine in azure portal.
