# Exact-statement gate: blocked

Item: `S56-M-1211-STATEMENT`  
Theorem: `THM-M-1211`  
Base revision: `7c261cad5ed43a724864ac5581564164750b865c`

## Decision

No exact Lean 4 target can be truthfully elaborated from the repository record. The complete source
wording is the title "Sogge local smoothing theorem", the attribution Christopher Sogge, the year
1991, and the gloss "local smoothing of solutions of the wave equation". It supplies no primary
source theorem/page, definitions, or errata disposition. The intake's references to Sogge's
monograph and the Seeger-Sogge-Stein paper are explicitly discovery candidates, not inspected
pinpoints.

This wording does not determine a proposition. In particular, it does not fix:

- the Euclidean wave propagator versus a variable-coefficient Fourier integral operator;
- the spatial dimension, scalar field, time interval, or spatial/frequency cutoff;
- the phase, amplitude, nondegeneracy, and cinematic-curvature hypotheses;
- the `L^p` range and whether an endpoint is included;
- the Sobolev/Bessel-potential conventions and exact derivative gain or epsilon loss;
- whether the constant is local or uniform and which parameters it may depend on.

These choices change the domains, ordered binders, hypotheses, and conclusion. The repository also
contains the same title as the separately scheduled `THM-M-0380`, and neighboring targets separately
name generic local smoothing and its conjectural family. Nothing in the metadata distinguishes a
numbered 1991 theorem from those alternatives. Selecting a convenient Euclidean estimate, a general
FIO estimate, or a later sharp exponent range would therefore substitute or broaden the unknown
root.

Consequently there is no source-faithful canonical expression to elaborate, no meaningful minimal
import set, no expression fingerprint or checked alternate transport, and no valid removed-
hypothesis, changed-domain, binder-scope, or boundary mutation suite. Introducing an abstract
predicate or a structure field that assumes the desired norm inequality would be fake statement
evidence. No Lean declaration, `sorry`, axiom, proxy predicate, or weakened theorem was introduced.
Machine state remains `M4`; statement acceptance and theorem completion are false.

## Pinned environment and search

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Commands ran in this worker clone using only the existing canonical pinned `.lake` artifacts. No
update, build, fetch, or clone command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1211` | 0 | rank 404, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| repository `rg` search for `Sogge`, local smoothing, and the source gloss | 0 | found only underspecified metadata, intake discovery candidates, the duplicate target, and unrelated uses of smoothing; no source-frozen proposition |
| pinned-mathlib `rg` search for Sogge, local smoothing, cinematic curvature, and Fourier integral operators | 1 | no matching theorem-specific source declaration (`rg` exit 1 means no match) |
| `git diff --check -- Stage1_Instances/THM-M-1211` | 0 | no whitespace errors after this artifact was added |

There is no applicable `lake env lean <target>.lean` check: an exact target expression does not
exist. Compiling an invented interface would validate that interface, not the assigned theorem.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact
theorem/page, including all referenced definitions and an errata check. It must freeze every
operator, domain, dimension, cutoff, curvature condition, exponent, Sobolev order, constant
dependency, and endpoint convention listed above, and distinguish this target from `THM-M-0380`,
`THM-M-1210`, and the local smoothing conjecture. A later statement run can then encode that exact
result, minimize its pinned imports, fingerprint the elaborated expression, check alternate
transports, and run all required mutation classes.

The assigned deliverable is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted. This artifact does not modify the execution DAG or claim
master acceptance, audit completion, or theorem completion.
