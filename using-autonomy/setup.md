# Set up an Autonomy project

Goal: get a project configured so the agent can build in it. You (the user's AI)
do this directly - you already hold the repo, its `.env`, and how it runs - so set
the config yourself rather than talking to a setup agent.

1. `list_projects` -> pick a project with a workspace, and pass its `project_id`
   to the setup tools. A gitless project (an empty `workspaces` list) has no code
   to set up yet.

   To connect a new repository: `list_available_projects` -> `add_projects` ->
   `initialize_project` with the repository's id -> poll `get_project` with that
   same id until its `status_data.status` is `READY` (poll `get_project`, not
   `list_projects`: the listing re-sends the whole org each call) ->
   `link_project_workspace` to put its workspace in a project (`create_project`
   first if none fits). Until that link, the repository's id is the `project_id`
   the setup tools take.

   If `get_project` returns `setup_bootstrap`, the project is on workspace-first
   setup and no workspace exists yet. A setup agent reads the repository and asks
   which workspace to set up: call `open_setup_chat` **without** `workspace_id`,
   read its card with `get_task_messages`, and answer it with
   `reply_setup_approval` (also without `workspace_id`). Once a workspace is
   chosen, its install, preview and configure steps run in that workspace's own
   setup chat (pass its `workspace_id`), and steps 2-4 below do not apply: the
   agent proves each command before it is saved.
2. `update_setup_config` -> set the project's commands:
   - `install_command` (e.g. `npm install`)
   - `validate_command` (e.g. `npx tsc --noEmit`)
   - optionally `dev_command` + `dev_url` (e.g. `npm run dev`, `http://localhost:5173`)
   - optionally `test_command` (e.g. `npx vitest run`) - the suite regression tests run
3. `list_env_vars` -> see which env the project needs (pending vs. stored), then
   `set_env_var` for each required value (read them from the local `.env`).
4. `get_setup_preview_status` -> confirm the dev server is live; share the preview URL.

If the user wants the *whole app* (not just components), load **full-mode.md**.
