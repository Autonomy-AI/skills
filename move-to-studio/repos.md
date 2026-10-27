# Repos: link the person's repos to a Studio project

This part runs through the MCP tools.
The exact connect sequence lives in **[../using-autonomy/setup.md](../using-autonomy/setup.md)**, step 1; follow it there rather than from memory.

Most of these tools need an **org admin**: `list_available_projects`, `add_projects`, `initialize_project` and `link_project_workspace`.
If the person is not an admin, make the list of what to link, and hand it to them for an admin.

## Steps

1. Take the repos `inventory.py` listed (most used first) and ask the person which ones matter to them.
2. `list_available_projects` (admin) shows every repo the org's Git connection can see and whether it is already linked. A repo that is missing entirely was never granted to Autonomy: the org admin adds it in the Git provider's app settings first.
3. **Not linked yet:** adding a repo (`add_projects`) and initializing it (`initialize_project`) are org-wide and start Studio's setup for that repo. Do them only if the person is an admin and agrees.
4. **Ready:** put the main repo on the person's project with `link_project_workspace`, following setup.md. If they have no project yet, `create_project` makes one, but a project can't be deleted afterwards: confirm the exact name with the person first.
5. **Each other repo:** a project links one repo today. Give each other repo its own project, named after the repo (same confirmation), and never replace the main repo to make room. Where Studio allows several repos on one project, it says so in the project's settings; use that instead.
6. A repo still initializing: leave it, and tell the person to link it once `get_project` shows it ready.

Linking a repo is only the connection.
Install, preview and env setup are the rest of setup.md, and the person can run them later with "set up my project".
