# Ansible Collection - jam82.meta

![GitHub](https://img.shields.io/github/license/jam82/ansible-collection-meta) ![GitHub last commit](https://img.shields.io/github/last-commit/jam82/ansible-collection-meta) ![GitHub issues](https://img.shields.io/github/issues-raw/jam82/ansible-collection-meta)

## Description

This collection provides a set of modules designed to streamline the ansible
role development and maintenance process.

## Installation

Your need to install the collection from github, as my galaxy account is broken:

```bash
ansible-galaxy collection install git+https://github.com/jam82/ansible-collection-meta.git,main
```

## Usage

After installation, you can use the modules provided by this collection in your playbooks. Here's an example of how to use a module from this collection:

```yaml
    - hosts: all
      tasks:
        - name: "Generate meta/argument_specs.yml"
          jam82.generate_argument_specs:
            defaults_file: /path/to/role/defaults/main.yml
            ouput_file: /path/to/role/meta/argument_specs.yaml
```

## Modules

- **generate_argument_specs**: A module for generating `meta/argument_specs.yml` from a roles' `defaults/main.yml`.

## Plugins

### Inventory

- **ansible_role_inventory**: Inventory plugin for using role directories as inventory hosts with `ansible_connection=local`.

## Playbooks

- **docs.yml**: Generate CONTRIBUTING.md, LICENSE and README.md
- **meta_main.yml**: Generate meta/main.yml
- **meta_requirements.yml**: Generate meta/requirements.yml
- **remove.yml**: Remove configured files from role directory

## Requirements

- ansible >= 2.15

## Contributing

Contributions to this collection are welcome. Please ensure to follow best practices for Ansible role and module development, including documentation for new features and roles. For more details, see the CONTRIBUTING.md file.

## License

[MIT](LICENSE)

## Authors

- Jonas Mauer <jam@kabelmail.net> (@jam82)
