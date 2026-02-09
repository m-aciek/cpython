# Trigger Docs Offline Build Workflow

## Overview

This workflow (`trigger-docs-offline.yml`) automatically triggers the python-docs-offline repository's build workflow when documentation changes are pushed to the CPython repository.

## Workflow Trigger Conditions

The workflow runs when:
- A commit is pushed to `main` or any `3.*` branch (e.g., `3.13`, `3.12`, etc.)
- The commit modifies any files under the `Doc/` directory

## How It Works

1. When the trigger conditions are met, the workflow sends a `repository_dispatch` event to the `m-aciek/python-docs-offline` repository
2. The event includes:
   - `event_type`: `cpython_docs_updated`
   - `branch`: The branch name where the commit was pushed
   - `repository`: The full repository name (e.g., `m-aciek/cpython`)
   - `sha`: The commit SHA
   - `commit_message`: The commit message

## Required Configuration

### 1. Personal Access Token (PAT)

This workflow requires a Personal Access Token with appropriate permissions to trigger workflows in the target repository.

**Steps to set up:**

1. Create a GitHub Personal Access Token with the following scopes:
   - `repo` (Full control of private repositories) OR
   - `public_repo` (Access public repositories) if both repos are public
   - The token needs permission to trigger workflows in the `m-aciek/python-docs-offline` repository

2. Add the token as a repository secret:
   - Go to the CPython repository settings
   - Navigate to Secrets and variables → Actions
   - Create a new repository secret named `DOCS_OFFLINE_TRIGGER_TOKEN`
   - Paste the Personal Access Token as the value

### 2. Target Repository Configuration

The `m-aciek/python-docs-offline` repository's `build.yaml` workflow needs to be updated to accept `repository_dispatch` events.

Add the following to the `on:` section of `.github/workflows/build.yaml`:

```yaml
on:
  workflow_dispatch:
    # ... existing workflow_dispatch configuration ...
  repository_dispatch:
    types: [cpython_docs_updated]
```

Then, update the workflow to use the branch from the client payload:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # ... other steps ...
      - uses: actions/checkout@v6
        with:
          repository: python/cpython
          ref: ${{ github.event.client_payload.branch || github.event.inputs.tag }}
      # ... remaining steps ...
```

## Testing

To test this workflow without making changes to documentation:

1. You can manually trigger workflows using the GitHub API
2. Or make a small change to a file in the `Doc/` directory on a test branch
3. Push to `main` or a `3.*` branch to see the workflow trigger

## Troubleshooting

- **Workflow doesn't trigger**: Ensure the `DOCS_OFFLINE_TRIGGER_TOKEN` secret is properly configured
- **403 Forbidden errors**: The PAT may not have sufficient permissions or may have expired
- **Target workflow doesn't run**: Verify the target repository has added `repository_dispatch` trigger support
