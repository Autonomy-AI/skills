# Autonomy skills

Agent Skills that teach a coding agent (Claude Code, …) how to drive the
Autonomy platform through the `autonomy` MCP server.

These are authored here, next to the MCP server, as the single source of truth
(`using-autonomy` also backs the MCP server's built-in `load_autonomy_skill` tool
and the prose guides on docs.autonomyai.io; `move-to-studio` ships only as an Agent
Skill, since it runs local scripts). A CI job mirrors this directory to the
public **`Autonomy-AI/skills`** repo, which is the install target for the Claude
Code plugin - a public repo is required because a private monorepo folder can't
be a public clone target.

## Layout

```
skills/
├── using-autonomy/
│   ├── SKILL.md          # entry point (progressive disclosure)
│   ├── setup.md          # configure a project
│   ├── tasks.md          # run / iterate / ship a coding task
│   ├── full-mode.md      # whole app vs. staging backend
│   └── troubleshooting.md
├── move-to-studio/
│   ├── SKILL.md          # entry point: rules, inventory, plan
│   ├── connectors.md     # connect every service the person uses
│   ├── repos.md          # link their repos to a Studio project
│   ├── memory.md         # import auto-memory and personal instructions
│   ├── skills.md         # add the skills they pick
│   ├── docs.md           # bring a docs folder into a Space
│   └── scripts/          # local inventory + pack-and-secret-scan helpers
└── .claude-plugin/
    └── plugin.json       # Claude Code plugin manifest
```

## Install (once mirrored to the public repo)

```bash
# Claude Code
/plugin marketplace add Autonomy-AI/skills
/plugin install using-autonomy
```

## Format

Standard [Agent Skills](https://modelcontextprotocol.io) format: a `SKILL.md`
with YAML frontmatter (`name`, `description`) that loads the focused reference
files only when the task needs them.
