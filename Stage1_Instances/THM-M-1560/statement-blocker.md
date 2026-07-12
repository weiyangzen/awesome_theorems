# Exact-statement gate: blocked

Item: `S56-M-1560-STATEMENT`  
Theorem: `THM-M-1560`  
Base revision: `b5768b55f94197ed20d70d350ea6d4def3c3a667`

## Decision

The exact Lean 4 target cannot be truthfully selected or elaborated from the authoritative
repository record. That record gives only the name "Deift-Zhou method," the authors and year, and
the phrase "steepest descent method." A method is not one proposition. The intake identifies the
1993 Annals paper *A steepest descent method for oscillatory Riemann-Hilbert problems. Asymptotics
for the MKdV equation* as a primary-source candidate, but no immutable full-text edition, numbered
theorem/page, exact transcription, premise map, errata disposition, or independent source review is
available in the dossier.

Choosing a target from the paper title would leave mathematically material choices unresolved:

- the modified-KdV normalization, sign convention, and class of initial or scattering data;
- the matrix Riemann-Hilbert contour, orientation, boundary values, jump convention, and
  normalization at infinity;
- regularity, decay, symmetry, spectral-singularity, reflection, and discrete-spectrum hypotheses;
- the space-time sector and scaling variable, including stationary points, transition regions, and
  boundary rays;
- the reconstruction map, special-function and phase conventions, leading coefficient, norm,
  uniformity quantifiers, and error rate;
- the treatment of zero reflection, soliton poles, coalescing stationary points, and other
  degenerate data.

These choices change the domains, ordered binders, hypotheses, conclusion, and excluded boundary
cases. Substituting an abstract `Prop`, a structure that stores the desired asymptotic estimate, a
generic small-norm interface, or a convenient scalar steepest-descent theorem would broaden or
weaken the source claim. No such declaration, axiom, placeholder, or assumed conclusion was added.

The first failed gate is rev-5.6 section 5 exact source-statement identification. It fails before
minimal imports, canonical elaboration, expression and environment fingerprints, checked
transports, or removed-hypothesis, changed-domain, binder-scope, and boundary mutation tests can be
meaningfully produced. The canonical formal target remains absent and machine state remains `M4`.
No statement acceptance, proof credit, audit completion, or theorem completion is claimed.

## Pinned checks

All commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). The canonical pinned `.lake`
artifacts were read through the pre-existing worker link. No `lake update`, build, dependency clone,
fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1560` | 0 | Rank 571, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | SHA-256 `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| repository `rg` for Deift-Zhou, nonlinear steepest descent, oscillatory Riemann-Hilbert, and modified KdV | 0 | Only target metadata and neighboring dossiers matched; no theorem-specific local Lean artifact or source-frozen proposition |
| pinned-mathlib `rg` for Riemann-Hilbert, steepest descent, modified KdV, mKdV, and oscillatory jumps | 1 | No matching API; exit 1 is the expected negative-search result |

There is no valid `lake env lean <target>.lean` check: the exact expression required to create that
file is precisely what the missing source decision prevents. Elaborating an invented interface
would be fake evidence rather than the assigned deliverable.

## Retry condition

An accountable source review must pin an immutable full-text edition and select one exact numbered
theorem/page. It must transcribe and independently verify every premise and conclusion, resolve
errata and imported inverse-scattering boundaries, and freeze all conventions and degenerate cases
listed above. A later statement run can then encode the exact target, minimize imports in the pinned
environment, fingerprint the elaborated expression, add checked alternate encodings, and run the
four required mutation classes.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
