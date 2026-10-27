---
name: move-to-studio
description: >-
  Move a person's local AI coding setup (Claude Code, Codex, Cursor, Claude
  Desktop and others) into Fei Studio: connect every service they use, link
  their repos, import their memory and personal instructions, add their skills,
  and bring a folder of docs into a Space. Use when the user says "move to
  studio", wants to migrate or onboard their setup into Autonomy, or asks how
  to bring their connectors, memory or skills over.
---

# Move to Studio

You are moving one person's local agent setup into Fei Studio (https://studio.autonomyai.io).
You do the work; the person approves.
Use the `autonomy` MCP tools wherever one exists, and Studio's web UI for the rest.
If you have browser tools, drive Studio yourself; if not, give the person the exact clicks and wait for them.

## Usage

- "move to studio" (or "all"): every part below, in order.
- One part at a time: `connectors`, `repos`, `memory`, `skills`, `docs`.

## Rules

- **Never type a password, API key, token or secret** into any page or tool, and never repeat one back. Leave key forms and vendor logins open for the person.
- **Vendor approval screens:** ask once, in chat, for permission to click Approve on the sign-in screens of the services the person picked. Click Approve only when the screen sends the person back to `autonomyai.io` or an address ending in `.autonomyai.io`; a look-alike such as `autonomyai.io.example.com` does not count. Anything else: stop and show the person.
- **The person's choices stay theirs:** which repos, which memories to keep, which skills, which Google account or Notion pages to share. Show the options and ask; don't decide.
- **Org-wide changes** (importing a repo, adding an MCP server for the whole org) affect every member. Do them only if the person is an org admin and says yes; otherwise list them for an admin.
- **Nothing leaves the machine unchecked.** Every zip goes through the secret scan in `scripts/pack.sh`, and the person clears each `SECRET?` line before anything is uploaded. The scripts never print a secret's value; don't print one yourself when you open a flagged line.
- **Verify every step from what Studio shows** (a tool result, the page text), not from a click having gone through.

## Step 1: Inventory and plan

1. Run the inventory from the repo the person mostly works in:
   - `python3 <skill_dir>/scripts/inventory.py <repo_dir>`: MCP servers from every agent tool on the machine, merged by URL, with each one's auth type and Studio route; then the repos cloned beside `<repo_dir>`, most used first.
   - `bash <skill_dir>/scripts/pack.sh inventory <repo_dir>`: memory files, personal instructions and skills.
2. Add every connector your own session exposes that the configs don't list (for example claude.ai connectors such as Gmail, Google Drive or Calendar), whether signed in or not.
3. `list_connector_status` shows what is already connected in Studio. Those are done.
4. `list_projects` shows the person's Studio projects. Ask which one is theirs to import into, or offer to create one (`create_project` can't be undone, so confirm the name first).
5. Show one plan table: each item, where it goes in Studio (map below), and what the person has to do themselves. Get a single "go", plus the vendor-approval permission.

| Local setup | In Studio | Shared with |
|---|---|---|
| MCP server or connector (Slack, Linear, Figma, Notion…) | Settings → Connectors, or Settings → MCP servers | Sign-ins: the person. MCP server list: the org |
| Auto-memory and personal instructions (`~/.claude/CLAUDE.md`) | Personal memory, or workspace memory for repo facts | Personal: the person. Workspace: everyone on the repo |
| `CLAUDE.md` / `AGENTS.md` / rules inside a repo | Nothing to do: Studio reads them from the checkout | Everyone on the repo |
| Skill | Settings → Skills → Add skill | The project |
| A folder of docs or notes | A Space | The project, or the person |
| Repos they work in | A project in Studio, linked to each repo | The org |

## Then, one part at a time

Load only the file for the part you are on.

- **[connectors.md](./connectors.md)**: every service the person uses.
- **[repos.md](./repos.md)**: link their repos to a Studio project.
- **[memory.md](./memory.md)**: import auto-memory and personal instructions.
- **[skills.md](./skills.md)**: add the skills they pick.
- **[docs.md](./docs.md)**: bring a docs folder into a Space.

## Step last: Report

One table: each item, then "done via <route>" or "waiting on you: <exact click or key>".
Then list any Studio tabs left open for the person, and anything that didn't carry over cleanly.
