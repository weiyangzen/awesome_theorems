#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"

exec timeout 900s bwrap \
  --clearenv \
  --ro-bind / / \
  --bind /tmp /tmp \
  --dev /dev \
  --proc /proc \
  --unshare-net \
  --die-with-parent \
  --new-session \
  --setenv LANG C.UTF-8 \
  --setenv LC_ALL C.UTF-8 \
  --setenv TZ UTC \
  --setenv LEAN_NUM_THREADS 1 \
  --setenv STAGE1_OUTER_SANDBOX 1 \
  --setenv HOME /home/sansha-2 \
  --setenv PATH /home/sansha-2/.elan/bin:/home/sansha-2/.local/bin:/usr/local/bin:/usr/bin:/bin \
  --chdir "$repo_root" \
  python3 -I -B Stage1_Instances/THM-M-1007/check_validation.py
