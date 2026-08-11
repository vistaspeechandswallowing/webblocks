# Working in this repo

## Default change workflow

Changes are developed on a feature branch and landed on `main` via a pull
request — never pushed straight to `main`. This keeps a reviewable diff and a
checkpoint for every change.

For automated (Claude) changes, the full round-trip happens without the owner
needing to touch GitHub:

1. Commit the change on the working feature branch and push it.
2. Open a pull request into `main`.
3. Merge the PR.
4. **Verify the change is actually present in `main`** (check the file content
   on `main`, not just that the merge returned success) before reporting done.

Step 4 matters: a PR can merge a moment before the final push lands, which
silently leaves the newest commit out of `main`. Always confirm the content.

## Hold for review

To review a change before it reaches `main`, ask to **"hold the merge"** — the
PR is left open so the diff can be read first, and merged only on the go-ahead.
