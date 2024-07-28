#!/usr/bin/env python3
import subprocess
import argparse
import os

parser = argparse.ArgumentParser(prog="adbsync",description="Syncs directory with an android device")
parser.add_argument("target", help="Target folder on remote device (required)")
parser.add_argument("local", help="List of folders that should be synced (default: all in current directory)", nargs='*', default=os.walk("."))
args = parser.parse_args()

# I know that this sucks
# Please don't complain about it
for name in args.local:
    print('!! Syncing', name)
    subprocess.check_output([
        'adb', 'shell', f'mkdir -p {args.target}/{name}'
    ])
    remote = subprocess.check_output([
        'adb', 'shell', f'ls {args.target}/{name}'
    ]).decode().strip().split('\n')
    local = os.listdir(name)
    delete = list()
    for path in remote:
        if path in local:
            continue
        delete.append(f'\"{args.target}/{name}/{path}\"')
    print(len(delete), 'files will be deleted')

    if len(delete) > 0:
        for arr in [delete[i:i + 250] for i in range(0, len(delete), 250)]:
            subprocess.call(['adb', 'shell', f'rm {' '.join(arr)}'])

    push = list()
    for path in local:
        if path in remote:
            continue
        push.append(f'./{name}/{path}')
    print(len(push), 'files will be pushed')

    if len(push) > 0:
        for arr in [push[i:i + 250] for i in range(0, len(push), 250)]:
            subprocess.call(['adb', 'push'] + arr + [f'{args.target}/{name}/'])
