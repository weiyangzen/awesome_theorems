# THM-M-0082 obligation-tree validation

Item: `S56-M-0082-OBLIGATION_TREE`. Base revision:
`f4aeafc83b9d0ab5a752188bd83124ddf69f5435`.

Validation ran from the worker clone on 2026-07-12. The existing pinned Lake
artifacts were reused; no dependency update, build, fetch, or clone was run.

```text
python3 Stage1_Instances/THM-M-0082/build_obligation_artifacts.py
  exit 0
  769e9ea30a88f4aee8aba874a58059ebaffc194822e5c62f1fe79866822892a9

python3 Stage1_Instances/THM-M-0082/check_obligation_tree.py
  exit 0
  PASS THM-M-0082 obligation tree: 13 obligations, 39 typed edges
  registry denominator sha256: 769e9ea30a88f4aee8aba874a58059ebaffc194822e5c62f1fe79866822892a9
  root closure: open (M3); exact central bridge remains M4

cd Formalizations/Lean &&
  lake env lean -o ../../Stage1_Instances/THM-M-0082/Statement.olean \
    ../../Stage1_Instances/THM-M-0082/Statement.lean
  exit 1
  The Lean 4.29.0 package-root check rejected an output module outside
  Formalizations/Lean. No dependency artifact was changed.

cd Formalizations/Lean &&
  lake env lean -R ../.. \
    -o ../../Stage1_Instances/THM-M-0082/Statement.olean \
    ../../Stage1_Instances/THM-M-0082/Statement.lean &&
  LEAN_PATH=../..:$LEAN_PATH lake env lean -R ../.. \
    ../../Stage1_Instances/THM-M-0082/ObligationTree.lean
  exit 0
  Exact statement and conditional bridge-to-root composition elaborated.
  Lean reported [propext, Classical.choice, Quot.sound]. The temporary local
  Statement.olean was removed after the check.

python3 Docs/tools/check_stage1_standard.py
  exit 0
  ok: 15 assurance groups and 1546 uniform-L0 Lean 4 targets

python3 scripts/stage1_target.py check
  exit 0
  1546 unique targets, ranks 1..1546, all L0/rework_required

git diff --check -- Stage1_Instances/THM-M-0082
  exit 0; no output
```

The successful Lean retry supplies the repository root explicitly with `-R`
while retaining the pinned Lake environment. Structural validation binds the
registry to the exact statement and anchor-audit hashes, recomputes the frozen
denominator, checks all required node fields and structured ledgers, checks
typed adjacency and reciprocal proof/composition edges, and confirms the
fail-closed root cut.

The central bridge, its expanded construction and lemma obligations, the
pinpoint human-source map, and release trust/provenance overlays remain open.
There is no accepted receipt and no theorem-completion claim; master acceptance
is still required for this phase.
