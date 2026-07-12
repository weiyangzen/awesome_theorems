# Exact-statement gate: blocked

Item: `S56-M-1267-STATEMENT`  
Theorem: `THM-M-1267`  
Base revision: `50fa1bbf0f067f9f3ad127ab97d86d255c928a2b`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
entire mathematical wording is the title `下半连续性` ("lower semicontinuity") and the gloss
`泛函的下半连续性` ("lower semicontinuity of functionals"). The record identifies no primary
source, edition, theorem/page, functional, or proposition. Its `已验证` label is explicitly
untrusted metadata and supplies neither source nor kernel evidence.

The wording does not determine the choices required to identify one theorem:

- the domain space, its topology, and whether convergence is topological, sequential, strong, or
  another mode;
- the codomain (`Real`, `EReal`, `ENNReal`, or another ordered space) and infinity conventions;
- the functional itself and its effective domain;
- whether lower semicontinuity is a premise, a conclusion, or merely the named definition;
- the hypotheses that would establish the property, such as convexity, measurability, growth,
  coercivity, or an integral representation;
- the intended characterization (neighborhood/filter, liminf, closed sublevels, or epigraph) and
  the assumptions under which alternate formulations are equivalent.

These choices produce inequivalent propositions. In particular, selecting mathlib's generic
`LowerSemicontinuous` predicate would turn a property name into a theorem target, while selecting a
closed-sublevel characterization or a variational-integral theorem would substitute mathematics
not present in the source. Weak lower semicontinuity of convex functionals is separately listed as
`THM-M-1268` and is not a permissible interpretation of this item.

The pinned mathlib tree contains the definition and many unrelated theorems using
`LowerSemicontinuous`, notably in `Mathlib.Topology.Semicontinuity.Defs` and convex-analysis
modules. Their availability does not disambiguate the source claim. No legacy slot or repo-local
Lean module is assigned to `THM-M-1267`.

Consequently the canonical human-claim identity gate fails before minimal imports, a canonical
Lean declaration, normalized expression hash, checked alternate transports, or meaningful
removed-hypothesis/domain/binder-scope/boundary mutations can be produced. Introducing an abstract
functional plus an assumption that it is lower semicontinuous would be circular, not an exact
elaboration. Machine debt remains `M4`; no statement receipt, downstream-node credit, audit
completion, or theorem completion is claimed.

## Required unblock

An accountable source reviewer must identify an immutable primary source by edition and exact
theorem/page, check relevant errata, and freeze the domain, topology or convergence mode, codomain,
functional, every hypothesis, exact conclusion, and degenerate cases. A later statement worker can
then transcribe that proposition without substitution, minimize its pinned imports, serialize its
elaborated expression and environment, and run all four required mutation classes.

## Narrow validation evidence

Commands ran inside this worker clone on 2026-07-12. The existing pinned Lake environment was used
read-only; no update, build, clone, fetch, or other `.lake` mutation was performed.

- Lean toolchain: Lean `4.29.0`, commit
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
| `python3 scripts/stage1_target.py show THM-M-1267` | 0 | rank 443; planned; no accepted legacy artifact; theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision above |
| `sed -n '9255,9278p' Docs/researches/math_theorems.md` | 0 | confirmed that the source record contains only the title, broad attribution/date, property gloss, importance, and untrusted status |
| `rg -n 'def LowerSemicontinuous\|class LowerSemicontinuous\|LowerSemicontinuous' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Topology Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis --glob '*.lean' \| head -80` | 0 | found the generic definition and multiple distinct uses; none identifies the unspecified source theorem |

First failed gate: exact source-statement identity. The assigned phase is not genuinely self-tested
to its completion gate, so no `.stage1-worker-selftest.json` is emitted.
