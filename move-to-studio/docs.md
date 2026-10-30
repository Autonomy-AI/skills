# Docs: bring a folder of docs into a Space

A Space holds pages: Markdown, HTML and images, in folders.
The project Space (`project/…`) is shared with everyone on the project; the personal Space (`user/…`, "Mine" in Studio) is the person's own, where it is turned on.
You write the pages yourself with `write_space_page`, so nothing is rewritten on the way.

## Steps

1. Ask which folder or repo to bring over (a notes folder, a docs repo, a personal pages site), and whether it is for the team (project Space) or just for them (personal Space).
2. Stage and scan: `bash <skill_dir>/scripts/pack.sh docs <dir or owner/repo> <out_dir>`.
   It copies only documents and images into `<out_dir>/docs/`, and never `.git`, `.env*`, keys, credentials or `*-private*` files.
   Clear every `SECRET?` line with the person (open the line yourself; never repeat the value). For a real secret, delete that file from `<out_dir>/docs/`, then `bash <skill_dir>/scripts/pack.sh scan <out_dir>/docs` until no `SECRET?` line prints; that also rebuilds `docs.zip`. Paths in `SECRET?` lines are relative to the staged folder.
   PDFs and images are not scanned, so ask the person to confirm none of them holds a secret.
3. Pick one folder for the import, named after the source, for example `project/handbook/` or `user/notes/`. Pages can't sit at a tier's root.
4. For each staged text file (`.md`, `.mdx`, `.html`, `.txt`), `write_space_page(project_id, path=<folder>/<its path in docs/>, content=<the file's text>)`. Keep the folder layout, so relative links between pages keep working.
   For each image or PDF, `upload_space_asset(project_id, path=<folder>/<its path>, file_base64, filename)`, but only small ones: a large file costs too much through the model, so list those for the person to upload in Studio.
   A refusal names the reason (a reserved file name, a full Space, over 1 MB): rename or split that file, and tell the person.
5. If the source has no home page, write one at `<folder>/README.md` that links to every page.
6. Check the result against the staged file list:
   - Project Space: `list_space_pages(project_id)`.
   - Personal Space: ask the person to check Spaces → **Mine** in Studio.

## No shell

Ask the person to attach the files to the chat, or paste each page.
Skip anything that is a key, credential or `.env` file, and ask them to leave those out.
Then steps 3 to 6 above, one `write_space_page` per file. A refusal that names a line means it holds a provider key, token or private key: tell the person which line, never the value, and save again with it taken out.
Images and PDFs are not scanned, so ask the person to confirm none of them holds a secret.

For a very large folder (hundreds of files), a task can do the copying instead: upload `docs.zip` (or have the person attach it in Studio's composer) and `start_task(project_id, instruction, initial_step="discover", reference_files=[<descriptor>])` with "Recreate every file in the attached zip as a page in my <project / personal> Space under <folder>, keeping the folder layout. Copy content exactly, without summarising or rewriting. Keep HTML pages as HTML. When done, list each page with its path and anything that didn't carry over."

Studio's Spaces view may not show folders, but the pages keep their paths.
