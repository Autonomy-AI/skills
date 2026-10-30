"""List every MCP server a person has configured in any agent tool, merged, with the Studio route for each.

Usage: python3 inventory.py <repo_dir>
Reads Claude Code, Codex, Cursor, Claude Desktop, Windsurf, Gemini CLI and VS Code configs,
then lists the repos cloned next to <repo_dir> from the same Git owner (how often each is
cloned = how much it is used).
Never prints a header, env or key value: only whether one is set.
"""

# Keeps the annotations valid on macOS's stock Python 3.9.
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

HOME = Path.home()

# Old vendor endpoints still sitting in configs -> the vendor's current one.
CURRENT_URL = {
    "https://mcp.datadoghq.com/api/unstable/mcp-server/mcp": "https://mcp.datadoghq.com/v1/mcp",
    "https://mcp.launchdarkly.com/mcp/fm": "https://mcp.launchdarkly.com/mcp/launchdarkly",
    "https://mcp.launchdarkly.com/mcp/aiconfigs": "https://mcp.launchdarkly.com/mcp/launchdarkly",
}
# Aggregators whose services Studio's Connectors tab already offers.
COVERED_BY_STUDIO = {"connect.composio.dev": "Studio Connectors already covers this"}
ENV_ARG_FLAGS = ("-e", "--env")  # docker run -e NAME=value
HEADER_ARG_FLAGS = ("--header", "-H")  # mcp-remote <url> --header "Authorization: ..."
SECRET_WORDS = (
    "key",
    "token",
    "secret",
    "password",
    "auth",
    "authorization",
    "sig",
    "signature",
    "credential",
)
# Only these take a hosted server's URL as an arg; any other http arg is the server's own setting.
BRIDGE = re.compile(r"(?:.*/)?(?:mcp-remote|mcp-proxy)(?:@.*)?")
# docker run flags that take a value, so the image is the first arg that is neither.
DOCKER_VALUE_FLAGS = {
    *ENV_ARG_FLAGS,
    "--env-file",
    "-v",
    "--volume",
    "--mount",
    "-p",
    "--publish",
    "--name",
    "-w",
    "--workdir",
    "-u",
    "--user",
    "--network",
    "--entrypoint",
    "--platform",
    "-l",
    "--label",
    "--pull",
    "--cpus",
    "-m",
    "--memory",
    "--add-host",
    "--cap-add",
    "--restart",
    "--device",
    "--gpus",
}
MASK = "<hidden>"


def _secret_name(name: str) -> bool:
    """A credential-named flag or query key: its last `-`/`_`/`.` segment ends in
    a credential word, so `--api-key` and `apiKey` match while `--auth-timeout`
    and `--design-system` do not."""
    return re.split(r"[-_.]", name.strip("-").lower())[-1].endswith(SECRET_WORDS)


def _looks_secret(value: str) -> bool:
    """A long opaque token: 20+ URL-safe chars mixing letters and digits."""
    return (
        len(value) >= 20
        and re.fullmatch(r"[A-Za-z0-9_\-.~+/=]+", value) is not None
        and any(c.isdigit() for c in value)
        and any(c.isalpha() for c in value)
    )


def _safe_url(url: str) -> tuple[str, bool]:
    """The URL with credentials, secret-looking query values and path tokens masked.

    Returns the printable URL and whether anything was masked: a key carried in
    the URL itself (Zapier-style /s/<token>/ paths, ?api_key=) must never be
    printed, and must not be pasted into Studio as an org-wide server either.
    """
    parts = urlsplit(url)
    masked = bool(parts.username or parts.password)
    netloc = (parts.hostname or "") + (f":{parts.port}" if parts.port else "")
    segments = [MASK if _looks_secret(seg) else seg for seg in parts.path.split("/")]
    query = [
        (
            MASK if _looks_secret(k) else k,
            MASK if _secret_name(k) or _looks_secret(v) else v,
        )
        for k, v in parse_qsl(parts.query, keep_blank_values=True)
    ]
    masked = masked or MASK in segments or any(MASK in pair for pair in query)
    printable = urlunsplit(
        (parts.scheme, netloc, "/".join(segments), urlencode(query, safe="<>"), "")
    )
    return printable, masked


