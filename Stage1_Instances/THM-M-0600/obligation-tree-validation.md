# THM-M-0600 obligation-tree validation

Item: `S56-M-0600-OBLIGATION_TREE`. Base revision:
`44b9849ef3fd618f97e63d42e60134771f7302b9`.

Validation ran in the worker automation clone on 2026-07-12. It reused the
existing pinned Lake dependency closure and did not update, fetch, clone, or
build dependencies.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0
  check_stage1_standard: ok (15 assurance groups, 41 legacy rows,
  300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)

python3 scripts/stage1_target.py check
  exit 0
  stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)

python3 scripts/stage1_target.py show THM-M-0600
  exit 0
  rank 638; planned; hard-statement-first lane; theorem_complete false

python3 Stage1_Instances/THM-M-0600/build_obligation_artifacts.py
  exit 0
  wrote 18 obligations and 44 typed edges
  071b084403b89cd9fb084d9fe7167cad1738e115f6353aaeabfab4516e93f981

python3 Stage1_Instances/THM-M-0600/check_obligation_tree.py
  exit 0
  PASS THM-M-0600 obligation tree: 18 obligations, 44 typed edges
  registry denominator sha256:
  071b084403b89cd9fb084d9fe7167cad1738e115f6353aaeabfab4516e93f981
  root closure: open (M3); the Morse normal-form engine remains M4

python3 -m json.tool Stage1_Instances/THM-M-0600/obligation-registry.json
python3 -m json.tool Stage1_Instances/THM-M-0600/typed-graphs.json
python3 -m json.tool Stage1_Instances/THM-M-0600/validation-specs.json
  exit 0 for all three files; valid JSON

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_DEPS=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0600
LEAN_PATH="$LEAN_DEPS" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_DEPS" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  root_of_morseNormalFormEngine depends on
  [propext, Classical.choice, Quot.sound]

rg -n -i '\b(sorry|admit|sorryAx)\b|^\s*axiom\b' \
  Stage1_Instances/THM-M-0600/Statement.lean \
  Stage1_Instances/THM-M-0600/ObligationTree.lean
  exit 1 as expected; no prohibited token matched
```

The first Lean attempt exited 1 because the newly written interface used an
invalid `forall x in ...` spelling, and the next attempt exposed the related
parser recovery plus an ASCII `top` name. After replacing these with the
statement's accepted binder spelling and `⊤`, the exact same scoped recipe
above exited 0. These development failures are recorded rather than hidden;
they are not current source or environment failures.

The structural validator checks source hashes, frozen denominator
recomputation, eligibility projections, all required node fields, debt ranges,
typed edge endpoints and adjacency, reciprocal proof/composition edges,
proof-DAG acyclicity and reachability, validation-recipe coverage, and the
fail-closed root boundary. Lean checks the exact conditional composition and
prints its axiom dependencies. No generated `.olean` remains in the owned
path.

This phase freezes architecture only. `MorseNormalFormEngine` has no proof
body; `M0600-T-ENGINE` is the remaining root cut set. The checks do not prove
the Morse lemma, establish H0/R0, complete the dossier audit, or satisfy any
release gate. Master acceptance is still required.
