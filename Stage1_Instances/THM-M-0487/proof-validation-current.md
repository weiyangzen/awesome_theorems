# THM-M-0487 proof-phase partial implementation

Item: `S56-M-0487-PROOF`

Base revision: `ec3b52a20f5e28de012c23dce1af403343b9a1cb`

Base tree: `b08b83715d8f74868d1f31bbe82a7951b26edad1`

## Implemented Bodies

`Proof.lean` adds a complete finite set of ordered prime triples for each natural `n`, its
cardinality `representationCount`, and two unconditional proof bodies:

- `representationCount_pos_iff` proves that positivity of this finite count is exactly the frozen
  `ThreePrimeRepresentation n` witness predicate; and
- `weakGoldbachTarget_iff_positiveRepresentationCountTarget` proves both directions between the
  canonical weak Goldbach target and positivity of that count at every qualifying input.

These declarations are substantive partial progress toward `M0487-N-REPRESENTATION`, extending
its existential normalization with an exact finite-count interface. That frozen node already has
the narrower `threePrimeRepresentation_iff` formal target and provisional `M0-L` interface, so
zero frozen obligations are claimed closed by this proof phase.

## Open Root

The minimal open proof cut remains `M0487-T-ANALYTIC` together with
`M0487-T-FINITE-UPPER`. The new equivalence proves no positivity result. The analytic child still
requires a placeholder-free proof for every odd `n >= 10^27`; the finite child still requires the
exact theorem through `8875694145621773516800000000000`, a complete admitted certificate bundle,
and a sound kernel replay.

The existing `root_of_analytic_and_finite` and `finiteRange_of_publishedFiniteUpper` declarations
are checked conditional composition terms. They consume the missing packages and construct
neither. Returning either as the root would substitute an implication for the canonical target.

Searches over all repo-local Lean files and all 9,676 pinned package Lean files found no eligible
weak or ternary Goldbach terminal declaration. The exact Formal Conjectures surface has a literal
`by sorry`; the Vinogradov target is eventual only; the audited bounded, binary, and conditional
projects are statement-mismatched or placeholder-tainted.

The root therefore remains `[H1, M3, R3]`; `root_kernel_closed=false`,
`audit_complete=false`, and `theorem_complete=false`. This partial proof handoff is not theorem
completion and does not satisfy the complete proof deliverable. In short: this is not theorem completion.

## Commands And Results

No `lake update`, `lake build`, dependency clone/fetch, network request, or `.lake` mutation was
performed. The automation-provided canonical `.lake` symlink was reused read-only, and all Lean
outputs were written below `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0487` | 0 | rank 1366; planned; legacy artifacts unaccepted; theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-0487/check_anchor_audit.py` | 0 before the proof self-test packet existed; 1 after finalization | the audit itself passed with seven candidate records, no exact placeholder-free candidate, and root H1/M3/R3; its old checker then rejects the current proof packet because it hardcodes the later obligation-tree packet ID |
| `python3 -B Stage1_Instances/THM-M-0487/check_obligation_tree.py` | 1 | prerequisite checker has a stale hardcoded expectation that its integrated DAG item is `[ ]` with zero attempts; the authoritative DAG now truthfully says `[_]` with one attempt |
| `bash Stage1_Instances/THM-M-0487/check_proof.sh` | 0 | isolated `Statement -> ObligationTree -> Proof` replay at `--trust=0` under direct pinned Lean and mathlib's `lake env lean`; outputs agreed after path normalization; both bodies were sorry-free and reported exactly `propext`, `Classical.choice`, and `Quot.sound`; evidence hashes and open-root boundary passed |
| scoped search for weak/ternary Goldbach and three-prime terminal declarations | 0 | relevant hits were confined to this dossier and the neighboring eventual three-primes statement; pinned mathlib's only Goldbach match was an unrelated Fermat-number docstring |
| prohibited-device scan over `Proof.lean` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, bodyless declaration, unsafe declaration, native proof escape, or equivalent device |
| `git diff --name-status 9f2a15ae..HEAD` over frozen proof inputs and pins | 0 | empty output; no frozen statement, composition, registry, graph, audit, validation-spec, target-manifest, toolchain, or dependency input changed after the prior blocker was integrated |
| `git diff --check -- Stage1_Instances/THM-M-0487 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The paired receipt and blocker bind the exact source hashes, frozen registry denominator,
toolchain, dependency revisions, declarations, axiom reports, partial scope, and unchanged root
cut to this base revision.

## Retry Condition

Resume root closure after placeholder-free implementations of `M0487-T-ANALYTIC` and
`M0487-T-FINITE-UPPER` with all frozen dependencies are available. Alternatively, integrate an
immutable compatible Lean 4 declaration of the exact root with complete dependency and license
evidence, then repeat exact-type, trust, provenance, computation-coverage, and composition checks.
