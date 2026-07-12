# Exact-statement gate: blocked

Item: `S56-M-1238-STATEMENT`  
Theorem: `THM-M-1238`  
Base revision: `424122d5aeb369ee90f995e9ffad0583c8b90492`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The repository source record says only `Sobolev空间的紧嵌入` ("compact embedding of Sobolev
spaces") under the name Rellich-Kondrachov. This identifies a theorem family, not one proposition.
The intake deliberately leaves the primary source, exact domain regularity, endpoint conventions,
and formal encoding open. In particular, it does not determine:

- the Sobolev order, scalar field, ambient dimension, or whether the domain is open/connected;
- whether the domain is Lipschitz, an extension domain, has a cone property, or satisfies another
  regularity hypothesis;
- the exact ranges of `p` and `q`, including `p = 1`, `p = n`, `p > n`, `q = 1`, and `q = infinity`;
- whether the source space is `W^{1,p}`, `W_0^{1,p}`, or a higher-order Sobolev space;
- whether compactness is stated as a compact operator, relative compactness of bounded images, or
  a bounded-sequence/subsequence principle.

These choices yield materially different theorems. The three source candidates in
`source-statement-crosswalk.md` are discovery anchors only: no stable edition plus theorem/page and
referenced definitions has been selected or inspected. Choosing one formulation here would invent
missing mathematics or silently substitute a special case. The metadata label `已验证` supplies no
statement identity or kernel evidence.

Rev-5.6 sections 0.1 and 5 make unresolved statement identity a hard stop. Without an exact human
claim, this phase cannot truthfully freeze ordered binders, hypotheses, excluded boundary cases,
checked alternate encodings, or the required hypothesis/domain/binder/boundary mutations. A Lean
expression fingerprint for an arbitrary proxy would not repair that failure.

## Legacy Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_176.lean` was inspected and elaborated only as
legacy discovery input. Its `RellichKondrachovData` contains four unconstrained proposition fields
(`sourceSobolevModel`, `targetLpModel`, `domainRegularity`, and `exponentHypotheses`) and then stores
the desired compact embedding as a field. Consequently its `StatementShape` is merely nonemptiness
of a package that already assumes the conclusion. It does not define a Sobolev space, an `L^q`
inclusion, a regular Euclidean domain, or the subcritical exponent range, and is not an exact
encoding of any pinpointed Rellich-Kondrachov theorem.

The legacy file's checked Gagliardo-Nirenberg-Sobolev wrappers are continuous norm estimates for
compactly supported smooth functions, not compact Sobolev embeddings. Successful elaboration of
that file therefore establishes only that its abstract interface and wrappers typecheck in the
pinned environment. It supplies no rev-5.6 statement acceptance or theorem proof credit.

## Required unblock

An accountable source reviewer must select an immutable primary source by edition, theorem/page,
exact wording, referenced definitions, and errata. The selection must fix the Sobolev order and
model, scalar and measure conventions, ambient dimension, domain and boundary hypotheses, complete
`p`/`q` range, endpoints, inclusion map, compactness formulation, and all degenerate cases. A later
statement worker can then encode that exact claim (or record a precise missing mathlib interface),
minimize pinned imports, print and hash the elaborated expression, check all credited transports,
and perform the four required structural mutations.

## Narrow validation evidence

Commands ran in this worker clone on 2026-07-12. Lean used the existing pinned `.lake` artifacts;
no Lake update, build, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1238` | 0 | rank 176, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_176.lean` | 0 | no output; legacy abstract boundary and local estimate wrappers elaborated only |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | checked mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_176.lean` | 0 | hashes `651c8acc...b1d2`, `321626c8...2d81`, and `667fce20...f05c` |

Known failures are exact source-statement identity, a canonical Lean target, minimal-import
determination, expression fingerprint, checked transports, and meaningful mutation tests. The
assigned phase is therefore not genuinely self-tested or complete, and no
`.stage1-worker-selftest.json` is emitted. No downstream-node or theorem-completion credit is
claimed.
