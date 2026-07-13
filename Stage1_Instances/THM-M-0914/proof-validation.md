# THM-M-0914 proof-phase validation

Item: `S56-M-0914-PROOF`. Base revision:
`9f2a15ae074a155a719c4b743df26f1e993312da`.

## Implemented proof

`Proof.lean` installs the manifest-pinned declarations
`Fintype.exists_ne_map_eq_of_card_lt`,
`Finset.exists_ne_map_eq_of_card_lt_of_maps_to`, and
`Finset.card_le_card_of_injOn` at their frozen interfaces. It then checks the
exact `Fin (n + 1) -> Fin n` target through two views of one proof route:

- the pinned finite-type wrapper composed with the frozen `Fin` cardinality
  package;
- the fully expanded frozen graph, including the cardinality bound,
  no-collision-to-injectivity conversion, finite-set terminal, universe
  membership normalization, finite-type wrapper, and exact root composition.

The direct and expanded roots share the same pinned finite-set terminal body,
so they receive no duplicate terminal-proof credit. All ten obligations
reachable from `M0914-ROOT` in the frozen proof graph now have provisional
proof bodies. The three predecessor-owned statement/interface obligations are
not reclaimed, and `M0914-S-FOUNDATION` remains open for downstream assurance.

The two exact root declarations elaborate, all twelve pinned and target-local
declarations are sorry-free, and their axiom reports are exactly `propext`,
`Classical.choice`, and `Quot.sound`. No target hypothesis, binder, boundary
case, carrier, or conclusion changed. This supports an `M0-W` route proposal
after master acceptance and validation. The accepted vector remains
`H1/M3/R4`, and this proof phase does not claim theorem completion.

## Commands and results

Commands ran in the isolated worker clone on 2026-07-13 (Asia/Shanghai).
`check_proof.sh` copied only `Statement.lean`, `ObligationTree.lean`, and
`Proof.lean` to a temporary directory; built temporary local oleans; put that
directory ahead of the pinned `LEAN_PATH`; and deleted it on exit. Existing
canonical pinned `.lake` artifacts were reused read-only. No `lake update`,
`lake build`, dependency clone/fetch, network access, or `.lake` mutation ran.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546
  uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0914
  exit 0: rank 1456, planned, L0/rework-required, theorem incomplete

bash Stage1_Instances/THM-M-0914/check_proof.sh
  exit 0: three pinned declarations and nine target-local declarations
  elaborated; all twelve were sorry-free and reported exactly
  [propext, Classical.choice, Quot.sound]

python3 -B Stage1_Instances/THM-M-0914/check_proof.py
  exit 0: exact source markers, frozen target and graph, receipt/input hashes,
  mathlib source/body/olean pins, worker packet, placeholder policy, and dirty
  ownership boundary passed

python3 -B Stage1_Instances/THM-M-0914/check_obligation_tree.py
  exit 1: the predecessor checker revalidated deterministic generation, the
  frozen artifacts, and the conditional Lean architecture, then reached its
  obligation-phase-only packet code and raised `UnboundLocalError` because no
  obligation-phase packet was supplied. The proof checker independently
  rechecks the immutable registry, graph, pins, and exact composition without
  modifying the predecessor checker or receipt.

python3 -m json.tool Stage1_Instances/THM-M-0914/proof-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0: both structured artifacts parse

PYTHONPYCACHEPREFIX=/tmp/stage1-m0914-proof-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0914/check_proof.py
  exit 0: the scoped proof validator compiles without writing generated files
  under the owned path

git diff --check -- Stage1_Instances/THM-M-0914 \
  .stage1-worker-selftest.json, plus no-index checks for untracked files
  exit 0 / exit 1 expected for no-index differences: no whitespace diagnostics
```

The node-specific receipt is `proof-receipt.json`. Only the integration lane
may accept it in dependency order or change authoritative state. Human-source
H0, readable R0, full foundation/provenance/trust acceptance, hermetic and
independent validation, release, `AUDIT-Z`, and `THEOREM-Z` remain open.
