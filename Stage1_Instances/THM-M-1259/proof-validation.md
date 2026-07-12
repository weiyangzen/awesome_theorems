# THM-M-1259 proof-phase blocker

Item: `S56-M-1259-PROOF`  
Date: `2026-07-12`  
Base revision: `6280a5556a0879b07f75e8bfd9359fa6cc60101b`

## Verdict

`blocked`: no eligible proof body for the exact Hormander sum-of-squares target exists in the
repository or pinned mathlib closure. The checked theorem
`expandedCore_composes_hormanderTarget` is only a conditional wrapper: it consumes
`ExpandedHypoellipticCore`, whose localized commutator estimate and regularity bootstrap remain
unimplemented. No premise, axiom, placeholder, weaker theorem, or substituted elliptic result was
added.

The first failed proof gate is `THM-M-1259-L-COMMUTATOR-ESTIMATE`. Its registry fingerprint is
explicitly `planned`, not a Lean declaration. Mathlib supplies useful definitions of distributions
and Lie brackets and a global first-order Sobolev inequality, but it does not supply the local
fractional positive-gain estimate for a variable-coefficient bracket-generating sum of squares.
Consequently the distribution regularization and arbitrary-order bootstrap are also open, and the
expanded analytic core cannot be constructed.

There is an additional statement risk that prevents truthful proof acceptance. `hormanderTarget`
quantifies over every `mu : Measure (Euclidean n)`, while the statement receipt calls this binder
Lebesgue measure. Because `IsSmoothDistribution` defines regularity by representation as a density
with respect to `mu`, replacing Lebesgue measure by an arbitrary measure, especially the zero
measure, materially changes the proposition. This proof attempt preserves the frozen target rather
than silently repairing or narrowing it.

Because the assigned proof phase is not self-tested complete, this attempt deliberately does not
create `.stage1-worker-selftest.json`.

## Narrow validation evidence

Commands ran in the worker clone. The pre-existing `Formalizations/Lean/.lake` entry is the
canonical pinned artifact link and was not modified. No Lake update, build, dependency clone, fetch,
or other dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard passes: 15 assurance groups and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1259` | 0 | Rank 161, planned, hard-mathlib-anchor lane, theorem incomplete. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1259/Statement.lean` | 0 | The exact root, expanded core, and conditional composition certificate elaborate with Lean 4.29.0. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1259/AnchorAudit.lean` | 0 | Supporting declaration types elaborate; none is an exact or stronger terminal theorem. |
| `rg -n '^\\s*(sorry\|admit\|axiom)(\\s\|$)' Stage1_Instances/THM-M-1259 --glob '*.lean'` | 1 | No prohibited Lean declaration token found; exit 1 means no match. |
| `rg -n -i -e 'h[oö]rmander' -e 'hypoellipt' -e 'subellipt' -e 'bracket.?generat' --glob '*.lean' Stage1_Instances Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | 125 textual hits occur only in this dossier and legacy `S1_M_161.lean`; no pinned mathlib terminal proof body was found. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |

The toolchain reports Lean commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
`Statement.lean` has SHA-256
`8258728ff71980a4431fb47213487c8d7655c64d0dd0f3ab2e9b058f8a95c0c7`; `lean-toolchain` has
SHA-256 `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; and
`lake-manifest.json` has SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Machine debt remains M4 and theorem completion remains false. The exact remaining machine cut set
is recorded in `proof-blocker.json`.
