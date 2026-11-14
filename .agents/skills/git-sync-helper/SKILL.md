---
name: git-sync-helper
description: Guided Git synchronization assistant for this project. Use when the user asks to verificar se tem mudancas desde a ultima vez, atualizar do GitHub, trazer alteracoes da equipe, guiar ajustes, resolver conflitos, commitar, publicar, subir alteracoes, fazer push, or run the standard manual sync flow: check remote changes, help adjust local work, then push approved updates to origin/main.
---

# Git Sync Helper

## Overview

Use this skill to safely synchronize the current project with GitHub. The default behavior is a guided manual flow: check whether GitHub changed since the last local sync, bring those changes in when safe, help the user adjust local work, then publish the final result.

## Default Guided Flow

When the user invokes this skill without a narrower command, follow this sequence:

1. Run diagnostics and fetch the latest remote state.
2. Tell the user whether GitHub has new commits, local files changed, local commits are waiting to be pushed, or conflicts exist.
3. If GitHub has new commits and local work is clean, pull with `git pull --ff-only`.
4. If GitHub has new commits and local work is dirty, explain the affected local files and guide the user to commit first, stash with explicit permission, or resolve manually.
5. If conflicts appear, guide resolution file by file and stop before completing destructive or ambiguous choices.
6. After the user or Codex finishes the requested adjustments, inspect the diff, stage only intended files, commit, pull again if needed, and push.
7. End with the final branch status, commit hash, and whether the checkout is clean.

## Safety Rules

- Always run diagnostics before changing Git state, including before every pull and before every push.
- Never discard, reset, checkout over, clean, or delete user changes unless the user explicitly asks for that exact destructive action.
- Treat `.env`, virtual environments, temporary folders, and generated secrets as sensitive; verify `.gitignore` is protecting them before staging broad changes.
- If there are conflicts, identify and explain them before editing. Resolve only when the correct combined result is clear.
- Use `git pull --ff-only` when there are no local commits to merge. If a merge or rebase is needed, explain the situation before choosing.
- Stage only the files intended for the current commit. Avoid `git add .` when unrelated changes or sensitive files are present.
- Use concise commit messages in Portuguese or English matching the user's wording.

## Diagnostic Step

Start with:

```powershell
.\.agents\skills\git-sync-helper\scripts\git-sync-status.ps1
```

If the script is unavailable or fails, run the equivalent checks manually:

```powershell
git status --short --branch
git remote -v
git fetch --prune
git status --short --branch
git log --oneline --decorate --max-count=8
git diff --stat
git diff --cached --stat
```

Summarize:

- current branch and upstream
- whether local files are modified, staged, untracked, or conflicted
- whether the branch is ahead, behind, or diverged from `origin/main`
- incoming commits from GitHub and outgoing local commits, when present
- whether the next action is pull, local adjustment, commit, push, or conflict resolution

## Interpreting Changes Since Last Sync

Use the tracking branch as the source of truth:

- `Behind > 0`: GitHub has commits the local checkout has not received.
- `Ahead > 0`: local commits have not been pushed.
- `Ahead > 0` and `Behind > 0`: histories diverged; inspect before merge or rebase.
- Modified/untracked files: local file changes exist but are not committed yet.
- Conflicted files: a merge/rebase conflict is active and must be resolved before other sync steps.

When incoming commits exist, show their short log with:

```powershell
git log --oneline HEAD..@{u}
```

When outgoing commits exist, show:

```powershell
git log --oneline @{u}..HEAD
```

## Update From GitHub

When the user asks to update local files or "trazer o que a equipe fez":

1. Run diagnostics.
2. If there are unstaged local changes, avoid pulling until they are committed, stashed with explicit permission, or confirmed safe to merge.
3. Run `git pull --ff-only` if the branch is only behind.
4. If fast-forward fails because histories diverged, inspect commits with `git log --oneline --left-right --graph HEAD...@{u}` and explain the choice: merge, rebase, or manual conflict handling.
5. After pulling, run diagnostics again and summarize incoming commits and changed files when useful.

## Publish Local Changes

When the user asks to subir, publicar, or push changes after adjustments:

1. Run diagnostics and inspect the diff.
2. Explain the local files changed and ask for clarification only if unrelated changes make the commit scope unclear.
3. Confirm no sensitive files are staged.
4. Stage the intended files.
5. Commit if needed.
6. Run diagnostics again or `git fetch --prune`; if behind, pull safely before pushing.
7. Push with `git push`.
8. Finish by reporting the commit hash, branch, remote, and clean/dirty status.

## Suggested User Prompts

Recognize and execute these as the default guided flow:

```text
$git-sync-helper sincroniza esse projeto
$git-sync-helper ve se tem mudanca da equipe e atualiza
$git-sync-helper sobe meus ajustes
$git-sync-helper verifica, puxa o que tiver e depois sobe minhas mudancas
```

## Conflict Handling

When conflicts occur:

1. List conflicted files with `git diff --name-only --diff-filter=U`.
2. Open each conflicted file and understand both sides.
3. Resolve by preserving the user's local intent and remote teammate changes when possible.
4. Run targeted checks if available.
5. Stage resolved files and complete the merge/rebase only after verifying the result.
6. Explain what was kept from each side.

## User-Facing Style

Use plain language. The user wants a reliable "check, update, upload" assistant, not a Git lecture. Explain only the relevant Git concept when it affects the decision.
