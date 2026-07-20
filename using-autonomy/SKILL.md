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

1. `list_projects` - pick a `project_id` and (once `READY`) a `workspace_id`.
2. If the project isn't `READY`, load **setup.md** and initialize it first.
3. `start_task(project_id, workspace_id, instruction)` - returns a `task_id`; work runs in the background.
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

- **Never `complete_task` without explicit user approval** - it opens a PR for their developers. It is the irreversible "send to devs" action.
- **Poll, don't block.** Background tools (`start_task`, `continue_task`, `complete_task`, `update_task_env`) return immediately; report progress from `get_task`.
- **You already hold the repo context** - set project config yourself rather than asking a setup agent.

Full documentation: https://docs.autonomyai.io
