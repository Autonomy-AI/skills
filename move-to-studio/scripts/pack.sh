#!/usr/bin/env bash
# Pack what move-to-studio uploads into Fei Studio, and flag likely secrets.
#   pack.sh inventory <repo_dir>              list memory files, personal instructions and skills
#   pack.sh memory <repo_dir> <out_dir>       zip the Claude Code auto-memory for <repo_dir>,
#                                             plus ~/.claude/CLAUDE.md as GLOBAL-CLAUDE.md
#   pack.sh docs <dir|owner/repo> <out_dir>   zip the documents and images in a folder or repo,
#                                             never packing keys, credentials, env files or private files
# Every zip is scanned first; a line that looks like a secret prints as SECRET? <file>:<line>,
# never with its value. Then the zip prints how to upload it.
set -euo pipefail

SECRET_RE='((^|[^A-Za-z0-9])sk-(ant-[a-z0-9]+-|proj-|live_)?[A-Za-z0-9_]{24,}|[sr]k_(live|test)_[A-Za-z0-9]{16,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|xox[abprs]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|-----BEGIN [A-Z ]*PRIVATE KEY|eyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}|://[^/:@ ]+:[^/@ ]+@|hooks\.slack\.com/services/[A-Za-z0-9/]{20,})'
# Matched case-insensitively, so AWS_SECRET_ACCESS_KEY= and DATABASE_PASSWORD= count too.
SECRET_KEYWORD_RE='([A-Za-z0-9_]*(key|secret|token|password)[A-Za-z0-9_]*["'"'"' ]*[:=] *["'"'"']?[A-Za-z0-9/+_.-]{16,}|bearer +[A-Za-z0-9._~+/-]{16,})'

# docs: never packed, whatever the folder holds.
NEVER_DIRS=(.git .claude .codex .cursor .agents .vscode .idea node_modules __pycache__ credentials secrets)

# Above this, the base64 (4/3 the size) is too long for an agent to write as one tool argument:
# attach the zip in Studio instead.
MCP_UPLOAD_MAX_BYTES=32768

memory_dir() {
  # Claude Code keys memory by an absolute path, every non-alphanumeric turned into '-'.
  # Use the folder's own memory when it has one, else the main repo's (a worktree or subfolder).
  local repo common own
  repo=$(cd "$1" && pwd -P)
  own="$HOME/.claude/projects/${repo//[^A-Za-z0-9]/-}/memory"
  if [ ! -d "$own" ] && common=$(git -C "$repo" rev-parse --path-format=absolute --git-common-dir 2>/dev/null); then
    repo=$(cd "$common/.." && pwd -P)
  fi
  echo "$HOME/.claude/projects/${repo//[^A-Za-z0-9]/-}/memory"
}

scan() {
  # Location only: printing the matched line would put the secret in the agent's transcript.
  local hits
  hits=$({ grep -rInE "$SECRET_RE" "$1"; grep -rIinE "$SECRET_KEYWORD_RE" "$1"; } 2>/dev/null | cut -d: -f1,2 | sort -t: -k1,1 -k2,2n -u | sed "s#^$1/#SECRET? #" || true)
  if [ -n "$hits" ]; then echo "$hits"; else echo "secret scan: no text file matched"; fi
  echo "secret scan: PDFs and images are not scanned; ask the person to check them"
}

upload_hint() {
  local bytes
  bytes=$(wc -c < "$1" | tr -d ' ')
  if [ "$bytes" -le "$MCP_UPLOAD_MAX_BYTES" ]; then
    printf 'upload: small enough for upload_reference_file (%s bytes); base64 it with: base64 < %q | tr -d '"'\\\\n'"'\n' "$bytes" "$1"
  else
    printf 'upload: %s bytes is too big to send through the model; ask the person to attach %q in Studio'"'"'s composer\n' "$bytes" "$1"
  fi
}

drop_links() {
  # zip follows links that find -type f, the prunes and grep -r skip, so a link would ship unscanned.
  find "$1" -type l -print | sed "s#^$1/#skipped link (not packed): #"
  find "$1" -type l -delete
}

