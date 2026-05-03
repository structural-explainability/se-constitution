#!/usr/bin/env bash
# sync_upstream.sh
# Sparse-clones the data/contract/ folder from se-formal-contract
# into upstream/se-formal-contract/main/.
# Writes commit SHA to a temp file for the lockfile updater to consume.
#
# Usage: bash .github/scripts/sync_upstream.sh
# Runs from repo root.

set -euo pipefail

ORG="structural-explainability"
UPSTREAM_DIR="upstream"
COMMIT_TEMP=".github/scripts/_sync_commits.txt"

declare -A REPOS=(
  ["se-formal-contract"]="data/contract"
)

mkdir -p "$UPSTREAM_DIR"
rm -f "$COMMIT_TEMP"

for REPO in "${!REPOS[@]}"; do
  FOLDER="${REPOS[$REPO]}"
  TARGET="$UPSTREAM_DIR/$REPO/main"
  TMP_DIR=$(mktemp -d)

  echo "==> Syncing $REPO/$FOLDER"

  git clone \
    --filter=blob:none \
    --sparse \
    --depth=1 \
    --branch main \
    "https://github.com/$ORG/$REPO.git" \
    "$TMP_DIR"

  (cd "$TMP_DIR" && git sparse-checkout set "$FOLDER")

  COMMIT=$(cd "$TMP_DIR" && git rev-parse HEAD)
  echo "$REPO=$COMMIT" >> "$COMMIT_TEMP"

  rm -rf "$TARGET"
  mkdir -p "$TARGET"

  if [ -d "$TMP_DIR/$FOLDER" ]; then
    cp -r "$TMP_DIR/$FOLDER/." "$TARGET/"
    echo "    Synced $FOLDER/ -> $TARGET/"
  else
    echo "    WARNING: $FOLDER/ not found in $REPO — target left empty"
  fi

  rm -rf "$TMP_DIR"
done

echo "==> Sync complete. Commit SHA written to $COMMIT_TEMP"