def _json(path: Path) -> dict:
    try:
        parsed = json.loads(path.read_text())
    except Exception:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _toml(path: Path) -> dict:
    try:
        import tomllib  # noqa: PLC0415 - Python 3.11+ only; older Pythons skip Codex configs
    except ModuleNotFoundError:
        return {}
    try:
        return tomllib.loads(path.read_text())
    except Exception:
        return {}


def _claude_desktop_config() -> Path:
    if sys.platform == "darwin":
        return HOME / "Library/Application Support/Claude/claude_desktop_config.json"
    if sys.platform == "win32":
        return (
            Path(os.environ.get("APPDATA", HOME)) / "Claude/claude_desktop_config.json"
        )
    return HOME / ".config/Claude/claude_desktop_config.json"


def _codex_configs(repo: Path) -> tuple[Path, Path]:
    return (HOME / ".codex/config.toml", repo / ".codex/config.toml")


def sources(repo: Path) -> list[tuple[str, dict]]:
    """(tool, {name: server_config}) for every config file that exists."""
    out: list[tuple[str, dict]] = []
    out.append(("claude-code", _json(repo / ".mcp.json").get("mcpServers", {})))
    cc = _json(HOME / ".claude.json")
    merged = dict(cc.get("mcpServers", {}))
    for proj in cc.get("projects", {}).values():
        merged.update(proj.get("mcpServers") or {})
    out.append(("claude-code", merged))
    for p in _codex_configs(repo):
        out.append(("codex", _toml(p).get("mcp_servers", {})))
    for p in (HOME / ".cursor/mcp.json", repo / ".cursor/mcp.json"):
        out.append(("cursor", _json(p).get("mcpServers", {})))
    out.append(
        ("claude-desktop", _json(_claude_desktop_config()).get("mcpServers", {}))
    )
    out.append(
        (
            "windsurf",
            _json(HOME / ".codeium/windsurf/mcp_config.json").get("mcpServers", {}),
        )
    )
    out.append(("gemini", _json(HOME / ".gemini/settings.json").get("mcpServers", {})))
    out.append(("vscode", _json(repo / ".vscode/mcp.json").get("servers", {})))
    return [(t, s) for t, s in out if s]


def _scan_args(args: list[str]) -> tuple[list[str], list[str], str | None]:
    """(printable args, auth kinds, first URL arg) - values after a key flag are dropped."""
    printable: list[str] = []
    auth: list[str] = []
    url = None
    skip_next = False
    for arg in args:
        if skip_next:
            skip_next = False
            continue
        flag = arg.split("=", 1)[0]
        if flag in ENV_ARG_FLAGS + HEADER_ARG_FLAGS or (
            flag.startswith("-") and _secret_name(flag)
        ):
            kind = {"-e": "env", "--env": "env", "--header": "headers", "-H": "headers"}
            auth.append(kind.get(flag, "key-arg"))
            skip_next = "=" not in arg
            continue
        if url is None and re.match(r"https?://", arg):
            url = arg
            continue
        if not _looks_secret(arg):
            printable.append(arg)
    return printable, auth, url


def _docker_image(args: list[str]) -> str | None:
    """The image in `docker run [flags] <image> [cmd...]`."""
    if "run" not in args:
        return None
    takes_value = False
    for arg in args[args.index("run") + 1 :]:
        if takes_value:
            takes_value = False
        elif arg.startswith("-"):
            takes_value = "=" not in arg and (
                arg in DOCKER_VALUE_FLAGS or _secret_name(arg)
            )
        else:
            return arg
    return None


