# Anchor-audit validation record

Item: `S56-M-0580-ANCHOR_AUDIT`  
Base revision: `70b2a7ed5befb7d04e66a3a6907b5cd496a3b701`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The exact repo-local target is a proposition definition, and the legacy Stage1
file supplies only aliases, conditional identity wrappers, and adjacent
topology infrastructure. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the exact
three-dimensional statement as a `proof_wanted` source entry. That command does
not retain a theorem constant or proof body, so the entry is `M3`, not `M0-W`.

The immutable `lean-dojo/LeanMillenniumPrizeProblems` candidate at
`540da94826f70f3edf4d4fc66ce6cda20e903f61` also defines rather than proves its
dimension-three proposition. It adds `SecondCountableTopology`, fixes `Type*`,
and proves only a generalized dimension-zero special case. Its comment that
mathlib contains a proved Poincare conjecture conflicts with the audited pinned
mathlib source and receives no proof credit.

The bounded public searches found no additional candidate. Sourcegraph and
GitHub repository search returned zero, while GitHub code search required
authentication and is recorded as blocked rather than negative. Consequently
the canonical root is `M4`: no usable Lean 4 proof artifact was located. This
completes only the anchor-audit phase and does not claim exhaustive global
absence, audit completion, or theorem completion.

## Commands and exact outcomes

All Lean commands used the existing pinned Lake environment. No dependency
update, fetch, clone, or build was performed.

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact manifest revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'Perelman|Poincare...|nonempty_homeomorph_sphere_three' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | only the pinned Poincare source module and aggregate import matched; all root entries are `proof_wanted` |
| `rg -n -i 'Perelman|Poincare...|nonempty_homeomorph_sphere_three' Formalizations/Lean/.lake/packages --glob '*.lean' --glob '!mathlib/**'` | 1 | no non-mathlib pinned dependency match; exit 1 is ripgrep's expected no-match status |
| Sourcegraph public search for the recorded alias family | 0 | `matchCount=0`; response SHA-256 `d6369e...68ba` |
| GitHub REST repository search for `Poincare Lean theorem` | 0 | `total_count=0`, complete response; SHA-256 `08c082...600b` |
| GitHub REST code search for `Perelman language:Lean` | 0 | response captured with HTTP 401; SHA-256 `b7dbd1...5e29e`; lane blocked |
| GitHub contents API inspection of `LeanMillenniumPrizeProblems@540da9...f61/Problems/Poincare/Millennium.lean` | 0 | source SHA-256 `045a97...deba`; dimension-three root is a `def`, only dimension zero is proved |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0580/AnchorAudit.lean` | 0 | five nearby pinned mathlib declarations elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0580/Statement.lean` | 0 | exact canonical target and definitional expansion re-elaborated |
| `python3 Stage1_Instances/THM-M-0580/check_anchor_audit.py` | 0 | pins, clean mathlib tree, source hashes, source markers, external classification, and fail-closed root status agreed |
| `python3 -m json.tool Stage1_Instances/THM-M-0580/anchor-audit.json` | 0 | structured ledger is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0580 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Open integration gate

Reopen only for a concrete terminal Lean 4 proof at an immutable revision with
its full dependency lock and license. Its elaborated type must match the frozen
target, its terminal body and transitive trust closure must be gap-free, and a
repo-local checked wrapper must pass. A URL, statement definition,
`proof_wanted` marker, or unrelated dimension-zero proof cannot cross this gate.
