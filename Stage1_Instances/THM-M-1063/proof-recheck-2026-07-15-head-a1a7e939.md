# THM-M-1063 proof recheck at current base

Item: `S56-M-1063-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T05:15:55+08:00`

Base revision: `a1a7e939e58f103f5ff5d23af51437fa8658aa04`

Base tree: `d881fd9641fa3e5f3ebe5082b35672981e90adcf`

## Verdict

`blocked`. The proof phase remains `[ ]`; no proof body or proof credit was added.

The frozen target is the full finite-variance Donsker invariance principle in continuous path
space. The current repository and pinned dependency closure contain no theorem with that result.
The available `target_iff_expandedSourceShape` only unfolds the target definitions, while
`ObligationTree.exactRoot_of_exactRoot` requires the complete target as its hypothesis and returns
it unchanged. Neither is an inhabitant of the root.

Pinned mathlib provides the scalar central limit theorem and generic Gaussian-process,
tightness, Prokhorov, Arzela-Ascoli, and convergence-in-distribution infrastructure. Those APIs do
not prove polygonal-path measurability, finite-dimensional convergence, finite-second-moment
uniform tightness, or path-law identification for the frozen process. A local and pinned-package
source scan found no Donsker or functional central limit declaration.

The nearest additional source found in a pre-existing external audit cache is
`facebookresearch/atlas-lean` at indexed revision
`34ffed396f376454c1a9b297f3fd74c5c801fb50`. Its `BrownianMotion.lean` uses Lean 4.29.0 and the
same mathlib revision, but it only targets Rademacher finite-dimensional increments. Its decisive
`variable_block_CLT_tendstoInDistribution` and `slutsky_deterministic_perturbation` bodies contain
`sorry`, and it has no continuous-path tightness or path-space convergence theorem. It is therefore
ineligible for import or proof credit. No dependency was fetched, built, or modified.

The first failed frozen gate remains `M1063-C-PATH`: there is no checked construction packaging the
floor-based pointwise formula as a continuous path. The substantive root cut remains
`M1063-L-CLT`, `M1063-L-MODULUS`, `M1063-L-ASCOLI`, `M1063-L-PROKHOROV`,
`M1063-L-LAW-UNIQUE`, and `M1063-T-API`. All 29 machine-required obligations remain open and the
root remains `M4`.

## Narrow evidence

The commands below ran in this checkout. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1,546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1063` | 0 | Rank 506; planned; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1063/check_obligation_tree.py` | 0 | 31 obligations and 125 typed edges passed; denominator `a55c3e2...26a7703`; root open at M4. |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-1063/DonskerTarget.lean` | 0 | The exact target and definitional expansion elaborated; output identified `DonskerInvariancePrinciple : Prop`. |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-1063/ObligationTree.lean` | 0 | The identity interface elaborated and displayed the complete Donsker target as both input and output. |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-1063/AnchorAudit.lean` | 0 | The scalar CLT and generic convergence anchors resolved; reported axioms were only `propext`, `Classical.choice`, and `Quot.sound`. |
| `rg -n -i --glob '*.lean' '\b(donsker|functional[ _-]+central[ _-]+limit|invariance[ _-]+principle)\b' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | Expected no-match exit; pinned mathlib has no topical declaration. |
| `rg -n -i --glob '*.lean' '\b(donsker|functional[ _-]+central[ _-]+limit|invariance[ _-]+principle)\b' Formalizations/Lean/.lake/packages --glob '!mathlib/**'` | 1 | Expected no-match exit; no other pinned package has a topical declaration. |
| `rg -n --pcre2 '(^|[^[:alnum:]_])(?:sorry|admit|sorryAx|unsafe|implemented_by|native_decide)([^[:alnum:]_]|$)|^[[:space:]]*(?:axiom|constant|opaque|extern)[[:space:]]' Stage1_Instances/THM-M-1063 --glob '*.lean'` | 1 | Expected no-match exit; the owned Lean sources contain no prohibited construct. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 at `98dc76e...`; Lake 5.0.0-src at the same Lean revision. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Mathlib revision `8a178386...` and tree `bdc39a3...`. |
| `sha256sum Stage1_Instances/THM-M-1063/{DonskerTarget.lean,ObligationTree.lean,AnchorAudit.lean,obligation-registry.json,typed-graphs.json}` | 0 | `de889c4...a1847`, `047c49f...991425`, `dabce3d...cf4e43`, `7886d9c...85d5e8`, `e63f2ce...875b5`. |
| `python3 -m json.tool` plus current-base blocker invariant assertions | 0 | The blocker parses and its identity, base/tree, hashes, unchanged vector, open-root flags, empty proof-credit arrays, exact cut set, and absent completion manifest agree. |
| `git diff --check` plus `git diff --no-index --check /dev/null` for both fresh files | 0 | No whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent because the assigned proof phase is incomplete. |

## Boundary and retry condition

Lifecycle stays `planned`; `audit_complete=false` and `theorem_complete=false`. The planned intake
manifest still contains `[H2, M3, R4]`, while the later frozen closure and prior proof blocker
classify the open root as `M4`. This recheck does not edit authoritative state and, under the
fail-closed conflict rule, reports the weaker proof vector `[H2, M4, R4]` with no delta. There are
no accepted receipt IDs. This current-base record is nonrelease blocker evidence, not a proof
receipt, and it does not satisfy `S56-M-1063-PROOF` or support master acceptance.

Resume only after the frozen path construction, measurability, finite-dimensional convergence,
finite-second-moment tightness, subsequential limit identification, Brownian-law uniqueness, and
final API composition packages are implemented without placeholders, or after an immutable exact
Lean 4 proof can be pinned, imported, exact-type checked, and provenance validated. Because the
assigned proof deliverable is incomplete, `.stage1-worker-selftest.json` is deliberately absent.
