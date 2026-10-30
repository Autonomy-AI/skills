# Skills: add the ones the person picks

Skills belong to a project's repository: everyone on it can run one as `/slug`.

## Steps

1. From the inventory, list the person's own skills (`~/.claude/skills` and similar). Skills inside a repo's `.claude/skills` already come with the repo: check `list_repo_skills(project_id, workspace_id)` and skip those.
2. Mark the ones that won't run in a Studio sandbox: they call a local CLI or script, read local paths, or need local secrets. Tell the person why, so they can rewrite them to use Studio's tools or leave them local.
3. For each skill the person picks, read its SKILL.md and call `create_skill(project_id, workspace_id, slug, name, description, body)`. It needs an org admin.
   - `slug` is the frontmatter's `slug`, else the skill's folder name. `name` and `description` come from the frontmatter; `body` is everything after it.
   - The body is at most 8000 characters, and only the SKILL.md is stored. Files beside it (scripts, references) are not: fold what the skill needs into its body, or tell the person what it lost.
   - A refusal names the reason (a taken slug, a built-in's slug, too long): fix it and try again.
   - Not an admin: the person can paste the same fields into Studio's Settings → **Skills** → **Add skill**, or ask an admin.
4. Confirm each one with `list_repo_skills(project_id, workspace_id)`.

**No shell:** ask the person to paste each SKILL.md (or attach it), and which of their skills they want. A skill they use in Claude Desktop or claude.ai is the same format, so split its SKILL.md into fields the same way. Then steps 2 to 4. If `create_skill` names a line that holds a credential, handle it the way the rules say.

To change one later, `update_skill(project_id, workspace_id, slug, ...)` with only the fields that change (`name`, `description`, `body`); to switch one off, `update_skill(project_id, workspace_id, slug, enabled=false)`.
