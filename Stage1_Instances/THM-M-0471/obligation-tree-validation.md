# THM-M-0471 obligation-tree validation

Item: `S56-M-0471-OBLIGATION_TREE`

Base revision: `5fe11f4b5e32a06ffb4432460319fc8ae906fe7b`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Frozen result

Registry version 1 freezes 22 unique semantic obligations before proof-phase adoption. The
canonical ten-field projection has SHA-256
`d3f11762e2a0f4c384d094d53e44100f20a21f81eb6ce527cd5f9897a9bc445c`.
The bundle contains 54 edges across separate proof, refinement, provenance, evidence, trust,
documentation, and workflow graphs. The proof DAG expands the visible pinned route through witness
construction, nonemptiness, primality, product reconstruction, uniqueness, the generic recursive
prime-product permutation theorem, divisor membership, erasure, and cancellation. All semantic
ledgers have budgets at most 65 steps.

Validation uses only the existing manifest-pinned Lake artifacts. No Lake update or build,
dependency clone or fetch, or other `.lake` mutation was performed.

## Commands and results

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546
  uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0471
  exit 0: rank 1353, planned, L0/rework_required, theorem_complete false

python3 -B Stage1_Instances/THM-M-0471/build_obligation_artifacts.py
  exit 0: wrote 22 obligations and 54 typed edges
  denominator: d3f11762e2a0f4c384d094d53e44100f20a21f81eb6ce527cd5f9897a9bc445c
  a second run produced byte-identical registry, graph, and recipe files

python3 -B Stage1_Instances/THM-M-0471/check_obligation_tree.py
  exit 0: PASS THM-M-0471 obligation tree: 22 obligations, 54 typed edges
  root closure: open (H1/M3/R4); the exact pinned family remains the proof-phase cut

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0471
LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean Statement.ilean
  exit 0: the canonical statement re-elaborated; both conditional compositions elaborated;
  exactPrimeListAnchor_of_packages reported [propext] and
  root_of_exactPrimeListAnchor reported [propext]; temporary outputs were removed
  obligation stdout SHA-256: e29073a26d924f453e3a58f73678aafce5bf6d35989b4a8bc29ee11060f6711e

python3 Stage1_Instances/THM-M-0471/check_anchor_audit.py
  exit 0: four immutable candidates, exact pinned source bodies, expression identity,
  hashes, direct axiom/sorry probes, and fail-closed status passed on the integrated base

cd Formalizations/Lean &&
  python3 ../../Stage1_Instances/THM-M-0471/check_statement.py
  exit 0: exact expression and source fingerprints, direct expansion, minimal import,
  four killed mutations, and the n = 2 boundary passed

python3 -B Stage1_Instances/THM-M-0471/check_intake.py
  exit 0: planned H1/M3/R4 dossier, expanded owned inventory, and open local tasks passed

python3 -m json.tool <each owned JSON and .stage1-worker-selftest.json>
  exit 0: all structured artifacts are valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0471-obligation-pycache \
  python3 -m py_compile <five owned validators/generator>
  exit 0: Python sources compiled outside the repository tree

rg -n -i --glob '*.lean' <prohibited proof/oracle markers> \
  Stage1_Instances/THM-M-0471/ObligationTree.lean
  exit 1: expected no-match result

git diff --check -- Stage1_Instances/THM-M-0471 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics; per-new-file no-index checks were also empty
```

The structural checker also validates authoritative item identity without changing state, the
accepted prerequisite cursor, frozen input hashes, canonical denominator and exclusions, complete
node schema, node/obligation bijection, all graph adjacency indices, endpoint legality, acyclicity,
reciprocal proof edges, exact proof reachability, recipe coverage, open closure, pinned source
hashes and declaration markers, receipt invariants, exact self-test changed paths, owned inventory,
newlines, and public-path hygiene.

## Status boundary

`ObligationTree.lean` validates conditional compositions whose mathematical packages are explicit
premises. It does not invoke or install the audited mathlib family. The root therefore remains
`[H1, M3, R4]`; accepted proof state is empty, and H0, accepted M0, R0, complete provenance/trust,
audit completion, validation, independent verification, release, and theorem completion remain
open. This worker packet is provisional and still requires dependency-ordered master acceptance.
