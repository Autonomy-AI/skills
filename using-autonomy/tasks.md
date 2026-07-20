# Run a coding task

1. `list_projects` -> pick `project_id` + `workspace_id`.
2. `start_task(project_id, workspace_id, instruction)` -> returns a `task_id`
   immediately; the work runs in the background.
3. Poll `get_task(project_id, task_id)` until the status is terminal
   (`COMPLETED` / `DISCARDED`) or it needs input. Don't block - report progress.
4. To reply or redirect: `continue_task(project_id, task_id, instruction)`.
   To abort a run that's going wrong: `stop_task`, then `continue_task` with new guidance.
5. `get_task_messages` to read what the agent did; `get_task_pr_diff` for the
   unified diff ("Files Changed"); `list_tasks` to see all tasks.

## Versions
A task can produce multiple versions. `get_task` shows the active one;
`checkout_task_version` switches; `get_task_pr_diff(version=N)` diffs a specific
version; `discard_task_changes` throws away sandbox changes without deleting the task.

## Plan (spec) document
Shape the plan before building: `list_spec_versions` / `get_task_spec_version` to
read, `update_spec_content` to edit the latest in place, `create_spec_version` to
save a new version with history.

## Shipping
When the user has **explicitly approved** the changes, `complete_task` finalizes
the task and opens/updates the PR for their developers. This is irreversible -
never call it without approval.

## Transparency
`list_agent_histories` -> one row per agent run; `get_agent_history_detail` ->
the full trace of a single run.
