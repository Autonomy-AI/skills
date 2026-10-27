# Run a coding task

1. `list_projects` -> pick a `project_id`. A project links one workspace at most,
   so `start_task` can omit `workspace_id`. A project with an empty `workspaces`
   list is usually gitless: start it in planner, discover or prototype - it has
   no code to build.
2. `start_task(project_id, instruction)` -> returns a `task_id`
   immediately; the work runs in the background.
3. Poll `get_task(project_id, task_id)` until the status is terminal
   (`COMPLETED` / `DISCARDED`) or it needs input. Don't block - report progress.
4. To reply or redirect: `continue_task(project_id, task_id, instruction)`.
   Sent mid-run it answers `queued: true` - parked in the change-request line, not
   dropped, so don't re-send. `get_task_queue` reads that line back: `queued` still
   dispatches by itself; `refused` is a request the gate turned down for good, with
   the reason. Check it when a follow-up seems to have gone nowhere.
   To abort a run that's going wrong: `stop_task`, then `continue_task` with new guidance.
   Every follow-up on this line of work goes here - refinements, broadened scope,
   corrections. Don't `start_task` again for them: two tasks can't be combined
   once they exist, so that splits one piece of work across several tasks
   permanently. If you're unsure an existing task covers it, `list_tasks` first
   and ask the user which they mean. (An archived or discarded task can't be
   continued - start a new one there.)

   A follow-up sent while a run is in flight waits for that run and then executes
   as its own turn. Pass `delivery="steer"` to have it join the running turn at
   the agent's next step instead. Steer when the message *corrects* what the run
   is doing right now, and waiting would mean correcting finished work; leave the
   default when it *adds* to a sequence the agent is part-way through, because
   arriving mid-sequence makes it abandon the half-finished part. Either way the
   message runs exactly once - the only thing this changes is when.
5. `get_task_messages` to read what the agent did; `get_task_pr_diff` for the
   unified diff ("Files Changed"); `list_tasks` to see all tasks.

## Versions
A task can produce multiple versions. `get_task` shows the active one;
`checkout_task_version` switches; `get_task_pr_diff(version=N)` diffs a specific
version; `discard_task_changes` throws away sandbox changes without deleting the task.

## Showing the result
`get_version_preview_url(project_id, task_id)` -> the preview of a finished
version (a published build; the link keeps working after the sandbox is gone,
and opens for anyone signed in to Studio who can see the project).
This is the one to share when the user wants to see the result. When it answers
with no `preview_url`, its `reason` says why - report that reason rather than
guessing: `building` / `build_failed` are about this build, while `not_built` and
`no_variants_indexed` mean nothing was ever published for that version.

`get_task_preview_url` / `get_storybook_url` are a **different** surface: the
task's live sandbox, serving whatever is checked out right now. Use them to watch
work in progress, never as a stand-in for a version's preview - the hosts look
alike, so the user can't catch the substitution. The exception is a `not_built` /
`no_variants_indexed` reason above: Studio's own version card falls back to the
live app there, so offer it too, named as the live app. Both hand back a URL even when
nothing is listening, so check that before sharing one: the live app needs BOTH
`dev_port_listening` and `proxy_listening` (it is served through a reverse proxy,
which is not started while a task is running), the variants server needs
`dev_server_running`.

## Plan document
The plan is a Space page at `task/PLAN.md`, versioned by the Space itself. Read it
with `get_space_page_content`. No tool here writes it: the planner owns that page,
and a person edits it in the Space view.

## Shipping
When the user has **explicitly approved** the changes, `complete_task` finalizes
the task and opens/updates the PR for their developers. This is irreversible -
never call it without approval.

## Transparency
`get_task_messages` -> the chat timeline: the agent's reasoning, its tool calls,
version cards, and any pending approval/question card (with the `tool_call_id`
you answer it with).
