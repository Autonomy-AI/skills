# Skills: add the ones the person picks

Adding a skill runs in Studio's web UI.
The MCP tools can read what is already there: `list_skills` for the platform catalog, `list_repo_skills` for skills Studio found in the repo.

## Steps

1. From the inventory, list the person's own skills (`~/.claude/skills` and similar). Skills inside a repo's `.claude/skills` already come with the repo: check `list_repo_skills` and skip those.
2. Mark the ones that won't run in a Studio sandbox: they call a local CLI or script, read local paths, or need local secrets. Tell the person why, so they can rewrite them to use Studio's tools or leave them local.
3. For each skill the person picks: Settings → **Skills** → **Add skill** → paste the whole `SKILL.md` (frontmatter and body) → read back the name and description Studio parsed → **Create skill**.
4. Confirm each one now shows in the Skills list.

A skill with extra files beside its `SKILL.md` (scripts, references) needs those folded into the body, or left out.
Say which ones lost something.