def classify(cfg: dict) -> dict:
    url = cfg.get("url") or cfg.get("serverUrl") or cfg.get("httpUrl")
    command = str(cfg.get("command", ""))
    raw_args = [str(a) for a in cfg.get("args", [])]
    args, arg_auth, arg_url = _scan_args(raw_args)
    auth = list(dict.fromkeys(arg_auth))
    if cfg.get("headers") or cfg.get("http_headers"):
        auth.append("headers")
    if cfg.get("env") or cfg.get("env_vars"):
        auth.append("env")
    if cfg.get("bearer_token_env_var") or cfg.get("bearer_token"):
        auth.append("bearer")
    auth = list(dict.fromkeys(auth))
    # A local bridge to a hosted server (npx mcp-remote <url>) is that hosted server.
    if any(BRIDGE.fullmatch(a) for a in [command, *raw_args]):
        url = url or arg_url
    if url:
        url = CURRENT_URL.get(url.rstrip("/"), url)
        host = urlsplit(url).hostname or ""
        url, key_in_url = _safe_url(url)
        if key_in_url:
            auth.append("key-in-url")
        if host in ("127.0.0.1", "localhost", "::1") or host.endswith(".localhost"):
            route = "skip: local dev server"
        elif host in COVERED_BY_STUDIO:
            route = f"skip: {COVERED_BY_STUDIO[host]}"
        elif auth:
            route = "needs the person: key/header (try Connectors sign-in first, else they add it)"
        else:
            route = "connectors first, else org MCP servers: add this URL, then Connect"
        return {
            "transport": "http",
            "target": url,
            "auth": auth or ["oauth-or-none"],
            "route": route,
        }
    image = _docker_image(args) if Path(command).name in ("docker", "podman") else None
    pkg = image or next(
        (
            a
            for a in args
            if a.startswith("@")
            or (a and not a.startswith("-") and "/" not in a and a != "mcp")
        ),
        cfg.get("command", ""),
    )
    target = f"{cfg.get('command', '')} {pkg}".strip()
    route = (
        "mcp-servers: add as stdio"
        if not auth
        else "needs the person: stdio server needs a key/env"
    )
    return {
        "transport": "stdio",
        "target": target,
        "auth": auth or ["none"],
        "route": route,
    }


def main() -> None:
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else ".").expanduser().resolve()
    print(
        "## MCP servers across agent tools (name, transport, target, auth, from, route)"
    )
    merged: dict[str, dict] = {}
    for tool, servers in sources(repo):
        for name, cfg in servers.items():
            if not isinstance(cfg, dict):
                continue
            info = classify(cfg)
            key = info["target"]
            entry = merged.setdefault(key, {"names": set(), "tools": set(), **info})
            entry["names"].add(name)
            entry["tools"].add(tool)
            # The same server is keyless in one tool: prefer the keyless form.
            if info["auth"] != entry["auth"] and "oauth-or-none" in info["auth"]:
                entry.update(info)
    for e in sorted(
        merged.values(),
        key=lambda e: (e["route"].startswith("skip"), sorted(e["names"])[0]),
    ):
        print(
            f"{'/'.join(sorted(e['names']))}\t{e['transport']}\t{e['target']}\tauth={','.join(e['auth'])}\tfrom={','.join(sorted(e['tools']))}\t-> {e['route']}"
        )
    if sys.version_info < (3, 11) and any(p.exists() for p in _codex_configs(repo)):
        print("## codex: needs python 3.11+, skipped")
    sibling_repos(repo)


def _origin(path: Path) -> str:
    try:
        return subprocess.run(
            ["git", "-C", str(path), "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            timeout=5,
        ).stdout.strip()
    except Exception:
        return ""


def _owner_and_name(url: str) -> tuple[str, str] | None:
    """('owner', 'repo') from an https or ssh remote URL."""
    path = url.rstrip("/").removesuffix(".git")
    path = (
        path.split(":", 1)[1]
        if "://" not in path and ":" in path
        else urlsplit(path).path
    )
    parts = [p for p in path.split("/") if p]
    return (parts[-2], parts[-1]) if len(parts) >= 2 else None


def sibling_repos(repo: Path) -> None:
    """Repos cloned beside <repo_dir> from the same owner, most-cloned first (worktrees count as uses)."""
    own = _owner_and_name(_origin(repo))
    if own is None:
        print(
            f"## repos: {repo.name} has no origin remote, so there is no owner to match"
        )
        return
    owner = own[0]
    counts: dict[str, int] = {}
    for d in repo.parent.iterdir():
        if not (d / ".git").exists():
            continue
        found = _owner_and_name(_origin(d))
        if found and found[0] == owner:
            counts[found[1]] = counts.get(found[1], 0) + 1
    print(f"## {owner} repos cloned beside {repo.name} (clones+worktrees)")
    for name, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"{owner}/{name}\t{n}")


if __name__ == "__main__":
    main()
