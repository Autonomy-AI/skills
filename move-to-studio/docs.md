# Docs: bring a folder of docs into a Space

A Space holds pages: Markdown, HTML and images, with folders.
A project's Space is shared with everyone on the project; a personal Space ("Mine") is the person's own, where it is turned on.
Pages are written by a Studio task, so this part runs through the MCP tools.

## Steps

1. Ask which folder or repo to bring over (a notes folder, a docs repo, a personal pages site), and whether it is for the team (project Space) or just for them (personal Space).
2. Pack and scan: `bash <skill_dir>/scripts/pack.sh docs <dir or owner/repo> <out_dir>`.
   It keeps only documents and images, and never packs `.git`, `.env*`, keys, credentials or `*-private*` files.
   Clear every `SECRET?` line with the person before uploading (open the line yourself; never repeat the value).
   PDFs and images are not scanned, so ask the person to confirm none of them holds a secret.
3. Get the zip to Studio. `pack.sh` prints which way fits:
   - **Small zip**: `upload_reference_file(project_id, file_base64, filename="docs.zip", extract=true)`, and keep the descriptor.
   - **Larger zip**: ask the person to start the task in Studio and attach `docs.zip` in the composer, with the instruction below.
4. Start it as a discover task, which writes into a Space without touching code: `start_task(project_id, instruction, initial_step="discover", reference_files=[<descriptor>])` with this instruction, naming the Space they picked:
   > Recreate every file in the attached zip as a page in my <project / personal> Space, keeping the folder layout. Copy content exactly, without summarising or rewriting. Keep HTML pages as HTML so they render as they do now. Build a home page that links to every page, and keep links between pages working. When done, list each page with its path and anything that didn't carry over cleanly.
5. Poll `get_task` until it finishes, then check the result against the zip's file list:
   - Project Space: `list_space_pages(project_id, workspace_id)`.
   - Personal Space: the MCP can't list it; ask the person to check Spaces → **Mine** in Studio, and use the task's own list of pages.

## What to expect

- Studio's Spaces view may not show folders, but the pages keep their paths.
- Pages can't sit at the very top level, so expect root files (`README.md` and the like) inside one folder.
