# THM-M-1464 exact-statement gate: blocked

Item: `S56-M-1464-STATEMENT`

Base revision: `1305c30bb297a27f8ce539ca8c0c90dc241aa6c7` (tree
`b77b52bf93cbd1927fd17f0d7f5bcab2eba3ab07`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1464-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt has `accepted: false`, is not
content-addressed, and contains no accepted receipt ID. Its historical validator also expects the
old authoritative intake state `[ ]` and no longer replays after integration changed that state to
`[_]`. Rev-5.6 section 10.2 permits preparation of this later-node blocker, but master closure
remains dependency ordered.

Independently and decisively, the exact-statement gate cannot pass. The complete repository record
is the method-family name "discontinuous Galerkin method", the Reed/Hill attribution and 1973 date,
and the gloss "finite elements allowing discontinuities." It supplies no truth-valued proposition,
formula, bibliography, ordered binder, hypothesis, conclusion, proof boundary, correction, erratum,
or reviewer. Stage0 explicitly leaves the precise definitions and premises open, and rev-5.6 treats
the catalog's verified label as untrusted metadata.

The likely primary source, Reed and Hill's *Triangular Mesh Methods for the Neutron Transport
Equation*, defines a particular two-dimensional discrete-ordinates transport discretization on
regular triangular meshes. It contains construction details and numerical experiments, not one
general theorem selected by the catalog. In particular, the authors say that they have no
theoretical stability result for relevant continuous-weight choices and report discontinuous-method
stability and accuracy experimentally. Several materially inequivalent roots therefore fit the
record:

- formal construction of the Reed-Hill cell equations;
- unisolvence of a fixed local weighted-residual system under specified weights and geometry;
- exact reproduction of one numerical benchmark under fixed arithmetic semantics;
- a later consistency, conservation, stability, convergence, or error theorem for a fixed DG
  scheme; or
- a modern elliptic, hyperbolic, or conservation-law DG theorem unrelated to the Reed-Hill scheme.

The repository selects none of them. It also fixes no PDE, domain, mesh family, broken trial and
test spaces, traces and jumps, numerical flux or penalty, boundary data, regularity, norm, rate,
constant dependencies, arithmetic model, or degenerate cases. Choosing a familiar interior-penalty
or abstract coercivity theorem would invent, narrow, broaden, or substitute proposition-changing
mathematics.

Sections 5 and 5.1 make ambiguity and a missing expression fingerprint hard blockers. There is no
canonical Lean expression whose imports can be minimized, no serialized elaborated expression or
canonical-target environment fingerprint, and no credited alternate transport. Removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined, not passed. No
`Statement.lean`, theorem declaration, proof body, weakened special case, or broadened interface was
added. The provisional root remains `[H5, M4, R4]`.

## Source And Lean Boundary

The intake observed the complete 23-leaf Reed-Hill PDF at SHA-256
`ec04436524f01ad10647398d8d8c81cd21f2b15a69cbcb5d3e9f1f70c22c2d89`. The source is not
vendored or independently admitted as a canonical statement. Its construction and experimental
claims are discovery and scope evidence only, not `H0` or statement identity.

The existing `IntakeProbe.lean` re-elaborates against the pinned environment. Its three direct
imports expose nine adjacent affine-simplex, piecewise-integration, and coercive-bilinear-form
interfaces. All nine checks pass, and three representative imported results report only `propext`,
`Classical.choice`, and `Quot.sound`. None defines a DG mesh, broken polynomial space, trace,
numerical flux, Reed-Hill sweep, stability theorem, or error theorem. Those imports therefore cannot
be certified minimal for an absent canonical target and receive no statement or proof credit.

A bounded exact-topic search over repo-local Lean and pinned mathlib found only the probe's own
Reed-Hill disclaimer and no source-selected DG terminal declaration. This is narrow feasibility
evidence, not the downstream anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1464` | 0 | rank 1141; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| direct reads of the manifest, DAG, blueprint, catalog, Stage0, and complete intake dossier | 0 | intake is `[_]`, statement is `[ ]`, and the canonical human claim, Lean target, imports, expression hash, and canonical environment fingerprint are null |
| `git blame -L 10686,10691 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `python3 -B Stage1_Instances/THM-M-1464/check_intake.py` | 1 | historical intake replay stops because it expects authoritative intake state `[ ]`, while integration records `[_]`; this phase records rather than rewrites stale intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `cd Formalizations/Lean/.lake/packages/mathlib && git rev-parse HEAD 'HEAD^{tree}' && git status --short` | 0 | revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1464/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; stdout SHA-256 `9d65a47407fb9cafa84aa711ae30a950b617a5ba664f95e94a429c554f5d9e99`; no canonical target was declared |
| `rg -n -i --glob '*.lean'` with DG, Reed-Hill, numerical-flux, and broken-space patterns over repo-local Lean, pinned mathlib, and this dossier | 0 | only the owned probe disclaimer matched; no source-selected terminal DG declaration was located |
| prohibited-construct `rg` scan over owned Lean files (exact replayable `argv` is in the structured blocker) | 1, expected no match | no prohibited declaration or placeholder token |

Final JSON parsing, tracked and no-index whitespace checks, and the absent-self-test check are
recorded in the structured blocker beside this report.

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
preserve and hash an immutable primary or approved authoritative source, select and independently
approve one exact truth-valued proposition, and map every incorporated definition, binder, premise,
conclusion, proof boundary, correction, and erratum. The selection must freeze the PDE, coefficients,
domain, mesh, broken spaces, traces and jumps, flux or penalty, boundary data, regularity, norm,
constants and rate, arithmetic and experiment boundary, neighboring-target ownership, and every
degenerate case.

A fresh statement worker can then encode exactly that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof
credit, or master acceptance is claimed.
