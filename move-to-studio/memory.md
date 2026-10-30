# Memory: import auto-memory and personal instructions

Studio has two kinds of memory.
**Personal memory** follows the person and holds their preferences, feedback on how to work with them, and their own ongoing work. Only they see it. It holds 30 entries per scope (global, and one per workspace), where the organization has it turned on.
**Workspace memory** belongs to a repo's workspace and is shared with everyone on it: facts about the codebase or tools. It holds 200 entries for the whole workspace.

You sort the memories with the person, then write each one with the MCP tools.

## Steps

1. Stage and scan: `bash <skill_dir>/scripts/pack.sh memory <repo_dir> <out_dir>`.
   It copies the Claude Code auto-memory for `<repo_dir>` into `<out_dir>/memory/` and, if present, the person's global `~/.claude/CLAUDE.md` as `GLOBAL-CLAUDE.md`.
   The scan prints each suspect as `SECRET? <file>:<line>` (relative to `<out_dir>/memory/`), without the value. Open that line yourself, show the person which entry it is (not the value), and have them say whether it is a real secret.
   - A real secret: leave that memory out. Delete its file from `<out_dir>/memory/` and its line from the staged `MEMORY.md` - the staged copy, never the person's own memory folder - then `bash <skill_dir>/scripts/pack.sh scan <out_dir>/memory` until it prints no `SECRET?` line.
   - A false positive: keep it, and say so in the plan.
   For another tool's memory or rules (for example Cursor's user rules), ask the person to save them as Markdown files in a folder and stage that with `pack.sh docs`.
2. Pick the project to import into (the one from the plan). Workspace memory needs a project with a linked repository (`get_project` lists its workspace), and it should be the repository the memories are about. Note that `workspace_id`; the memory tools below need it. If the local memory is about a repo that isn't in Studio yet, hold its repo facts until that repo is linked: saved on a different repo, they would tell its agents the wrong thing.
3. Check room: `list_personal_memories(project_id, bind_to_workspace=false)` and `(…, bind_to_workspace=true, workspace_id)` for what the person already has, and `get_memory_usage(project_id, workspace_id)` for how full the shared workspace memory is. A large import can fill workspace memory for everyone on the repo, so say how full it is. The usage total counts every scope, including each agent's own doc, so it can be higher than what `list_workspace_memories` shows for the shared scope.
4. Read every staged file (`MEMORY.md` is the index; each other file is one memory) and sort each into a plan, one line per memory:
   - **personal, global**: the person's preferences, feedback on how to work with them, their ongoing projects. `GLOBAL-CLAUDE.md` belongs here.
   - **personal, this repo**: the same, but only about this repository.
   - **workspace**: facts about the codebase or tools that would help anyone on it. Skip what the repo's own CLAUDE.md or rules already say.
   - **drop**: stale experiment notes, one-off session state, anything tied to a temporary environment or a date that has passed.
   Merge related ones so each personal scope stays within 30. Keep each memory's wording and its Why / How to apply lines. Memories that point at local paths (`~/.claude/...`, scratch folders) lose that pointer in Studio: keep the finding, drop the path.
5. Show the plan and wait for the person's go. **Don't approve it for them.**
6. Write what they approved:
   - Personal: `save_personal_memory(project_id, key, value, description, bind_to_workspace, category, workspace_id)` (`workspace_id` only with `bind_to_workspace=true`). If it says personal memory is not turned on, tell the person; those memories have nowhere to go yet.
   - Workspace: `save_workspace_memory(project_id, workspace_id, key, value, description, category)`. It needs an admin. Not an admin: use the task route below for the workspace memories.
   - A refusal names the reason (a credential, over 100 lines, a full scope): fix that entry and save it again.
7. Confirm with `list_personal_memories` and `list_workspace_memories`.

## No shell

Claude Desktop and claude.ai keep memory and project instructions in the person's account, not in files you can read.
1. Ask the person to paste what they want carried over, one piece at a time: what Claude remembers about them (asking "what do you remember about me?" in a chat shows it), a project's instructions, a rules file. Never ask for a secret; tell them to leave out any line with a password or key.
2. Take what you can already see too: memory or instructions in your own context are the person's, so offer them.
3. Then steps 2 to 7 above, with each pasted piece as a staged file. The save tools refuse a credential by line, so a missed one is stopped before it is stored.

## Task route (not an admin, or no MCP memory tools)

A Studio task can write both kinds of memory for any member.
Upload the zip `pack.sh` made: when it says the zip is small enough, `upload_reference_file(project_id, file_base64, filename="memory.zip", extract=true)`; otherwise ask the person to attach `memory.zip` in Studio's composer.
Then `start_task(project_id, instruction, workspace_id=<workspace_id>, initial_step="planner", reference_files=[<descriptor>])`, so the agent shows a plan before writing anything, with this instruction:

> Import my memory from the attached zip. MEMORY.md is the index and every other file is one memory; GLOBAL-CLAUDE.md, if present, holds my personal instructions. Sort each item: personal memory for my preferences, feedback on how to work with me, and my own ongoing projects (30 entries per scope, so merge related ones and keep the strongest 30); workspace memory for facts about the codebase or tools that would help anyone on this repo, skipping what the repo's CLAUDE.md or rules already say; drop stale experiment notes, one-off session state, and anything tied to a temporary environment or a date that has passed. Keep each memory's wording and its Why / How to apply lines. Show me the plan (memory → tier) before you write anything, and write only after I say go.

Poll `get_task` and read `get_task_messages` until the plan arrives, show it to the person, and relay their answer with `answer_task_question` or `continue_task`.
Give them `get_task_studio_url` if they want to watch it in Studio.
