# Proof execution record

Item: `S56-M-1105-PROOF`  
Theorem: `THM-M-1105`  
Execution date: `2026-07-12`  
Base revision: `270e3fb34fda8c9a44c27d55bd2b9ac69b3c4945`

## Verdict

The proof phase is blocked and is not self-tested as complete. No proof body was added, no
obligation was marked closed, and no self-test receipt was emitted.

The frozen registry requires twenty machine obligations. All twenty still have
`terminal_proof_body_id: null`. The only existing theorem,
`Stage1.THM_M_1105.ObligationTree.root_of_sample_weak_convergence`, proves the definitional
transport from an assumed `SampleWeakConvergence` terminal to the root conclusion. Its `terminal`
argument is exactly the open analytic conclusion and therefore supplies no closure for
`M1105-T-WEAK` or any of its dependencies.

The preceding immutable anchor audit found no exact theorem in the repository or pinned mathlib.
The only external finite-combinatorial candidate covers part of the Catalan branch and supplies
none of the random-matrix expectation, concentration, almost-sure moment, tightness, or
bounded-continuous approximation results. Importing or wrapping it would not prove the frozen
target. Consequently there is no dependency-legal proof body that can truthfully be pinned or
wrapped in this phase.

## First failed gate and root cut

The first failed gate is kernel closure of the frozen proof obligations. The immediate substantive
cut is:

- `M1105-L-NONPAIR`: asymptotic suppression of non-pairing and diagonal walk patterns;
- `M1105-L-PAIRING` and `M1105-L-CATALAN`: leading-walk classification and Catalan count;
- `M1105-L-CONCENTRATION`: summable deviations for normalized trace moments;
- `M1105-T-MOMENTS-AS`: simultaneous almost-sure convergence of all moments;
- `M1105-L-SEMICIRCLE-MOMENTS` and `M1105-L-TIGHTNESS`;
- `M1105-L-POLYNOMIAL`, `M1105-L-BC-APPROX`, and `M1105-T-WEAK`.

Each is a major formalization package rather than an available theorem invocation. The exact root
therefore remains `M3`; theorem completion, proof-phase completion, `M0`, `H0`, and `R0` are not
claimed.

## Validation evidence

All commands reused the existing pinned `.lake` symlink. No update, build, clone, fetch, or other
dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1,546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets with ranks 1 through 1,546 |
| `python3 scripts/stage1_target.py show THM-M-1105` | 0 | rank 545; lifecycle planned; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1105/check_obligation_tree.py` | 0 | 22 obligations and 108 typed edges valid; root explicitly open at M3 |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1105/Statement.lean)` | 0 | exact proposition elaborated; only unused-hypothesis linter warnings |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1105/ObligationTree.lean)` | 0 | conditional terminal-to-root transport elaborated; only unused-hypothesis linter warnings |
| `rg -n -i 'wigner|semicircle|semi.?circle' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | only the unrelated geometric use of “semicircle” in Thales' theorem |
| `rg -n '\\b(sorry|admit|axiom)\\b' Stage1_Instances/THM-M-1105 --glob '*.lean'` | 1 | no forbidden Lean declaration or proof placeholder found |
| `git diff --check -- Stage1_Instances/THM-M-1105` | 0 | no whitespace errors before this record was added |

The structural and elaboration checks establish that the open architecture is internally
consistent. They do not turn the assumed terminal in `ObligationTree.lean` into a proof.
