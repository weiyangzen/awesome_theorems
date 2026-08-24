#!/bin/bash
set -euo pipefail
unset CDPATH

entrypoint_failure() {
  case "$1" in
    invalid_stage_timeout)
      printf '%s\n' '{"schema_version":"awesome-theorems-lean-entrypoint-diagnostic/1.0","status":"failed","diagnostics":[{"code":"invalid_stage_timeout","message":"M0387_STAGE_TIMEOUT_SECONDS must be a positive integer","action":"unset M0387_STAGE_TIMEOUT_SECONDS or set it to a positive integer number of seconds"}]}' >&2
      ;;
    missing_toolchain_file)
      printf '%s\n' '{"schema_version":"awesome-theorems-lean-entrypoint-diagnostic/1.0","status":"failed","diagnostics":[{"code":"missing_toolchain_file","message":"the tracked Formalizations/Lean/lean-toolchain file is unavailable","action":"restore the tracked lean-toolchain file before running validation"}]}' >&2
      ;;
    missing_python)
      printf '%s\n' '{"schema_version":"awesome-theorems-lean-entrypoint-diagnostic/1.0","status":"failed","diagnostics":[{"code":"missing_python","message":"python3 is unavailable on PATH","action":"install Python 3 and make python3 available on PATH for the preflight and dossier lint"}]}' >&2
      ;;
    missing_timeout)
      printf '%s\n' '{"schema_version":"awesome-theorems-lean-entrypoint-diagnostic/1.0","status":"failed","diagnostics":[{"code":"missing_timeout","message":"the timeout executable is unavailable on PATH","action":"install GNU coreutils timeout before running bounded validation stages"}]}' >&2
      ;;
    missing_elan)
      printf '%s\n' '{"schema_version":"awesome-theorems-lean-entrypoint-diagnostic/1.0","status":"failed","diagnostics":[{"code":"missing_elan","message":"the official elan executable is unavailable or not executable","action":"install official elan 4.2.3, put elan on PATH, or set ELAN_HOME to its installation root"}]}' >&2
      ;;
    *)
      printf '%s\n' '{"schema_version":"awesome-theorems-lean-entrypoint-diagnostic/1.0","status":"failed","diagnostics":[{"code":"unknown_entrypoint_failure","message":"the validation entrypoint failed before preflight","action":"inspect the entrypoint and restore its tracked bootstrap prerequisites"}]}' >&2
      ;;
  esac
  exit 1
}

stage_timeout_seconds="${M0387_STAGE_TIMEOUT_SECONDS:-7200}"
if [[ ! "$stage_timeout_seconds" =~ ^[1-9][0-9]*$ ]]; then
  entrypoint_failure invalid_stage_timeout
fi

run_started_epoch="$(date +%s)"
run_started_at="$(date --utc +%Y-%m-%dT%H:%M:%SZ)"
printf 'M0387_RUN_BEGIN|started_at=%s|stage_timeout_seconds=%s\n' \
  "$run_started_at" "$stage_timeout_seconds"

record_run_end() {
  local run_exit=$?
  local run_finished_epoch run_finished_at
  run_finished_epoch="$(date +%s)"
  run_finished_at="$(date --utc +%Y-%m-%dT%H:%M:%SZ)"
  printf 'M0387_RUN_END|finished_at=%s|exit_code=%s|wall_seconds=%s\n' \
    "$run_finished_at" "$run_exit" "$((run_finished_epoch - run_started_epoch))"
}
trap record_run_end EXIT

run_stage() {
  local stage="$1"
  local cwd="$2"
  local stage_started_epoch stage_started_at stage_finished_epoch stage_finished_at
  shift 2
  stage_started_epoch="$(date +%s)"
  stage_started_at="$(date --utc +%Y-%m-%dT%H:%M:%SZ)"
  printf 'M0387_STAGE_BEGIN|%s|started_at=%s|cwd=%s|timeout_seconds=%s\n' \
    "$stage" "$stage_started_at" "$cwd" "$stage_timeout_seconds"
  printf 'M0387_STAGE_ARGV|%s' "$stage"
  printf '|%q' "$@"
  printf '\n'
  if (
    cd -- "$cwd"
    timeout --signal=TERM --kill-after=30s "$stage_timeout_seconds" "$@"
  ); then
    local stage_exit=0
  else
    local stage_exit=$?
  fi
  stage_finished_epoch="$(date +%s)"
  stage_finished_at="$(date --utc +%Y-%m-%dT%H:%M:%SZ)"
  printf 'M0387_STAGE_END|%s|finished_at=%s|exit_code=%s|wall_seconds=%s\n' \
    "$stage" "$stage_finished_at" "$stage_exit" \
    "$((stage_finished_epoch - stage_started_epoch))"
  return "$stage_exit"
}