need() {
  command -v "$1" >/dev/null 2>&1 || { echo "needs '$1' installed (e.g. brew install $1 / apt install $1)"; exit 1; }
}

case "${1:-}" in
  inventory)
    repo="${2:?repo_dir}"
    mem=$(memory_dir "$repo")
    echo "## memory_dir $mem"
    if [ -d "$mem" ]; then
      n=0; for f in "$mem"/*; do [ -f "$f" ] || continue; echo "${f##*/}"; case "$f" in *.md) n=$((n + 1)) ;; esac; done
      echo "count $n"
    else echo "none"; fi
    echo "## personal instructions"
    for f in "$HOME/.claude/CLAUDE.md" "$HOME/.codex/AGENTS.md" "$HOME/.gemini/GEMINI.md"; do
      if [ -f "$f" ]; then echo "$f ($(wc -l < "$f" | tr -d ' ') lines)"; fi
    done
    echo "## skills"
    for d in "$repo/.claude/skills" "$HOME/.claude/skills" "$HOME/.codex/skills" "$HOME/.agents/skills"; do
      if [ -d "$d" ]; then find -L "$d" -maxdepth 2 -name SKILL.md | sed "s#/SKILL.md##; s#^$d/#$d -> #"; fi
    done | sort -u
    ;;
  memory)
    repo="${2:?repo_dir}"; out="${3:?out_dir}"
    need zip
    mem=$(memory_dir "$repo")
    tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
    if [ -d "$mem" ]; then cp -R "$mem/." "$tmp/"; fi
    drop_links "$tmp"
    if [ -f "$HOME/.claude/CLAUDE.md" ]; then cp "$HOME/.claude/CLAUDE.md" "$tmp/GLOBAL-CLAUDE.md"; fi
    find "$tmp" -name '.*' -prune -exec rm -rf {} +
    if [ -z "$(ls -A "$tmp")" ]; then echo "nothing to pack: no memory at $mem and no ~/.claude/CLAUDE.md"; exit 1; fi
    scan "$tmp"
    mkdir -p "$out"; out=$(cd "$out" && pwd -P); rm -f "$out/memory.zip"
    (cd "$tmp" && zip -qr "$out/memory.zip" .)
    echo "zip $out/memory.zip ($(find "$tmp" -type f | wc -l | tr -d ' ') files)"
    upload_hint "$out/memory.zip"
    ;;
  docs)
    src="${2:?dir or owner/repo}"; out="${3:?out_dir}"
    need zip
    mkdir -p "$out"; out=$(cd "$out" && pwd -P)
    tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT; mkdir -p "$tmp/src"
    if [ -d "$src/.git" ]; then git -C "$src" archive HEAD | tar -x -C "$tmp/src"   # tracked files only
    elif [ -d "$src" ]; then cp -R "$src/." "$tmp/src/"
    elif [[ "$src" =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ ]]; then need gh; gh repo clone "$src" "$tmp/src" -- --depth 1 -q
    else echo "not a folder or an owner/repo: $src"; exit 1; fi
    drop_links "$tmp/src"
    cd "$tmp/src"
    for d in "${NEVER_DIRS[@]}"; do find . -type d -name "$d" -prune -exec rm -rf {} +; done
    find . \( -name '*-private*' -o -name '*.pem' -o -name '*.key' -o -name '*.p12' -o -name '.env*' -o -name '.DS_Store' \) -prune -exec rm -rf {} +
    find . -type f ! \( -iname '*.md' -o -iname '*.mdx' -o -iname '*.html' -o -iname '*.txt' -o -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.gif' -o -iname '*.svg' -o -iname '*.pdf' \) -delete
    find . -type d -empty -delete
    if [ -z "$(ls -A .)" ]; then echo "nothing to pack: no documents or images in $src"; exit 1; fi
    cd - >/dev/null
    scan "$tmp/src"
    rm -f "$out/docs.zip"
    (cd "$tmp/src" && zip -qr "$out/docs.zip" .)
    echo "zip $out/docs.zip ($(find "$tmp/src" -type f | wc -l | tr -d ' ') files)"
    upload_hint "$out/docs.zip"
    ;;
  *) sed -n 2,9p "$0"; exit 2 ;;
esac
