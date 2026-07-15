# THM-M-0783 proof recheck at `7787e214` (slot41)

Item: `S56-M-0783-PROOF`

Intent: `prove`

Recorded: `2026-07-15T21:55:05+08:00`

Base revision: `7787e214a8b29a1e90effb45a51c79bf485e1d78`

Base tree: `3bd6ee7fd3409565bd5ddfb06d6c007b063b7984`

## Verdict

`blocked`. No placeholder-free terminal proof body for
`Stage1Instances.THM_M_0783.MartinsAxiom` exists in the repository-local pinned dependency
closure. The frozen target is object-level Martin's axiom, an additional set-theoretic axiom rather
than a theorem supplied by the selected Lean/mathlib foundation. The dossier's provisional root
classification remains `[H5, M4, R4]`; rev-5.6 section 3.1 makes `H5` a barrier to ordinary theorem
proof execution.

The sole substantive proof leaf, `M0783-L-DENSE-FAMILY`, is definitionally
`ExpandedMartinsAxiom`, hence is the full missing proposition. The existing theorem
`root_of_denseFamilySolver` accepts that entire proposition as an explicit premise and transports
it to the root. Fresh `lake env lean --trust=0` elaboration confirms that this conditional
composition is valid and depends on `[propext, Classical.choice, Quot.sound]`; it supplies no
inhabitant of the premise and earns no root proof credit.

Fresh bounded scans found no Martin's-axiom, forcing-axiom, or dense-family-solver declaration in
the installed pinned package sources or an unconditional proof in target history. The nearest
pinned result is mathlib's Rasiowa-Sikorski construction `Order.idealOfCofinals` with
`Order.cofinal_meets_idealOfCofinals`. It requires an `Encodable` index type and therefore handles
only countable dense families, strictly weaker than families of every cardinality below the
continuum. An independently elaborated scratch construction confirmed this countable boundary and
the CH-conditional route: full `MartinsAxiom` follows from the extra premise
`Cardinal.continuum <= Cardinal.aleph 1`, not unconditionally. Neither result may replace the exact
target.

Introducing `MartinsAxiom` with `axiom`, a bodyless declaration, an extra premise, or a stronger
foundation would not prove the frozen target. Relative consistency, independence, consequences,
and barrier theorems are also distinct targets. None is silently substituted here.

The item remains `[ ]`; lifecycle remains `planned`; no proof body or receipt was produced. Audit
completion and theorem completion remain false. Because the requested proof phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` is deliberately absent.

## Scheduler Loop

Before this handoff, the owned path contained 23 integrated proof-recheck JSON/Markdown pairs, all
with verdict `blocked`, but the authoritative DAG still records `attempts: 0` and `children: []`.
Rev-5.6 section 10.2 requires an unresolved item to be split after five execution ticks rather than
repeatedly assigned unchanged. The master must reconcile attempt accounting and stop unchanged
positive-proof retries. This H5 target should be redirected to an explicit theory-extension,
barrier, consistency, independence, or corrected-statement workflow, or decomposed into meaningful
children. That is target-policy repair, not completion of this proof item.

One prerequisite inconsistency also remains outside this proof phase: the `M0783-ROOT` node in
`typed-graphs.json` has a stale `machine_debt` value of `M3`, while that artifact's closure boundary,
the anchor audit, obligation checker, and proof rechecks classify the open root as `M4`. This worker
preserves the frozen prerequisite artifact for master reconciliation.

## Failed Gate

The first failed gate is exact kernel closure of `M0783-L-DENSE-FAMILY` without a placeholder,
undeclared premise, foundation extension, or substituted theorem. The proof-relevant root cut is:

```text
M0783-L-DENSE-FAMILY
```

The complete frozen cut additionally contains `M0783-X-SOURCE`, `M0783-X-FOUNDATION`,
`M0783-X-PROVENANCE`, `M0783-X-READABLE`, and `M0783-X-WORKFLOW`.

Do not retry unchanged proof search. A proof retry requires a genuinely new immutable,
license-compatible Lean 4 terminal body for the exact target in the pinned repository-local closure,
with acceptable exact-type, axiom, placeholder, provenance, and composition reports. Otherwise the
master must apply the H5 redirect/split policy above.

## Narrow Validation

The automation-provided `Formalizations/Lean/.lake` symlink was treated as read-only. No `lake
update`, `lake build`, dependency clone/fetch, or checkout repair was run. Preflight reported only
that untracked symlink, so this is nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `git status --short --branch` | 0 | Detached `HEAD`; only `?? Formalizations/Lean/.lake` before this handoff |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 and the uniform L0/rework-required baseline passed |
| `python3 scripts/stage1_target.py show THM-M-0783` | 0 | Rank 788, lifecycle `planned`, legacy artifacts unaccepted, theorem incomplete |
| `LEAN_NUM_THREADS=1 timeout --foreground --kill-after=10s 600s python3 Stage1_Instances/THM-M-0783/check_statement.py` | 0 | Expression hash `c5896a33...5599ada`; four structural mutations killed; pinned Lean 4.29.0 and mathlib `8a178386...ea95` |
| `python3 Stage1_Instances/THM-M-0783/check_obligation_tree.py` | 0 | 12 obligations and 28 typed edges passed; denominator `0581a4ed...25532c9`; root open `M4` |
| `python3 Stage1_Instances/THM-M-0783/check_anchor_audit.py` | 0 | Anchor boundary, six Lean probes, local statement status, and pinned mathlib revision passed |
| Isolated trust-zero `lake env lean` elaboration of `Statement.lean` and `ObligationTree.lean` | 0 | Exact statement and conditional composition elaborated; axiom report `[propext, Classical.choice, Quot.sound]`; `Statement.olean` SHA-256 `a3bd8eef...415c6`, 38800 bytes; temporary objects removed |
| Scoped prohibited-construct scan of owned Lean sources | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, bodyless/opaque declaration, unsafe/oracle path, or proof placeholder |
| Scoped exact-candidate scan of installed pinned package Lean sources | 1 | Expected no-match: no Martin's-axiom, forcing-axiom, or dense-family-solver declaration found |
| Scoped Rasiowa-Sikorski scan of pinned mathlib | 0 | Found only the strictly weaker `Encodable`-family construction in `Mathlib/Order/Ideal.lean` |
| Target-scoped Git history declaration scan | 0 | No unconditional Martin's-axiom proof body found |
| Source/dependency hash and revision checks | 0 | Owned hashes match the structured handoff; mathlib is pinned at revision `8a178386...ea95`, tree `bdc39a31...c2b` |
| Target-scoped blocker invariant validation | 0 | JSON parsed; current base, blocked open state, unchanged vector, false completion flags, exact cut/paths, repeated-attempt evidence, and absent self-test agreed |
| `git diff --check` plus `git diff --no-index --check /dev/null` for both new handoff files | 0 | No whitespace errors or untracked-file diagnostics |

These successful checks validate the exact statement, frozen prerequisite artifacts, conditional
composition boundary, and repeated-attempt blocker. They do not prove Martin's axiom and do not
satisfy this proof item.
