# Copyright (c) 2026 Mark Deazley. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
"""Pure formatting functions for admin MCP tool responses."""

from __future__ import annotations


def format_disk_quota(bytes_val: int) -> str:
    """Format a byte count as human-readable (KB/MB/GB)."""
    if bytes_val <= 0:
        return "0"
    if bytes_val >= 1_073_741_824:
        return f"{bytes_val / 1_073_741_824:,.1f} GB"
    if bytes_val >= 1_048_576:
        return f"{bytes_val / 1_048_576:,.0f} MB"
    if bytes_val >= 1_024:
        return f"{bytes_val / 1_024:,.0f} KB"
    return f"{bytes_val} B"


def _format_number(val: int | float) -> str:
    """Format a number with comma separators."""
    if isinstance(val, float):
        return f"{val:,.2f}"
    return f"{val:,}"


def _format_perm_value(key: str, val: object) -> str:
    """Format a single permission value for display."""
    if isinstance(val, bool):
        return "true" if val else "false"
    if key == "disk_quota" and isinstance(val, (int, float)):
        return format_disk_quota(int(val))
    if key == "mongo_query_quota" and isinstance(val, (int, float)) and int(val) <= 0:
        return "unlimited"
    if isinstance(val, list):
        if len(val) == 1 and val[0] == "*":
            return "*"
        return ", ".join(str(x) for x in val)
    if isinstance(val, (int, float)):
        return _format_number(val)
    return str(val)


# Permission keys grouped by section for display
_SECTIONS: list[tuple[str, list[str]]] = [
    ("System", [
        "max_sessions", "instruction_budget", "role_admin", "allowlist_admin",
        "list_sessions", "session_kick",
        "send_system_notification", "send_user_notification",
    ]),
    ("LVFS", [
        "lvfs_modify", "disk_quota",
    ]),
    ("Network Client", [
        "net_client_allowed", "net_client_domains", "net_client_quota",
    ]),
    ("Network Server", [
        "net_server_bind", "net_server_tcp", "net_server_udp",
    ]),
    ("Code Execution", [
        "evaluate", "evaluate_tainted",
    ]),
    ("Database", [
        "mongo_access", "mongo_query_quota",
    ]),
]


def format_roles_list(data: dict) -> str:
    """Format admin_list_roles response as a table.

    Server returns: {"roles": ["admin", "beta-tester", ...], "default_role": "...", "count": N}
    """
    roles = data.get("roles", [])
    default_role = data.get("default_role", "")

    lines = [f"Roles ({len(roles)}):"]
    if roles:
        # roles is a list of strings
        names = sorted(roles) if roles else []
        max_w = max((len(n) for n in names), default=4)
        max_w = max(max_w, 4)  # minimum "NAME" width
        lines.append(f"  {'NAME':<{max_w}}   DEFAULT")
        for name in names:
            marker = " *" if name == default_role else ""
            lines.append(f"  {name:<{max_w}}  {marker}")
    lines.append("")
    lines.append(f"Default role: {default_role}")
    return "\n".join(lines)


def format_role_detail(data: dict) -> str:
    """Format admin_get_role response as grouped key/value.

    Server returns: {"role": "admin", "permissions": {...}, "is_default": true/false}
    """
    name = data.get("role", data.get("name", "?"))
    is_default = data.get("is_default", False)
    perms = data.get("permissions", {})

    default_str = "yes" if is_default else "no"
    lines = [f"Role: {name} (default: {default_str})", ""]

    # Find max key width across all sections for alignment
    all_keys = [k for _, keys in _SECTIONS for k in keys if k in perms]
    max_key_w = max((len(k) for k in all_keys), default=20)

    seen_keys: set[str] = set()
    for section_name, keys in _SECTIONS:
        section_keys = [k for k in keys if k in perms]
        if not section_keys:
            continue
        lines.append(f"  {section_name}:")
        for k in section_keys:
            val = perms[k]
            formatted = _format_perm_value(k, val)
            lines.append(f"    {k + ':':<{max_key_w + 1}}  {formatted}")
            seen_keys.add(k)
        lines.append("")

    # Any remaining keys not in known sections
    extra = {k: v for k, v in perms.items() if k not in seen_keys}
    if extra:
        lines.append("  Other:")
        for k, v in sorted(extra.items()):
            formatted = _format_perm_value(k, v)
            lines.append(f"    {k + ':':<{max_key_w + 1}}  {formatted}")
        lines.append("")

    return "\n".join(lines)


def format_users_list(data: dict) -> str:
    """Format admin_list_users response as a table."""
    users = data.get("users", [])
    default_role = data.get("default_role", "")

    lines = [f"Users ({len(users)}):"]
    if users:
        max_uid = max(len(u.get("user_id", "")) for u in users)
        max_uid = max(max_uid, 7)  # minimum "USER ID" width
        lines.append(f"  {'USER ID':<{max_uid}}   ROLE")
        for u in users:
            uid = u.get("user_id", "")
            role = u.get("role", "")
            lines.append(f"  {uid:<{max_uid}}   {role}")
    lines.append("")
    lines.append(f"Default role: {default_role}")
    return "\n".join(lines)


def format_mutation_result(data: dict) -> str:
    """Format a mutation result as a one-liner.

    Server returns various shapes:
    - set_role: {"action": "created"|"updated", "role": "..."}
    - delete_role: {"action": "deleted", "role": "..."}
    - set_user_role: {"user_id": "...", "role": "..."}
    - delete_user: {"action": "deleted", "user_id": "...", "previous_role": "...", "now_defaults_to": "..."}
    - reload: {"action": "reloaded", "directory": "...", "roles_count": N, "users_count": N}
    """
    action = data.get("action", "")
    role = data.get("role", "")
    user_id = data.get("user_id", "")

    if action == "reloaded":
        rc = data.get("roles_count", "?")
        uc = data.get("users_count", "?")
        return f"Configuration reloaded. {rc} roles, {uc} users."

    if action == "deleted" and user_id:
        prev = data.get("previous_role", "?")
        default = data.get("now_defaults_to", "?")
        return f"User '{user_id}' deleted. Previous role: {prev}. Now defaults to: {default}."

    if action == "deleted" and role:
        return f"Role '{role}' deleted."

    if action in ("created", "updated") and role:
        return f"Role '{role}' {action}."

    if user_id and role:
        return f"User '{user_id}' assigned to role '{role}'."

    # Fallback
    return str(data)