repo_root="$(cd -- "$(dirname -- "$0")/.." && pwd -P)"
lean_root="$repo_root/Formalizations/Lean"
if [[ ! -f "$lean_root/lean-toolchain" ]]; then
  entrypoint_failure missing_toolchain_file
fi
toolchain="$(tr -d '\r\n' < "$lean_root/lean-toolchain")"

if ! command -v python3 >/dev/null 2>&1; then
  entrypoint_failure missing_python
fi
if ! command -v timeout >/dev/null 2>&1; then
  entrypoint_failure missing_timeout
fi

# These variables can redirect elan/Lake away from the tracked toolchain or
# manifest.  The canonical entrypoint is intentionally invariant under them.
unset ELAN_TOOLCHAIN LAKE_OVERRIDE_LEAN LEAN LEAN_SYSROOT LEAN_PATH LAKE_PKG_URL_MAP

if [[ -n "${ELAN_HOME:-}" ]]; then
  elan="$ELAN_HOME/bin/elan"
else
  elan="$(command -v elan || true)"
fi

if [[ -z "$elan" || ! -x "$elan" ]]; then
  entrypoint_failure missing_elan
fi

echo "[preflight] verify the exact tracked Lean, Lake and Lake package revisions"
run_stage preflight "$repo_root" \
  python3 scripts/check_lean_environment.py --elan "$elan"

lake=("$elan" run "$toolchain" lake)

if [[ -n "${LAKE_NUM_JOBS:-}" ]]; then
  echo "[preflight] note: Lake 5 has no LAKE_NUM_JOBS scheduler control; value=$LAKE_NUM_JOBS is recorded as a non-enforcing caller hint"
fi

echo "[1/7] build node-scoped statement/reduction and branch modules"
run_stage build_branches "$lean_root" "${lake[@]}" build \
  +AwesomeTheorems.NumberTheory.THM_M_0387.StatementAndReductionPath \
  +AwesomeTheorems.NumberTheory.THM_M_0387.FLT4Path \
  +AwesomeTheorems.NumberTheory.THM_M_0387.FLT3Path \
  +AwesomeTheorems.NumberTheory.THM_M_0387.RegularPrimesPath \
  +AwesomeTheorems.NumberTheory.THM_M_0387.SmallExponentsPath \
  +AwesomeTheorems.NumberTheory.THM_M_0387.InternalCoveragePath \
  +AwesomeTheorems.NumberTheory.THM_M_0387.Sample

echo "[2/7] build the Stage1 integration wrapper"
run_stage build_stage1_wrapper "$lean_root" "${lake[@]}" build \
  +AwesomeTheorems.Stage1.S1_M_001

echo "[3/7] check theorem-folder sample"
run_stage check_sample "$lean_root" \
  "${lake[@]}" env lean ../../THM-M-0387/FermatLastTheorem_Sample.lean

echo "[4/7] build the shared AwesomeTheorems aggregator"
run_stage build_aggregator "$lean_root" "${lake[@]}" build +AwesomeTheorems

echo "[5/7] run the full local Lake build"
run_stage full_lake_build "$lean_root" "${lake[@]}" build

echo "[6/7] compile the rev-5.6 dossier lint"
run_stage compile_lint "$repo_root" \
  python3 -m py_compile scripts/lint_theorem_dossier.py

echo "[7/7] lint rev-5.6 tree, evidence, pins, public surfaces, and Lean probes"
run_stage dossier_lint "$repo_root" \
  python3 scripts/lint_theorem_dossier.py THM-M-0387
