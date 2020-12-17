#!/bin/env python
import argparse
import os
import sys
import datetime


if sys.platform != "linux":
    print("Just support in linux :)")
    sys.exit()

os.system("uname -a")

SDK_REPO = "azure-sdk-for-python"
SWAGGER_REPO = "azure-rest-api-specs"
SDK_PATH = SDK_REPO
SWAGGER_PATH = SWAGGER_REPO

with open("template/_version.tp", "r") as f:
    VERSION_TEMPLATE = "".join(f.readlines())

with open("template/first_t2_changelog.tp", "r") as f:
    FIRST_T2_CHANGELOG = "".join(f.readlines())

with open("template/readme_usage.tp") as f:
    README_USAGE = "".join(f.readlines())

def path_join(*args):
    return os.path.join(*args)

def codegen(swagger_name, mode="single"):
    # check update
    os.system("npm install -g autorest")

    python_sdk_folder = path_join(SDK_PATH, "sdk")
    swagger = path_join(SWAGGER_PATH, "specification", swagger_name, "resource-manager/readme.md")
    print(swagger)

    if mode == "multi":
        print("codegen multi mode.")
        cmd = "autorest --version=3.0.6339 --python --track2 --use=@autorest/python@5.5.0 --use=@autorest/modelerfour@4.15.443 --python-sdks-folder={python_sdks_folder} --multiapi {swagger}".format(
            python_sdks_folder=python_sdk_folder,
            swagger=swagger
        )
        print(cmd)
        os.system(cmd)
    else:
        print("codegen single mode.")
        cmd = "autorest --version=3.0.6339 --python --track2 --use=@autorest/python@5.5.0 --use=@autorest/modelerfour@4.15.443 --python-sdks-folder={python_sdks_folder} --python-mode=update {swagger}".format(
            python_sdks_folder=python_sdk_folder,
            swagger=swagger
        )
        print(cmd)
        os.system(cmd)

def update_version(sdk_set_name, package_name, version):

    print("update_version.")
    package_full_name = "azure-mgmt-" + package_name
    package_version_path = path_join(SDK_PATH, "sdk", sdk_set_name, package_full_name, "azure", "mgmt", package_name, "_version.py")
    with open(package_version_path, "w") as f:
        f.write(VERSION_TEMPLATE.format(version=version))

def update_changelog(sdk_set_name, package_name, version):

    print("update changelog.")
    package_full_name = "azure-mgmt-" + package_name
    package_changelog_path = path_join(SDK_PATH, "sdk", sdk_set_name, package_full_name, "CHANGELOG.md")
    update_date = str(datetime.date.today())
    logs = ""

    with open(package_changelog_path, "r") as f:
        f.readline()
        f.readline()
        logs = "".join(f.readlines())
    with open(package_changelog_path, "w") as f:
        new_log = "# Release History\n\n## {version} ({date})\n\n".format(version=version, date=update_date) + FIRST_T2_CHANGELOG + logs
        f.write(new_log)

def update_readme(service_name, sdk_set_name, package_name):

    print("update readme")
    package_full_name = "azure-mgmt-" + package_name
    package_readme_path = path_join(SDK_PATH, "sdk", sdk_set_name, package_full_name, "README.md")
    new_readme = list()

    flag = False
    startword = "#"
    with open(package_readme_path, "r") as f:
        line = f.readline()
        while line != "":
            if line == "# Usage\n":
                flag = True
                startword = "#"
                new_readme.append("# Usage\n")
                new_readme.append(README_USAGE.format(service_name=service_name))
            elif line == "## Usage\n":
                flag = True
                startword = "##"
                new_readme.append("## Usage\n")
                new_readme.append(README_USAGE.format(service_name=service_name))

            if line.startswith(startword) and line != startword + " Usage\n":
                flag = False
            if not flag:
                new_readme.append(line)

            line = f.readline()
    with open(package_readme_path, "w") as f:
        f.write("".join(new_readme))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-version", help="Output package version.")
    parser.add_argument("--base-path", help="the base path including azure-sdk-for-python and azure-rest-api-specs")
    parser.add_argument("--service-name", help="service name")
    parser.add_argument("--swagger-name", help="service swagger name")
    parser.add_argument("--sdk-set-name", help="service sdk set name")
    parser.add_argument("--package-name", help="service package name")
    parser.add_argument("--last-version", help="last pushed version.")
    parser.add_argument("--mode", help="codegen mode: multi and single(default)")


    args = parser.parse_args()
    global SDK_PATH
    SDK_PATH = path_join(args.base_path, SDK_REPO)
    global SWAGGER_PATH
    SWAGGER_PATH = path_join(args.base_path, SWAGGER_REPO)

    # codegen
    codegen(args.swagger_name, mode=args.mode)

    # update version
    update_version(args.sdk_set_name, args.package_name, args.output_version)

    # update changelog
    update_changelog(args.sdk_set_name, args.package_name, args.output_version)

    # update readme
    update_readme(args.service_name, args.sdk_set_name, args.package_name)

    # update setup
    # PASS
    print("Done.")


if __name__ == "__main__":
    main()

