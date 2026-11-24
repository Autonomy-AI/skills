# Enable Full Mode

Full Mode runs the project's whole front end in Autonomy while proxying its API
calls to the project's existing **staging backend** - so the user can traverse
and edit the entire live app without Autonomy running the backend.

1. Ensure setup basics are done (load **setup.md** first if not).
2. `list_preview_targets` -> find the target that serves the app (its command +
   URL) and its `target_id`. If setup did not save it, ask the setup chat
   (`open_setup_chat`) to add it.
3. `update_preview_proxy_config` on that target (`cors_hosts=[<staging API host>]`,
   `forwarded_origin=...`) -> points the app's API calls at the staging backend.
   This is the core of Full Mode.
   - Use `forwarded_origin="${PUBLIC_ORIGIN}"` if the app's auth (Clerk/NextAuth) needs it.
4. `update_setup_files(files=[{file_path: ".env", file_content: "..."}])`
   -> any env the front end needs (e.g. the staging API base URL).
5. Start a task; the agent starts that target, and `list_task_previews` returns
   its URL while it runs.
