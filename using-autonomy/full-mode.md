# Enable Full Mode

Full Mode runs the project's whole front end in Autonomy while proxying its API
calls to the project's existing **staging backend** - so the user can traverse
and edit the entire live app without Autonomy running the backend.

1. Ensure setup basics are done (load **setup.md** first if not).
2. `update_setup_config(dev_command, dev_url)` -> the command + URL that serve the app.
3. `update_preview_proxy_config(cors_hosts=[<staging API host>], forwarded_origin=...)`
   -> points the app's API calls at the staging backend. This is the core of Full Mode.
   - Use `forwarded_origin="${PUBLIC_ORIGIN}"` if the app's auth (Clerk/NextAuth) needs it.
4. `update_setup_files(files=[{file_path: ".env", file_content: "..."}])`
   -> any env the front end needs (e.g. the staging API base URL).
5. `get_setup_preview_status` -> returns the live preview URL of the whole app.

Note: Full Mode is feature-flagged (the `project_cors_proxy` flag). If a call is
rejected with `403`, the project may not have Full Mode enabled.
