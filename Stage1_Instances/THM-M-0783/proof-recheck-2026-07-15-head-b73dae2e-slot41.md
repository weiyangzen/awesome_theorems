# THM-M-0783 proof recheck at `b73dae2e` (slot41)

Item: `S56-M-0783-PROOF`

Intent: `prove`

Recorded: `2026-07-15T20:50:28+08:00`

Base revision: `b73dae2e6741a0be1f316d748a37f487a671cca4`

Base tree: `d582d50d420e2a27b4fb21ed0abea58cee03184f`

## Verdict

`blocked`. No placeholder-free terminal proof body for
`Stage1Instances.THM_M_0783.MartinsAxiom` exists in the repository-local pinned dependency
closure. The frozen target is object-level Martin's axiom, an additional set-theoretic axiom rather
than a theorem supplied by the selected Lean/mathlib foundation. The dossier's current provisional
root classification is `[H5, M4, R4]`; rev-5.6 section 3.1 makes `H5` a barrier to ordinary theorem
proof execution.

The sole substantive proof leaf, `M0783-L-DENSE-FAMILY`, is definitionally
`ExpandedMartinsAxiom`, hence is the full missing proposition. The existing theorem
`root_of_denseFamilySolver` accepts that entire proposition as an explicit premise and transports
it to the root. Fresh `lake env lean` elaboration confirms that this conditional composition is
valid and depends only on `[propext, Classical.choice, Quot.sound]`; it supplies no inhabitant of the
premise and earns no root proof credit.

Fresh bounded scans found no Martin's-axiom, forcing-axiom, or dense-family-solver declaration in
the installed pinned package sources or in target Git history. The nearest pinned theorem is
mathlib's Rasiowa-Sikorski construction `Order.idealOfCofinals` with
`Order.cofinal_meets_idealOfCofinals`. It requires an `Encodable` index type and therefore handles
only countable dense families, strictly weaker than the target's families of every cardinality
below the continuum.

Introducing `MartinsAxiom` with `axiom`, a bodyless declaration, an extra premise, or a stronger
foundation would not prove the frozen target. Replacing it by a countable-family theorem, a
conditional result, relative consistency, independence, or a consequence would substitute a
different theorem. None of these routes is allowed by the assigned gate.

The item remains `[ ]`; lifecycle remains `planned`; no proof body or receipt was produced. Audit
completion and theorem completion remain false. Because the requested proof phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` is deliberately absent.

One prerequisite inconsistency remains outside this proof phase: the `M0783-ROOT` node in
`typed-graphs.json` has a stale `machine_debt` value of `M3`, while the same artifact's closure
boundary, the anchor audit, the obligation checker, and proof rechecks classify the open root as
`M4`. This worker preserves the frozen prerequisite artifact for master reconciliation.

## Failed Gate

The first failed gate is exact kernel closure of `M0783-L-DENSE-FAMILY` without a placeholder,
undeclared premise, or foundation extension. The proof-relevant root cut is:

```text
M0783-L-DENSE-FAMILY
```

The complete frozen cut additionally contains `M0783-X-SOURCE`, `M0783-X-FOUNDATION`,
`M0783-X-PROVENANCE`, `M0783-X-READABLE`, and `M0783-X-WORKFLOW`.

Retry requires an immutable, license-compatible Lean 4 terminal proof body for the exact target in
the pinned repository-local closure with acceptable exact-type, axiom, placeholder, provenance, and
composition reports. Alternatively, the master must redirect this additional axiom to a
theory-extension, consistency, or independence target; that is a target-policy correction, not
completion of this proof item.

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
| `cd Formalizations/Lean && tmp=$(mktemp -d /tmp/thm-m-0783-slot41.XXXXXX) && lake env lean --trust=0 -t0 -R ../../Stage1_Instances/THM-M-0783 -o "$tmp/Statement.olean" ../../Stage1_Instances/THM-M-0783/Statement.lean && LEAN_PATH="$tmp" lake env lean --trust=0 -t0 -R ../../Stage1_Instances/THM-M-0783 ../../Stage1_Instances/THM-M-0783/ObligationTree.lean; s=$?; rm -rf "$tmp"; exit $s` | 0 | Exact statement and conditional composition elaborated at trust level zero; axiom report `[propext, Classical.choice, Quot.sound]`; temporary objects removed |
| Scoped prohibited-construct scan of owned Lean sources | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, bodyless/opaque declaration, unsafe/oracle path, or proof placeholder |
| Scoped exact-candidate scan of installed pinned package Lean sources | 1 | Expected no-match: no Martin's-axiom, forcing-axiom, or dense-family-solver declaration found |
| Scoped Rasiowa-Sikorski scan of pinned mathlib | 0 | Found only the strictly weaker `Encodable`-family construction in `Mathlib/Order/Ideal.lean` |
| Target-scoped Git history declaration scan | 0 | No unconditional Martin's-axiom proof body found |
| `python3 -m json.tool` plus target-scoped blocker invariant assertions | 0 | JSON parsed; current base, blocked open state, unchanged vector, false completion flags, exact cut/paths, and absent self-test agreed |
| `git diff --check` plus `git diff --no-index --check /dev/null` for both new handoff files | 0 | No whitespace errors or untracked-file diagnostics |

These successful checks validate the exact statement, prerequisite artifacts, and conditional
composition boundary. They do not prove Martin's axiom and do not satisfy this proof item.
