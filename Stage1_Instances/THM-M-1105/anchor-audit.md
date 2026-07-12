# Anchor audit

This audit is for `S56-M-1105-ANCHOR_AUDIT` and the exact proposition
`Stage1.THM_M_1105.WignerSemicircleLaw`. The frozen inventory and immutable candidate identities
are in `anchor-inventory.json`. Search cutoff: 2026-07-12 (Asia/Shanghai).

## Result

No repo-local, pinned-mathlib, or external Lean 4 theorem was found that proves the exact almost-sure
bounded-entry Wigner semicircle target. The machine classification advances from `M4` to `M3`:
the exact statement and several kernel-checked interfaces exist, but the theorem proof and major
analytic bridges do not. This is `formalization_debt`, not repo-local integration debt. No external
candidate warrants `M1`, and this audit claims neither root closure nor theorem completion.

| Candidate | Immutable identity | Exact scope and disposition |
|---|---|---|
| repo-local | repository base `d6c8d69dcdc00307a764772787a5e3d4d895147b` | No exact proof body or wrapper. Existing weak-convergence work is supporting API exploration only. |
| mathlib | `mathlib4@8a178386ffc0f5fef0b77738bb5449d50efeea95` | No Wigner/semicircle declaration. `Matrix.IsHermitian.eigenvalues`, `trace_eq_sum_eigenvalues`, `iIndepFun.charFun_map_sum_eq_prod`, and `ProbabilityMeasure.tendsto_iff_forall_integral_tendsto` are usable interfaces, not a semicircle proof. |
| semicircle-catalan | `Wondermonger-daydreaming/semicircle-catalan@95d99de4490a50af6d909f27e670a82691d6c4e8` | Placeholder scan of the immutable Lean archive was empty. `Pairing.genus_zero_iff_noncrossing`, `card_noncrossingPairing_eq_catalan`, and `Pairing.genus_zero_count` close a finite combinatorial branch. The project explicitly says it does not formalize the analytic probability theory, so it is a strict partial candidate and cannot close this target. Toolchain `v4.29.0-rc6`, mathlib `1f3cdaa...`, Apache-2.0. |
| HighDimProb | `dududuguo/HighDimProb@8d4eec8bc06d80e8436ab3505000fca999b46546` | Provides random-matrix/concentration infrastructure. Immutable archive searches found no Wigner, semicircle, empirical spectral measure, or equivalent exact theorem. Toolchain `v4.29.1`, mathlib `5e932f9...`, Apache-2.0. |

The semicircle-catalan archive SHA-256 is
`6bfa9530cdc687c2202ad0b5047aa03ef7a78bf351f4b311d16a8cb93cfb88e8`; its two principal source
hashes are `8117db5e31b0d7f2631ea70904e7c127519bcf4719e5a98425bb11d3dafde345` and
`fbc3b3900e85f45f12d840273c6edf66886632a820ae487867413f63c7d0f5dc`. The HighDimProb archive
SHA-256 is `e924a9a05112ddabc257b03bc95c67ca5f62e812f91a0c72bbdfcdc02b4bd703`.

## Statement comparison

The finite pairing candidate could support a future moment-method branch showing that limiting
even moments are Catalan numbers. It supplies none of the target's random-matrix hypotheses,
trace-moment expansion, suppression of non-pairing/higher-genus terms, variance or concentration
bound, almost-sure upgrade, moment determinacy, or bounded-continuous-test-function convergence.
Thus importing it today would not yield an exact wrapper and would create no integration debt.

Mathlib supplies eigenvalue enumeration for Hermitian matrices and a generic weak-convergence
characterization. It does not supply the bridge from the empirical spectrum of the random matrices
to the semicircle density. HighDimProb is similarly infrastructural and statement-mismatched.

## Discovery ledger

Search order followed rev-5.6 section 7.2: local sources, pinned mathlib, then public Lean 4
repositories. Queries included `Wigner`, `Wigner semicircle`, `semicircle`, `semi-circle`,
`random matrix Lean4`, `empirical spectral measure`, `eigenvalue distribution`, `weak convergence`,
and `Catalan moments`. Repo-local and mathlib searches used `rg` over Lean sources. GitHub repository
search and immutable `git ls-remote`/archive downloads located and froze the two external projects.
The GitHub code-search API was unavailable without authentication, and grep.app returned HTTP 503;
these are access limitations, not silent negative results. No dependency was cloned, fetched into
the project, or added to `.lake`.

## Validation

Base revision: `d6c8d69dcdc00307a764772787a5e3d4d895147b`.

| Command | Result |
|---|---|
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1105/AnchorAudit.lean)` | exit 0; all four supporting interface declarations elaborated; the exact root's separate statement check remains in `statement-validation.md` |
| `rg -n -i "wigner|semicircle|semi.?circle" Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | exit 0 only for Thales' geometric semicircle; no random-matrix candidate |
| immutable archive search for `Wigner`, `semicircle`, `empirical.*(spectr|eigen)`, `spectral.*measure` in HighDimProb | no matches |
| placeholder scan `rg -n "\\b(sorry|admit|axiom)\\b"` over semicircle-catalan Lean sources | no matches |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0 |
| `python3 scripts/stage1_target.py check` | exit 0 |

The next phase must freeze an obligation tree whose root cut includes the analytic bridges listed
above. This receipt completes candidate classification only; source fidelity, proof, trust closure,
readability, hermetic release, and independent review remain open.
