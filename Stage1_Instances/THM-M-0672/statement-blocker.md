# Exact-statement gate: blocked

Item: `S56-M-0672-STATEMENT`

Theorem: `THM-M-0672`

Base revision: `20b8abf35019d24fc944d56d6af62cb098711ee3`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is the title `模型配方法` and the gloss `非标准分析的基础`, attributed to
Abraham Robinson in 1966. The accepted intake correctly preserves a contradiction in the discovery
metadata rather than resolving it by guesswork: the title suggests a model-companion or
model-completion method, while the gloss and date suggest Robinson's nonstandard-analysis program.
Neither phrase identifies one proposition.

The plausible readings are inequivalent. A model-companion result would need a first-order
language, theories, equality of universal consequences or an embedding characterization, and a
precise model-completeness conclusion. A nonstandard-analysis foundation could instead mean
transfer, an ultrapower construction, an elementary extension, or a saturation/enlargement result.
They have different domains, ordered binders, hypotheses, conclusions, and boundary cases.
Selecting any familiar version would invent or substitute mathematics, including substitution of
the separately scheduled model-completeness and Los-theorem targets.

The bibliographic lead, Robinson's *Non-standard Analysis* (1966), is only a discovery candidate:
the repository supplies no edition, chapter, theorem, page, wording, incorporated definitions, or
errata disposition. It also supplies no source that connects the Chinese title to a particular
model-companion theorem. Thus the canonical human claim fails before minimal imports, an elaborated
expression hash, checked transports, or meaningful removed-hypothesis, changed-domain,
binder-scope, and boundary mutations can be established. An opaque predicate or structure field
assuming one candidate conclusion would be a placeholder and is not permitted. Machine debt
remains `M4`; no statement, proof, audit, or theorem-completion credit is claimed.

## Lean boundary

The pinned environment contains concrete neighboring APIs in
`Mathlib.ModelTheory.ElementaryMaps`, `Mathlib.ModelTheory.Ultraproducts`, and
`Mathlib.Analysis.Real.Hyperreal`. The search found no declaration described as a model companion or
model completion. The presence of elementary embeddings, Los's theorem, and hyperreals does not
select the intended proposition, so these APIs receive no statement or proof credit. There is no
applicable `lake env lean <canonical-target>.lean` command because a canonical target does not yet
exist.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The existing canonical `.lake` artifacts were read
only; no update, build, clone, fetch, or dependency mutation was run.

## Validation record

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0672` | 0 | rank 716, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8a...1d2` and `321626...2d81`, recorded in the JSON blocker |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| repository `rg` search for the Chinese title, gloss, model companions/completions, and nonstandard analysis | 0 | only the underspecified source metadata was found outside the target dossier; no exact proposition |
| pinned-mathlib `rg` search for model companions/completions, nonstandard analysis, elementary embeddings, ultraproducts, and Los's theorem | 0 | neighboring elementary-map, ultraproduct, Los, and hyperreal APIs found; no companion/completion declaration and no source-specific root |

## Retry condition

An accountable reviewer must preserve and hash an immutable primary source, select and transcribe
one exact theorem with all incorporated definitions and assumptions, resolve the title/gloss
mismatch, dispose of errata, and independently approve the source crosswalk. A later statement
worker can then encode that same claim, minimize pinned imports, serialize and hash the elaborated
expression, check alternate transports, and run all four required mutation classes.

This is the first failed gate, not completion of the statement node or any later node. The assigned
phase is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
