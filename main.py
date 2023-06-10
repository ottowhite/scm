#!/usr/bin/env python3
import os
import sys
import subprocess


def printline():
    columns = os.getenv('COLUMNS', subprocess.check_output(['tput', 'cols']).decode().strip())
    print(' ' * int(columns))


def recursively_create_directory(current_dirname):
    if not os.path.isdir(current_dirname):
        recursively_create_directory(os.path.dirname(current_dirname))
        os.mkdir(current_dirname)


def recursively_create_directory_for_file(filepath):
    recursively_create_directory(os.path.dirname(filepath))


def clear_other_hard_links(file_to_clear_hardlinks):
    inode_number = subprocess.check_output(['ls', '-i', file_to_clear_hardlinks]).decode().split()[0]
    hard_link_references = subprocess.check_output(['find', '~', '/etc', '-inum', inode_number, '2>', '/dev/null']).decode().split()

    for file_reference in hard_link_references:
        if os.path.realpath(file_reference) == os.path.realpath(file_to_clear_hardlinks):
            print('Retain:', file_reference)
        else:
            print('Delete:', file_reference)
            subprocess.call(['sudo', 'rm', file_reference])


def create_hard_link(config_file_name, config_file_dst):
    # TODO: Only use sudo if absolutely necessary

    # Evaluate ~
    config_file_dst = os.path.expanduser(config_file_dst)

    recursively_create_directory_for_file(config_file_dst)
    src = os.path.realpath(config_file_name)

    subprocess.call(['sudo', 'ln', '-i', src, config_file_dst])


def hard_link_config_file(config_file_name, config_file_dst):
    if os.path.isfile(config_file_name):
        print("1) Clearing residual hard links for", config_file_name + '.')
        clear_other_hard_links(config_file_name)
        print()

        print("2) Creating hard link:", config_file_name, '->', config_file_dst)
        create_hard_link(config_file_name, config_file_dst)
    else:
        print(config_file_name, 'does not exist, skipping.')


def pull_config_repo(repo_file_name, repo_http_url):
    os.chdir(repo_file_name)

    if os.path.isdir(repo_file_name):
        print('Pulling config file changes from:', repo_http_url)
        subprocess.call(['git', 'pull'])
        os.chdir('..')
    else:
        print('Cloning repository at:', repo_http_url)
        subprocess.call(['git', 'clone', repo_http_url])


def try_hard_link_config_file_if_required(config_directory_line, repo_file_name):
    config_file_name = os.path.join(repo_file_name, 'config_files', config_directory_line.split(',')[0])
    config_file_dst = config_directory_line.split(',')[1]
    config_file_required = config_directory_line.split(',')[2]

    if config_file_required == 'y':
        printline()
        print('Processing:', config_file_name)
        print('Destination:', config_file_dst)
        printline()

        hard_link_config_file(config_file_name, config_file_dst)
    else:
        printline()
        print(config_file_name, 'not required, skipping.')
        printline()


def process_config_files(repo_http_url):
    repo_file_name = os.path.splitext(os.path.basename(repo_http_url))[0]
    pull_config_repo(repo_file_name, repo_http_url)

    with open(os.path.join(repo_file_name, 'config_directory.csv')) as f:
        for config_directory_line in f:
            try_hard_link_config_file_if_required(config_directory_line.strip(), repo_file_name)


if __name__ == '__main__':
    process_config_files(sys.argv[1])