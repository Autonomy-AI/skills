# Memory: import auto-memory and personal instructions

Studio has two kinds of memory.
**Personal memory** follows the person and holds their preferences, feedback on how to work with them, and their own ongoing work. It holds 30 entries per scope, and is available where the organization has it turned on.
**Workspace memory** belongs to a repo and is shared with everyone on it: facts about the codebase or tools. It holds 200 entries for the whole workspace, shared by everyone.
The import merges and trims to fit.

A Studio task does the sorting, because it can write both kinds.
This part runs through the MCP tools.

## Steps

1. Pack and scan: `bash <skill_dir>/scripts/pack.sh memory <repo_dir> <out_dir>`.
   It zips the Claude Code auto-memory for `<repo_dir>` and, if present, the person's global `~/.claude/CLAUDE.md` as `GLOBAL-CLAUDE.md`.
   The scan prints each suspect as `SECRET? <file>:<line>`, without the value. `pack.sh` deletes its copy when it exits, so `<file>` is relative to the `memory_dir` that `pack.sh inventory` printed, and `GLOBAL-CLAUDE.md` is `~/.claude/CLAUDE.md`. Open that line in the real file yourself, show the person which entry it is (not the value), and have them remove it or confirm it is a false positive before anything is uploaded. Re-run until clean.
   For another tool's memory or rules (for example Cursor's user rules), ask the person to save them as Markdown files in a folder, then zip and scan that folder with `pack.sh docs`.
2. Pick a repo-backed project to import into (the one from the plan): one whose `list_projects` entry has a workspace. Note its `workspace_id`; the memory tools below need it. A project with no repo has no workspace memory, so import there only if the person wants personal memory alone.
3. Check room first: `get_memory_usage(project_id, workspace_id)`. Workspace memory is shared, and a large import can fill it to the cap for everyone on the repo. Tell the person how full it is.
4. Get the zip to Studio. `pack.sh` prints which way fits:
   - **Small zip** (it prints the `base64` command): `upload_reference_file(project_id, file_base64, filename="memory.zip", extract=true)`, and keep the descriptor it returns.
   - **Larger zip**: sending it through the model costs too much. Ask the person to open Studio, start a task in the project, and attach `memory.zip` in the composer before pasting the instruction below.
5. Start the import as a planning task, so nothing is written before the person approves: `start_task(project_id, instruction, workspace_id=<workspace_id>, initial_step="planner", reference_files=[<descriptor from step 4>])` with this instruction:
   > Import my memory from the attached zip. MEMORY.md is the index and every other file is one memory; GLOBAL-CLAUDE.md, if present, holds my personal instructions. Sort each item: personal memory for my preferences, feedback on how to work with me, and my own ongoing projects (30 entries per scope, so merge related ones and keep the strongest 30); workspace memory for facts about the codebase or tools that would help anyone on this repo, skipping what the repo's CLAUDE.md or rules already say; drop stale experiment notes, one-off session state, and anything tied to a temporary environment or a date that has passed. Keep each memory's wording and its Why / How to apply lines. Show me the plan (memory → tier) before you write anything, and write only after I say go.
6. Poll `get_task` and read `get_task_messages` until the plan arrives (a few minutes for ~40 memories).
7. Show the plan to the person and relay their answer with `answer_task_question` (when the plan arrives as a question card) or `continue_task`. **Don't approve it for them.**
8. When the task finishes, confirm with `list_workspace_memories(project_id, workspace_id)`, and point the person at their personal memory in Studio.

## What to expect

- Memories that point at local paths (`~/.claude/...`, scratch folders) lose that pointer in Studio. Keep the finding, drop the path.
- The agent dedupes against the repo's own CLAUDE.md and rules by itself.
- Give the person `get_task_studio_url` so they can watch the task in Studio if they want.
