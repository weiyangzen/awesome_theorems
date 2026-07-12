# Exact-statement gate: blocked

Item: `S56-M-1174-STATEMENT`  
Theorem: `THM-M-1174`  
Base revision: `54743c8a753017ec2ce50ffebf85facec9112b95`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
entire mathematical wording is the method/family name `Moser iteration` and the phrase `local
boundedness of weak solutions`, attributed to Jurgen Moser in 1960. No primary source, edition,
theorem/page, displayed estimate, or uniquely quantified proposition is identified. The intake
dossier therefore freezes an ambiguous theorem family at `[H4, M4, R4]`, not a canonical human
claim.

The missing choices are mathematically substantive:

- elliptic versus parabolic equation, divergence versus non-divergence form, and the operator's
  sign convention;
- ambient dimension, domain, nested balls or cylinders, and interior versus boundary locality;
- scalar field, coefficient matrix, measurability, boundedness, ellipticity, and forcing terms;
- weak solution versus subsolution, the test-function class, sign assumptions, and Sobolev space;
- the input exponent and norm, essential-supremum convention, scaling powers, estimate constant,
  and every dependency of that constant; and
- zero solution, null or degenerate regions, endpoint exponents, and other boundary cases.

These choices produce inequivalent propositions. In particular, an elliptic local boundedness
estimate, a parabolic cylinder estimate, an abstract numerical iteration lemma, and a theorem about
harmonic functions are not interchangeable. Selecting any one because it is convenient to encode
would broaden, narrow, or substitute mathematics absent from the catalogue.

Consequently the statement phase fails at canonical human-claim identity, before minimal imports,
fixed binders and universes, an elaborated expression fingerprint, checked alternate transports,
or meaningful removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations can be defined. No Lean declaration, axiom, assumed PDE predicate, abstract interface
containing the conclusion, placeholder, or convenient special case was introduced. The statement
node remains open at `M4`; neither statement acceptance nor theorem completion is claimed.

## Repository and pinned-library boundary

Repository-wide discovery found only the underspecified catalogue wording, generated target
records, the intake dossier, and a neighboring dossier that explicitly treats Moser iteration as a
supporting or separate result. The pinned mathlib source contains a general mention of weak PDE
solutions in distribution documentation, but no Moser-iteration or local-boundedness theorem that
could identify the missing source claim. These negative searches are discovery evidence only and
do not perform the separately scheduled anchor audit.

There is no applicable `lake env lean <target>.lean` elaboration check: the expression to put in
that file is precisely what the source does not determine. Elaborating a freely selected
abstraction would be fake statement evidence rather than the smallest real validation of the
assigned deliverable.

## Validation evidence

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai). The canonical pinned `.lake`
directory was read only; no update, build, clone, fetch, or dependency mutation was performed.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1174` | 0 | rank 374, planned lifecycle, legacy artifacts unaccepted, theorem incomplete |
| repository `rg` search for the theorem ID, Chinese and English titles, and catalogue wording | 0 | only underspecified metadata, generated records, and the neighboring exclusion; no exact proposition |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `git -C "$(readlink -f Formalizations/Lean/.lake/packages/mathlib)" rev-parse HEAD` | 0 | pinned mathlib revision recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | the two hashes recorded above |
| pinned-mathlib `rg` search for Moser iteration, local boundedness, and weak solution/subsolution | 0 | one documentation mention of weak PDE solutions; no matching theorem target |

## Retry condition

An accountable source reviewer must pin an immutable primary or authoritative scholarly source by
edition and exact theorem/page, resolve corrections and errata, and freeze every equation, domain,
coefficient, solution, test-space, sign, exponent, norm, constant-dependency, quantifier, and
boundary-case choice listed above. A later statement worker can then encode that exact claim,
minimize pinned imports, serialize and hash its elaborated expression and environment, compile all
credited transports, and run all four required mutation classes.

The assigned phase is not genuinely self-tested to its completion gate. Therefore no
`.stage1-worker-selftest.json` is emitted.
