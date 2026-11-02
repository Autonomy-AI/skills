# Troubleshooting

- **401 / authentication failed** -> the session/token expired; re-authenticate
  the `autonomy` server in the MCP client.
- **410 Gone** -> the call names a removed tool or a replaced id; re-read
  `get_project` for current ids.
- **403 on preview-config** -> the `project_cors_proxy` (Full Mode) flag is not
  enabled for this project.
- **Setup not progressing** -> `get_project` for the setup status;
  `list_env_vars` to spot unset required env vars, then `set_env_var` to fill them.
- **Repository not READY** -> a just-connected repository is
  `PENDING_INITIALIZATION`; call `initialize_project` with its id and poll
  `get_project` with the same id (cheaper than re-listing the org). If it failed,
  `rerun_initialization`. `link_project_repo` puts it in a project at any time.
- **No preview is running** -> the agent starts previews when it needs them;
  `list_task_previews` shows what runs. Ask it in the task to show one.
- **Tasks start from stale dependencies** -> `get_template_refresh_status` first: it
  reports whether refreshing auto-disabled after repeated failures, and
  `retry_template_refresh` clears that flag (fix the root cause first, or it
  re-disables). If refreshing is enabled but never runs,
  `get_effective_refresh_policy` shows what's in force after the repo ->
  project -> org cascade. Admin-only.
- **Task seems stuck** -> tasks run in the background; keep polling `get_task`.
  If it's going the wrong way, `stop_task` then `continue_task` with new guidance.
