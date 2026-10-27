---
name: using-autonomy
description: >-
  Drive the Autonomy coding platform through its MCP server - set up a project,
  run coding tasks, enable Full Mode, and ship changes to developers. Use when
  the user wants to build, edit, or ship front-end code via Autonomy, or has the
  `autonomy` MCP server connected.
---

# Using Autonomy

Autonomy is a coding platform you drive through the `autonomy` MCP server. You
pick a project, run a coding task from a natural-language instruction, review the
result, and send it to the user's developers as a pull request. The platform runs
the work in a sandbox - you orchestrate and report progress.

## First moves

1. `list_projects` - pick a `project_id`. A project with an empty `workspaces` list is usually gitless: it runs planner, discover and prototype tasks only.
2. To connect a repository to a project, load **setup.md**.
3. `start_task(project_id, instruction)` - returns a `task_id`; work runs in the background. Pass `workspace_id` only if `start_task` asks for one.
4. Poll `get_task` until terminal (`COMPLETED` / `DISCARDED`) or awaiting input. Don't block.
5. Review with `get_task_messages` and `get_task_pr_diff`; iterate with `continue_task`.
6. On the user's approval, `complete_task` to ship (opens/updates the PR).

## Load the focused reference for the task at hand

Read only the file that matches what the user is doing - not all of them.

- **[setup.md](./setup.md)** - configure a project (install/validate/dev commands, env vars) so the agent can build in it.
- **[tasks.md](./tasks.md)** - the full task lifecycle: start, poll, iterate, versions, plan document, ship.
- **[full-mode.md](./full-mode.md)** - run the whole app against the user's staging backend.
- **[troubleshooting.md](./troubleshooting.md)** - 401 / 410 / 403 and setup-stuck fixes.

## Rules

- **Never `complete_task` without explicit user approval** - it opens a PR for their developers. It is the irreversible "ship to devs" action.
- **`start_task` is for new work only.** If the user is refining, broadening, or correcting something an existing task already covers, `continue_task` on that `task_id`. Two tasks can't be combined once they exist, so a follow-up sent as a new task splits one line of work permanently. If you're unsure, `list_tasks` first and ask which they mean. An archived or discarded task can't be continued - start a new one there.
- **Poll, don't block.** Background tools (`start_task`, `continue_task`, `complete_task`, `send_setup_message`) return immediately; report progress from `get_task`.
- **You already hold the repo context** - set project config yourself rather than asking a setup agent.

Full documentation: https://docs.autonomyai.io
