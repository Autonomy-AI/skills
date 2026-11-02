# Set up an Autonomy project

Goal: get a project configured so the agent can build in it. You (the user's AI)
do this directly - you already hold the repo, its `.env`, and how it runs - so set
the config yourself rather than talking to a setup agent.

1. `list_projects` -> pick a project with a linked repository, and pass its
   `project_id` to the setup tools. A gitless project (no repository) has no code
   to set up yet.

   To connect a new repository: `list_available_projects` -> `add_projects` ->
   `initialize_project` with the repository's id -> poll `get_project` with that
   same id until its `status_data.status` is `READY` (poll `get_project`, not
   `list_projects`: the listing re-sends the whole org each call) ->
   `link_project_repo` to put it in a project (`create_project` first if none
   fits). Until that link, the repository's id is the `project_id` the setup
   tools take.

   Initialization opens a setup chat: an agent reads the repository, proves the
   install and validate commands, and saves every preview target it finds. Read
   its cards with `get_task_messages` and answer them with
   `reply_setup_approval`. Steps 2-4 below are for setting things yourself.
2. `update_setup_config` -> set the repository's commands:
   - `install_command` (e.g. `npm install`)
   - `validate_command` (e.g. `npx tsc --noEmit`) - READY needs it to run to the
     end; type errors already in the code are fine
   - optionally `test_command` (e.g. `npx vitest run`) - the suite regression tests run
3. `list_env_vars` -> see which env the repository needs (pending vs. stored), then
   `set_env_var` for each required value (read them from the local `.env`).
4. `list_preview_targets` -> the ways to look at the repository running (e.g. `web`,
   `pnpm dev`, `http://localhost:5173/`); a Storybook is just another target. The
   setup chat saves them, and tasks start them when they need them.

If the user wants the *whole app* (not just components), load **full-mode.md**.
