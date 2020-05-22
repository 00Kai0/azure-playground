import argparse
import os
from string import Template

template = '''# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.${target} import ${Target}ManagementClient
from azure.mgmt.resource import ResourceManagementClient

# - other dependence -
# - end -


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    ${Res_name} = "${res_var}xxyyzz"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    ${target}_client = ${Target}ManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    # - init depended client -
    # - end -

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # - init depended resources -
    # - end -

    # Create ${resource}
    ${res_var} = ${target}_client.${res_obj}.${is_lro}create_or_update(
        GROUP_NAME,
        ${Res_name},
        {
            # TODO: init resource body
        }
    )${need_result}
    print("Create ${resource}:\\n{}".format(${res_var}))

    # Get ${resource}
    ${res_var} = ${target}_client.${res_obj}.get(
        GROUP_NAME,
        ${Res_name}
    )
    print("Get ${resource}:\\n{}".format(${res_var}))

    # Update ${resource}
    ${res_var} = ${target}_client.${res_obj}.${is_lro}update(
        GROUP_NAME,
        ${Res_name},
        {
            # TODO: init resource body
        }
    )${need_result}
    print("Update ${resource}:\\n{}".format(${res_var}))
    
    # Delete ${resource}
    ${res_var} = ${target}_client.${res_obj}.${is_lro}delete(
        GROUP_NAME,
        ${Res_name}
    )${need_result}
    print("Delete ${resource}.\\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()
'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", help="output file")
    parser.add_argument("--is-lro", help="is this a LRO request")
    parser.add_argument("--resource-client", help="client for this resource.")
    parser.add_argument("--resource", help="resource for this sample.")

    output_path = os.getcwd() + "/sample.py"
    args = parser.parse_args()
    if not args.resource_client:
        print("resource-client is needed.")
        print("example:  python tt.py --out=/_/sample.py --is-lro=True --resource-client=network --resource=virtual_network")
        return 0
    if not args.resource:
        print("resource is needed.")
        print("example:  python tt.py --out=/_/sample.py --is-lro=True --resource-client=network --resource=virtual_network")
    if args.out:
        # default is current path
        if not args.out.endswith(".py"):
            print("output file should like: /../sample.py")
            print("example:  python tt.py --out=/_/sample.py --is-lro=True --resource-client=network --resource=virtual_network")
            return 0
        output_path = args.out

    target = args.resource_client
    Target = target[0].upper() + target[1:].lower()
    res_var = args.resource.lower()
    Res_name = res_var.upper()
    resource = " ".join([s.lower() for s in res_var.split("_")])
    res_obj = res_var + "s"
    is_lro = ""
    need_result = ""
    if args.is_lro:
        is_lro = "begin_"
        need_result = ".result()"

    temp = Template(template)
    code = temp.substitute(
        target=target,
        Target=Target,
        Res_name=Res_name,
        res_var=res_var,
        resource=resource,
        res_obj=res_obj,
        is_lro=is_lro,
        need_result=need_result
    )

    with open(output_path, "w") as f:
        f.write(code)
    print("create sample to {} successfully.".format(output_path))

if __name__ == '__main__':
    main()

