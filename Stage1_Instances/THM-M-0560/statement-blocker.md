# Exact-statement gate: blocked

Item: `S56-M-0560-STATEMENT`  
Theorem: `THM-M-0560`  
Base revision: `60aae17521cd359d0473812b6927789cb4fee9e6`

## Decision

An exact Lean 4 target cannot yet be truthfully selected from the authoritative repository record.
The record fixes only the Chinese phrase `广义上同调论的可表性` ("representability of generalized
cohomology theories"), Edgar Brown, and 1962. The intake deliberately leaves the canonical root
open pending inspection of Brown's 1962 article and 1963 correction. Those documents are currently
only bibliographic discovery anchors: no immutable copy, full page range, theorem/page pinpoint,
verbatim result, imported definitions, or correction crosswalk exists in this clone.

The short phrase does not determine a unique proposition. In particular it does not fix:

- Brown's general contravariant-functor theorem versus its generalized-cohomology consequence;
- reduced versus unreduced theories, or pointed sets versus groups or abelian groups;
- the precise connected pointed CW domain and its smallness conventions;
- the variance, wedge cardinality, and exact wedge-to-product comparison;
- the excision, weak-pushout, or Mayer-Vietoris exactness hypothesis;
- degreewise representing spaces versus compatible spectrum structure;
- treatment of the one-point space, disconnected spaces, the zero theory, empty or infinite
  wedges, and degree shifts.

These choices alter domains, ordered binders, hypotheses, and the conclusion. Selecting one from
memory, replacing the theorem by an abstract category whose Brown properties are merely assumed,
or elaborating only `Functor.IsRepresentable` would substitute a representability interface for
Brown's existence theorem. The existing
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_139.lean` expressly records that boundary.

Consequently there is no canonical declaration on which to perform minimal-import reduction,
expression hashing, checked transports, or meaningful removed-hypothesis, changed-domain,
binder-scope, and boundary mutations. No Lean declaration or proof escape was introduced. Machine
state remains `M4`; statement acceptance, audit completion, and theorem completion are false.

## Pinned environment and validation

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Commands ran inside this worker clone. The canonical `.lake` artifacts were read only; no update,
build, clone, or fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and exactly 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0560` | 0 | rank 608, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| repository `rg` search for the theorem title, translated claim, Brown representability, and *Cohomology Theories* | 0 | found only underspecified metadata, discovery anchors, and the explicit representability-interface boundary |
| pinned-mathlib `rg` search for Brown representability, CW complexes, pointed homotopy, and generalized/reduced cohomology theory | 0 | found CW and general homotopy-category infrastructure but no Brown theorem or source-frozen generalized-cohomology target; exit 0 reflects infrastructure matches |

There is no applicable `lake env lean <target>.lean` command: the exact mathematical expression
required by this node has not been source-selected. Elaborating a convenient proxy would not
validate the assigned deliverable.

## Retry condition

An accountable source review must acquire immutable copies of the 1962 article and 1963
correction, hash them, pinpoint the exact selected theorem and all imported definitions, transcribe
its premises and conclusion, and record the correction's effect. It must explicitly decide every
scope choice and boundary case listed above and preserve the boundary with `THM-M-0561` (Omega
spectrum representation). A later statement run can then encode that result, minimize its pinned
imports, fingerprint the explicit elaborated expression, add checked transports, and execute
structural mutation tests.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
