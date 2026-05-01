"""
Common filter plugins for Ansible.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import json
import yaml
from ansible.errors import AnsibleFilterError
from ansible.module_utils.common.text.converters import to_text


class QuotedString(str):
    """String value emitted with double quotes."""


class LiteralString(str):
    """Multiline string value emitted as block literal."""


class LintableDumper(yaml.SafeDumper):
    """Safe YAML dumper with ansible-lint friendly indentation."""

    def increase_indent(self, flow: bool = False, indentless: bool = False) -> Any:
        return super().increase_indent(flow, False)

    def ignore_aliases(self, data: Any) -> bool:
        return True


def _represent_quoted_string(dumper: yaml.Dumper, data: QuotedString) -> yaml.Node:
    return dumper.represent_scalar(
        "tag:yaml.org,2002:str",
        str(data),
        style='"',
    )


def _represent_literal_string(dumper: yaml.Dumper, data: LiteralString) -> yaml.Node:
    return dumper.represent_scalar(
        "tag:yaml.org,2002:str",
        str(data),
        style="|",
    )


LintableDumper.add_representer(QuotedString, _represent_quoted_string)
LintableDumper.add_representer(LiteralString, _represent_literal_string)


def _plain(value: Any) -> Any:
    """
    Convert Ansible/Jinja wrapper objects into plain Python YAML-safe values.
    """
    if isinstance(value, Mapping) or hasattr(value, "items"):
        return {to_text(key): _plain(val) for key, val in value.items()}

    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_plain(item) for item in value]

    if value is None or isinstance(value, bool | int | float):
        return value

    return to_text(value)


def _prepare(value: Any) -> Any:
    """
    Prepare plain Python values for deterministic, lintable YAML output.

    Mapping keys stay plain strings.
    String values are quoted or emitted as literal blocks.
    """
    if isinstance(value, dict):
        return {str(key): _prepare(val) for key, val in value.items()}

    if isinstance(value, list):
        return [_prepare(item) for item in value]

    if isinstance(value, str):
        if "\n" in value:
            return LiteralString(value)
        return QuotedString(value)

    return value


def to_lintable_yaml(value: Any, indent: int = 2, sort_keys: bool = False) -> str:
    """
    Convert any Ansible-renderable value into deterministic, ansible-lint-safe YAML.
    """
    try:
        data = json.loads(json.dumps(_plain(value), default=to_text))
        data = _prepare(data)
        return yaml.dump(
            data,
            Dumper=LintableDumper,
            default_flow_style=False,
            indent=indent,
            sort_keys=sort_keys,
            allow_unicode=True,
            width=120,
        ).rstrip()
    except Exception as exc:
        raise AnsibleFilterError(
            f"to_lintable_yaml filter plugin error: {exc}"
        ) from exc


class FilterModule:
    """Ansible filter module."""

    def filters(self) -> dict[str, Any]:
        return {
            "to_lintable_yaml": to_lintable_yaml,
        }
