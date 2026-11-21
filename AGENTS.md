# sandbox-os — instructions for agents

sandbox-os is the pilot project of the Personal AI Manager: a minimal FastAPI service on which
the controlled delivery loop is exercised. Work here arrives as a Linear issue (team COS, project
"sandbox-os") and leaves as a pull request. The rules for every worker are in the hub at
`~/Projects/companion-os/personal-ai-manager/agents/worker-charter.md`; the role is named in your
first message. This file adds what is specific to this repository.

## Layout

| Path | What |
|---|---|
| `main.py` | The FastAPI app and its endpoints; an in-memory store |
| `models.py` | Pydantic models |
| `tests/` | Tests, run with pytest (create it if your issue adds the first test) |
| `requirements.txt` | Runtime dependencies (a risk-trigger path) |
| `requirements-dev.txt` | Test dependencies (a risk-trigger path) |

## Environment

One shared virtual environment, created by the user, lives in the main checkout and is used from
every worktree by its absolute path. Do not create or change it, and do not `pip install`; a
dependency an issue needs is a question for the Manager.

```bash
PY=/home/sesq/Projects/companion-os/sandbox-os/.venv/bin/python
```

## Build and test

Run from the root of your worktree:

```bash
/home/sesq/Projects/companion-os/sandbox-os/.venv/bin/python -m py_compile main.py models.py
/home/sesq/Projects/companion-os/sandbox-os/.venv/bin/python -m pytest -q
```

pytest exits with code 5 when there are no tests yet; say so in the report rather than calling
it a pass.

A reviewer runs the same tests without writing to the implementor's worktree:

```bash
cd <worktree> && PYTHONDONTWRITEBYTECODE=1 /home/sesq/Projects/companion-os/sandbox-os/.venv/bin/python -m pytest -q -p no:cacheprovider
```

Tests use FastAPI's `TestClient` (`from fastapi.testclient import TestClient`) against
`main.app`. The store is module state: reset `main._items` and `main._next_id` in a fixture.

## Git and GitHub

- Repository: `nypro-wa/sandbox-os` (public). Default branch: `main`, protected by a ruleset:
  changes only through a pull request with an approving review by someone other than the author.
  The user merges.
- You push as the agent account. The credential helper for `github.com` in this repository's
  git config does that; never add or change credentials.
- Branch: the one in your spec, `agent/<issue-id-lowercase>-<slug>`. Commit messages:
  `<ISSUE-ID>: <what>`.
- Push: `git push -u origin HEAD:<branch from your spec>`. Orca prefixes your local branch with
  `nypro-wa/`; the explicit target keeps the planned name on GitHub. Never push to `main`, never
  force-push.
- Open the pull request, from the root of your worktree:

  ```bash
  GH_CONFIG_DIR=$HOME/.config/gh-agent gh pr create --repo nypro-wa/sandbox-os --base main --title "<ISSUE-ID>: <title>" --body-file <file>
  ```

  The body follows `.github/pull_request_template.md`. Write the body file inside your worktree
  under `.git-pr-body.md` (ignored), not in `/tmp`.
- Update it on a repair round, as one plain command, with
  `GH_CONFIG_DIR=$HOME/.config/gh-agent gh api -X PATCH repos/nypro-wa/sandbox-os/pulls/<n> -F body=@.git-pr-body.md`.
  Not `gh pr edit`: it fails on this repository with a Projects-classic GraphQL error.

## Linear

Through the Orca CLI, each as one plain command (no pipes, `&&`, `;` or `$(…)`):

```bash
~/.config/orca/linux-orca-cli-shim/orca linear issue <ISSUE-ID> --comments --json
~/.config/orca/linux-orca-cli-shim/orca linear status set <ISSUE-ID> --to "In Progress"
~/.config/orca/linux-orca-cli-shim/orca linear status set <ISSUE-ID> --to "In Review"
~/.config/orca/linux-orca-cli-shim/orca linear comment add <ISSUE-ID> --body "<text>"
~/.config/orca/linux-orca-cli-shim/orca linear label add <ISSUE-ID> --label Blocked
```

## Risk triggers added by this project

On top of the fixed list in the hub's `protocols/approval-policy.md` (never fewer):

| Trigger | Paths | Keywords |
|---|---|---|
| Data deletion in the store | `main.py` | `del _items`, `_items.clear`, `_items.pop` |
| Endpoint removed or renamed | `main.py` | `@app.delete`, a removed `@app.` line |

## Protected files

`AGENTS.md`, `CLAUDE.md` and `.claude/` are changed only by a builder of the Personal AI Manager,
not through an issue. Editing them is refused by `.claude/settings.json`.
