# Troubleshooting

- **401 / authentication failed** -> the session/token expired; re-authenticate
  the `autonomy` server in the MCP client.
- **410 / stale workspace** -> the `workspace_id` no longer exists; re-read
  `get_project` to get a current one.
- **403 on preview-config** -> the `project_cors_proxy` (Full Mode) flag is not
  enabled for this project.
- **Setup not progressing** -> `get_setup_preview_status` for dev-server state;
  `list_env_vars` to spot unset required env vars, then `set_env_var` to fill them.
- **Repository not READY** -> a just-connected repository is
  `PENDING_INITIALIZATION`; call `initialize_project` with its id and poll
  `get_project` with the same id (cheaper than re-listing the org). If it failed,
  `rerun_initialization`. Once `READY`, `link_project_workspace` puts it in a project.
- **start_task asks for a workspace_id** -> the project's workspace is hidden from
  you or inactive, so `list_projects` shows none. An admin makes it visible, or
  unlinks it in Studio and links a READY one with `link_project_workspace`.
- **Tasks start from stale dependencies** -> `get_template_refresh_status` first: it
  reports whether refreshing auto-disabled after repeated failures, and
  `retry_template_refresh` clears that flag (fix the root cause first, or it
  re-disables). If refreshing is enabled but never runs,
  `get_effective_refresh_policy` shows what's in force after the workspace ->
  project -> org cascade. Admin-only.
- **Task seems stuck** -> tasks run in the background; keep polling `get_task`.
  If it's going the wrong way, `stop_task` then `continue_task` with new guidance.
