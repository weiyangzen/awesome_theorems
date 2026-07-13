# THM-M-0554 proof-phase recheck: blocked

Item: `S56-M-0554-PROOF`

Attempt: `2026-07-14T02:37:59+08:00`

Base revision: `40801f373a9b0443cc58ff8ec365fb5b75c8b8c3`

Base tree: `f3b8367a9ec13bd00b783bc4367d64003ffcde28`

## Verdict

`blocked`. No genuine Atiyah-Hirzebruch spectral-sequence proof body was
implemented or found in the pinned dependency closure. The root remains `M4`;
this attempt adds no proof receipt, composition certificate, debt-vector
change, or state transition.

The immediate root cut remains:

- `M0554-X-GENCOH`: generalized-cohomology pair, excision, and wedge infrastructure;
- `M0554-C-EXACT-COUPLE`: the skeletal-filtration exact-couple construction;
- `M0554-C-E2-MODEL`: the cellular-cohomology `E2` identification;
- `M0554-L-STRONG`: strong convergence for the finite skeletal filtration.

Pinned mathlib supplies only generic spectral-sequence, CW-complex, and
singular-homology substrate. A fresh search of every pinned package found no
AHSS, generalized-cohomology, exact-couple, or strong-convergence proof body.
Mathlib's spectral-object file also documents its intended `spectralSequence`,
`homologyData`, and `spectralSequenceHomologyData` constructions as `TODO`.

## First Failed Gate

The exact-statement-fidelity gate fails before a proof can be credited. In
`Statement.lean`, the theory facts `pointIsPoint`, `exactnessAxiom`, and
`wedgeAxiomOrRepresentability`, and the CW facts `finiteCW`, `exhaustive`, and
`cellAttachments`, are proposition-valued data rather than required proofs.
The output chooses the meanings of `coefficientConvention`,
`strongConvergence`, and `naturalityInSpace`, while
`filtrationIsInducedBy` is only `K.skeleton = K.skeleton`.

Consequently the literal proposition has a zero spectral-sequence inhabitant
using zero objects, reflexive isomorphisms, and output-selected `True`
propositions. An independent disposable trust-level-zero probe elaborated that
term and reported only `propext`, `Classical.choice`, and `Quot.sound`. The
term is deliberately not retained or credited: it constructs no AHSS and
consumes none of the frozen semantic children. Accepting it would violate the
no-fake-result and checked child-to-parent composition rules.

There is also an unresolved predecessor-authority mismatch. `instance.json`
still records a null canonical module, declaration/expression, expression
hash, and environment fingerprint with status `open_statement_phase`, whereas
`statement.json` separately records provisional elaboration. A proof-only
worker cannot silently replace those predecessor artifacts.

## Validation

All Lean commands reused the automation-provided symlink to the pinned
canonical `.lake` artifacts. No update, build, dependency clone/fetch, network
action, or `.lake` mutation was performed. Generated Lean objects were placed
in a temporary directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | 32 obligations and 91 typed edges passed; denominator `3c72072a...8048b`; root remains M4 without a composition certificate. |
| Isolated `lake env lean --trust=0 -R "$target" -o "$tmp/Statement.olean" "$target/Statement.lean"` from `Formalizations/Lean` | 0 | The frozen target elaborated with Lean 4.29.0; temporary output size was 429072 bytes and was removed. |
| `rg -n -i --glob '*.lean' 'Atiyah[-_ ]?Hirzebruch|AtiyahHirzebruch|\\bAHSS\\b|generalized[ _-]*(co)?homology|exact[ _-]*couple|strong[ _-]*convergence' Formalizations/Lean/.lake/packages` | 1 | Expected no-match result: no pinned proof candidate was found. |
| The same query over repo-local Lean sources outside this dossier | 0 | Hits were the legacy `S1_M_106.lean` statement/audit surface and unrelated proof plans, not a terminal AHSS proof body. |
| `rg -n --pcre2 '^\\s*(?:sorry|admit|axiom)(?:\\s|$)|\\bsorryAx\\b|^\\s*unsafe(?:\\s|$)' Stage1_Instances/THM-M-0554 --glob '*.lean'` | 1 | Expected no-match result: no prohibited declaration token occurs in the owned Lean sources. |
| Pinned toolchain, mathlib revision/tree, and manifest checks | 0 | Lean `4.29.0` commit `98dc76e...16740`; mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`; manifest SHA-256 `321626c8...2d81`. |
| Spectral-object source hash and TODO scan | 0 | SHA-256 `2ce62b9d...740aa`; the intended generic constructors are documented as `TODO`. |

## Retry Condition

First publish and master-accept a source-faithful statement, reconcile the
instance authority, and issue obligation-registry version 2. Then implement
and compose the four root-cut packages without placeholders. An alternative is
an immutable exact compatible Lean 4 AHSS proof that can be pinned,
exact-type transported, and checked with full provenance and trust closure.

This artifact is durable blocker evidence only. It does not satisfy
`S56-M-0554-PROOF`, close an obligation, complete the audit or theorem, or
authorize master acceptance. Because the assigned phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` remains absent.
