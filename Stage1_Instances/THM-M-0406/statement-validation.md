# Statement validation record

Item: `S56-M-0406-STATEMENT`  
Base revision: `026b21f5359f8f2e643d0f1ee2846428c517be20`

## Frozen target

The canonical declaration is
`Stage1Instances.THMM0406.CorvajaZannierTheoremOne`. It transcribes Theorem 1
of Corvaja and Zannier, *On integral points on surfaces*, pages 706-707. The
primary source resolves the repository metadata conflict: the authors are
Corvaja and Zannier, the object is a surface, and Evertse is mentioned later
only as a source of quantitative Subspace-Theorem estimates.

The target retains the number field, finite place set, geometrically
irreducible nonsingular projective surface, affine open, at least four
distinct irreducible boundary divisors, no-three-meet condition, global
positive weights and intersection constant, and the conclusion that one
proper curve contains all `S`-integral rational points. Mathlib schemes and
finite places are used directly. Missing divisor-intersection and integral
surface-point infrastructure is represented by typed operations and
predicates, not by an opaque stand-in for the theorem.

## Commands and results

All commands ran in this worker clone. Lean ran from `Formalizations/Lean`
and reused the existing pinned Lake environment without mutating it.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0406/Statement.lean` | 0 | Canonical target and exact-type fixture elaborated; fully explicit `#print` output SHA-256 is `0f59d3486b6464922278f83f5e3871c79e0c2e7964d1e3a8a412f16e567b385b`. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0406` | 0 | Rank 19, planned, L0/rework_required, theorem incomplete. |
| `for f in Stage1_Instances/THM-M-0406/{instance,task-dag,statement}.json; do python3 -m json.tool "$f" >/dev/null || exit; done` | 0 | All structured artifacts parsed. |
| `git diff --check -- Stage1_Instances/THM-M-0406 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

## Mutation boundary

Removing `r >= 4`, smooth/geometric irreducibility, affineness, boundary
irreducibility, the no-three-meet condition, positivity, or the common
intersection equation changes the primary theorem. So does moving weights
under the divisor-pair binders, changing the domain to arbitrary schemes, or
admitting zero-weight and too-few-divisor boundary cases. These variants are
not credited. This record establishes statement elaboration only.
