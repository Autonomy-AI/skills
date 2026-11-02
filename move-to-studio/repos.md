# Repos: link the person's repos to a Studio project

This part runs through the MCP tools.
The exact connect sequence is step 1 of the setup guide: `load_autonomy_skill(name='setup')` through the MCP, or **[../using-autonomy/setup.md](../using-autonomy/setup.md)** with the plugin installed. Follow it there rather than from memory.

Most of these tools need an **org admin**: `list_available_projects`, `add_projects`, `initialize_project` and `link_project_repo`.
If the person is not an admin, make the list of what to link, and hand it to them for an admin.

## Steps

1. Take the repos `inventory.py` listed (most used first) and ask the person which ones matter to them. With no shell, ask them to name their repos (`owner/name`).
2. `list_available_projects` (admin) shows every repository the org's Git connection can see, and whether it is already in the org's active set (`is_linked`). The ids it shows are repository ids. A repo that is missing entirely was never granted to Autonomy: the org admin adds it in the Git provider's app settings first.
3. **Not in the active set yet:** adding a repo (`add_projects`, with those repository ids) and initializing it (`initialize_project`) are org-wide and start Studio's setup for that repo. Do them only if the person is an admin and agrees. Poll `get_project` with the repository's id until `status_data.status` is `READY`.
4. **Ready:** put each repo the person picked on their project with `link_project_repo(project_id, repo_id)`, following setup.md. If they have no project yet, `create_project` makes one, but a project can't be deleted afterwards: confirm the exact name with the person first.
5. **Several repos:** a project links any number of repositories. The first one linked is the primary, where new tasks start; `set_primary_repo(project_id, repo_id)` changes it. Link the others to the same project, unless the person wants a separate project per repo (same name confirmation). Never `unlink_project_repo` a repo that is already linked to make room; it detaches that repo from the project.
6. A repo still initializing: you can link it anyway, because tasks can edit its code before it is set up. Install, checks and previews arrive once initialization finishes; tell the person to watch `get_project` for `READY`.

Linking a repo is only the connection.
Install, preview and env setup are the rest of setup.md, and the person can run them later with "set up my project".
