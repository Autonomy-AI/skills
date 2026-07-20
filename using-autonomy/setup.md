# Set up an Autonomy project

Goal: get a project configured so the agent can build in it. You (the user's AI)
do this directly - you already hold the repo, its `.env`, and how it runs - so set
the config yourself rather than talking to a setup agent.

1. `list_projects` -> pick a project. If its `status_data.status` isn't `READY`
   (e.g. a just-connected repo in `PENDING_INITIALIZATION`), call
   `initialize_project` and poll `list_projects` until it's `READY` - that's when
   it gets a `workspace_id`.
2. `update_setup_config` -> set the project's commands:
   - `install_command` (e.g. `npm install`)
   - `validate_command` (e.g. `npx tsc --noEmit`)
   - optionally `dev_command` + `dev_url` (e.g. `npm run dev`, `http://localhost:5173`)
3. `list_env_vars` -> see which env the project needs (pending vs. stored), then
   `set_env_var` for each required value (read them from the local `.env`).
4. `get_setup_preview_status` -> confirm the dev server is live; share the preview URL.

If the user wants the *whole app* (not just components), load **full-mode.md**.
