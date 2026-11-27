# Voyage – rules for AI assistants

## 🚨 GOLDEN RULE: DO NOT MAKE GIT ACTIONS YOURSELF

**Never run any git command that changes the repository.** This includes `git add`, `git commit`, `git push`, `git pull`, `git merge`, `git rebase`, `git checkout -b`, `git switch -c`, `git branch`, `git stash`, `git reset`, `git tag`, and creating or merging pull requests (`gh pr ...`).

Instead, when work is ready, **tell the team**:

- the **branch name** to create, and
- the **commit message** to use.

The team runs the git commands themselves.

Read-only commands such as `git status`, `git diff` and `git log` are allowed.

### Naming conventions to suggest

- Branches: `<type>/<short-description>`, for example `feature/onboarding-questionnaire`, `fix/map-marker-sync`, `chore/project-setup`
- Commits: [Conventional Commits](https://www.conventionalcommits.org/), for example `feat: add destination ranking endpoint`
- Types: `feat`, `fix`, `chore`, `docs`, `test`, `refactor`, `style`, `ci`

## Project notes

- Setup: `python setup.py` (see README.md). Python dependencies are pinned in `requirements.txt`. Frontend dependencies are in `frontend/package-lock.json`.
- Never commit `.env` files or put secret keys in `NEXT_PUBLIC_*` variables.
- The technical specification (`Voyage_Technical_Specification_v1.0.md`) is git-ignored and shared outside the repo.
