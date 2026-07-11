# Statement gate blocker

Item: `S56-M-1172-STATEMENT`  
Theorem: `THM-M-1172`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The accepted intake deliberately freezes only a family of second-order uniformly elliptic
`W^{2,p}` regularity results. The repository source record supplies the title `W^{2,p}` regularity
and the gloss "solutions have second derivatives in `L^p`", but no primary-source theorem or page.
That information does not choose among mathematically different statements, including:

- an interior estimate versus a global Dirichlet estimate;
- divergence versus nondivergence form, and scalar equations versus systems;
- constant, continuous, VMO, or other coefficient hypotheses;
- weak versus strong solutions and local versus global `W^{2,p}` membership;
- the dimension, range of `p`, domain/boundary regularity, boundary data, lower-order terms, and
  precise norm estimate (including the dependencies of its constant).

Choosing these binders and hypotheses here would synthesize a convenient elliptic regularity
theorem rather than elaborate the exact source claim. The two candidate books in the intake
crosswalk are discovery anchors only: neither has an inspected edition/theorem/page and complete
assumption mapping. The untrusted source label `已验证` supplies no missing mathematical content.
Section 5 and section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` make statement ambiguity and a
missing exact expression fingerprint hard blockers.

The historical discovery module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_147.lean` does not repair the source gap. Its
`W2pRegularityData` takes `weakEquation`, `ellipticityHypotheses`, and `boundaryHypotheses` as
arbitrary propositions and takes both the second-derivative `MemLp` conclusion and the desired
estimate as input fields. Its `StatementShape` is only nonemptiness of that supplied data. It uses
classical Frechet derivatives rather than a checked weak-second-derivative Sobolev model. Thus it
cannot be the exact PDE theorem and receives no statement or proof credit, although it elaborates.

Consequently there is no source-faithful Lean expression for which minimal imports, ordered
binders, normalized kernel expression, checked alternate transports, or removed-hypothesis,
changed-domain, binder-scope, and boundary-case mutations can truthfully be recorded. Machine debt
remains `M4`. No `sorry`, axiom, proxy predicate, placeholder declaration, or substituted special
case was introduced.

## Environment fingerprint

- Repository base revision: `b614452f9bb46017d5423ccca0a5c196ba91be22`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Historical discovery module SHA-256:
  `14738b9384aaef6efe3e9d4970a496a81604de64d8098f5901153fb981d2e0f3`.

## Narrow validation evidence

Commands ran from this worker clone using only the existing canonical pinned `.lake` artifacts.
No update, build, fetch, or clone command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1172` | 0 | Rank 147, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_147.lean` | 0 | Historical abstract statement-shape and infrastructure module elaborated with no output; this is not exact-statement evidence |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Checked mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| pinned-mathlib `rg` search for `W2p`, `W^{2,p}`, `WeakDerivative`, Calderon-Zygmund, elliptic regularity, and second-derivative/`MemLp` combinations | 1 | No matching Lean source declaration; exit 1 means no matches |

## Retry condition

An accountable source reviewer must select and inspect one immutable primary-source theorem and
record its edition, theorem/page, exact wording, referenced definitions, all assumptions, constant
dependencies, and errata status. That decision must freeze the operator form, coefficient and
ellipticity model, solution notion, domain and boundary conditions, exponent range, locality, and
exact membership/estimate conclusion. A later statement worker can then encode that claim with
minimal pinned imports and run the four required mutation classes.

Until then, statement acceptance, audit completion, and theorem completion are false. Because the
assigned phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json` is emitted.
