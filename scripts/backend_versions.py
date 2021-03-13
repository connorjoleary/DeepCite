#!/bin/python3
import argparse
import json
import os

DEFAULT_FPATH = os.path.join(os.getcwd(), '..', 'backend', 'lambda', 'defaults.json') 
PACKAGE_FPATH = os.path.join(os.getcwd(), '..', 'extension','package.json')
MANIFEST_FPATH = os.path.join(os.getcwd(), '..', 'extension', 'manifest.json') 

def get_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def update_version(action, curr_version):
    version = [int(x) for x in curr_version.split(".")]
    if len(version) < 3:
        raise Exception(f"Error: Expected the version number format to follow '0.0.0' but instead got '{curr_version}'.")
    if action == 'patch':
        version[2] += 1
        return '.'.join(str(_) for _ in version)
    if action == 'minor':
        version[2] = 0
        version[1] += 1
        return '.'.join(str(_) for _ in version)
    if action == 'major':
        version[2] = 0
        version[1] = 0
        version[0] += 1
        return '.'.join(str(_) for _ in version)
    raise Exception(f"Error: Expected either 'patch', 'minor', or 'major' but instead got '{action}'.")

def extension_update(args):
    defaults = get_json(DEFAULT_FPATH)
    # if the version number is given then use that otherwise get the version number from 'package.json'.
    extension_version = args.number if args.number else get_json(PACKAGE_FPATH)['version']
    defaults['VERSIONS'].update({'EXTENSION': extension_version})
    with open(DEFAULT_FPATH, 'w') as f:
        json.dump(defaults, f, indent=2)

def semantic_versioning(args):
    defaults = get_json(DEFAULT_FPATH)
    service = args.service.upper()
    curr_version = defaults['VERSIONS'][service]
    new_version = update_version(args.action, curr_version)
    # Update the defaults
    defaults['VERSIONS'].update({service: new_version})
    with open(DEFAULT_FPATH, 'w') as f:
        json.dump(defaults, f, indent=2)
    # We also can update the package.json(so can npm) and manifest.json
    if service == 'EXTENSION' and args.force_extension:
        # Update the package.json
        package = get_json(PACKAGE_FPATH)
        # Make sure that the verion hasn't already been updated
        if package['version'] != new_version:
            package['version'] = new_version
            with open(PACKAGE_FPATH, 'w') as f:
                json.dump(package, f, indent=2)
        # Now update the manifest.json
        manifest = get_json(MANIFEST_FPATH)
        # Make sure that the verion hasn't already been updated
        if manifest['version'] != new_version:
            manifest['version'] = new_version
            with open(MANIFEST_FPATH, 'w') as f:
                json.dump(manifest, f, indent=2)
    print(new_version)

def show_versions(args):
    # if neither backend or extension is specified then the default behavior is to display both.
    # `show_all` should only be true when both backend and extension are false.
    show_all = not (args.backend or args.extension)
    if args.backend or show_all:
        print("\nBACKEND")
        defaults_versions = get_json(DEFAULT_FPATH)['VERSIONS']
        print("-- DEFAULT VERSIONS --")
        for k, v in defaults_versions.items():
            print(f"{k}: {v}")
        print(f"From File: {DEFAULT_FPATH}")
    if args.extension or show_all:
        print("\nEXTENSION")
        manifest_version = get_json(MANIFEST_FPATH)['version']
        print(f"MANIFEST: {manifest_version}")
        package_version = get_json(PACKAGE_FPATH)['version']
        print(f"PACKAGE: {package_version}")
        print(f"From Manifest: {MANIFEST_FPATH}")
        print(f"From Package: {PACKAGE_FPATH}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="backend_versions", description='Update and manage the version numbers for the backend.')
    subparsers = parser.add_subparsers()

    extension_parser = subparsers.add_parser('extension', help="Update the backend to have the current extension verion.")
    extension_parser.add_argument(
        '-n',
        '--number',
        type=str,
        help='Explicitly provide the current extension version number.',
        default=False
        )
    extension_parser.add_argument(
        '-r',
        '--refresh',
        action='store_true',
        help='Try and get the extension version number from the "package.json".',
        default=True
        )
    # Set the function that will run if this cmd line arg is selected
    extension_parser.set_defaults(func=extension_update)

    
    version_parser = subparsers.add_parser('version', help="Does semantic versioning for the other services in the backend.")
    version_parser.add_argument(
        'action',
        type=str,
        help='What kind of update to apply to the version number.',
        choices=['major', 'minor', 'patch']
        )
    version_parser.add_argument(
        'service',
        type=str,
        help='Which service do you wish to update.',
        choices=['model', 'lambda', 'api', 'extension']
        )
    version_parser.add_argument(
        '-f',
        '--force-extension',
        action='store_true',
        help='''This will also update extension versions.
         NPM does a better job at versioning package.json, so you most likely want to that first then use this to update the manifest.json.
         The package and manifest are only updated if the versions don't match, so if you "patch extension" with npm then you "version 
         patch extension" only the manifest will be updated.''',
        default=False
        )
    # Set the function that will run if this cmd line arg is selected
    version_parser.set_defaults(func=semantic_versioning)

    show_parser = subparsers.add_parser('show', help="Simply prints out the current versions.(If no argument is provided then it will print out all of the versions)")
    show_parser.add_argument(
        '-b',
        '--backend',
        action='store_true',
        help='List all the versions from the backend.',
        default=False
        )
    show_parser.add_argument(
        '-e',
        '--extension',
        action='store_true',
        help='List all of the versions from the extension.',
        default=False
        )
    # Set the function that will run if this cmd line arg is selected
    show_parser.set_defaults(func=show_versions)
    args = parser.parse_args()
    args.func(args)