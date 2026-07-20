# Troubleshooting

- **401 / authentication failed** -> the session/token expired; re-authenticate
  the `autonomy` server in the MCP client.
- **410 / stale workspace** -> the `workspace_id` no longer exists; re-run
  `list_projects` to get a current one.
- **403 on preview-config** -> the `project_cors_proxy` (Full Mode) flag is not
  enabled for this project.
- **Setup not progressing** -> `get_setup_preview_status` for dev-server state;
  `list_env_vars` to spot unset required env vars, then `set_env_var` to fill them.
- **Project not READY** -> a just-connected repo is `PENDING_INITIALIZATION`; call
  `initialize_project` and poll `list_projects`. If it failed, `rerun_initialization`.
- **Task seems stuck** -> tasks run in the background; keep polling `get_task`.
  If it's going the wrong way, `stop_task` then `continue_task` with new guidance.
