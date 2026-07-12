# Exact-statement gate: blocked

Item: `S56-M-1236-STATEMENT`  
Theorem: `THM-M-1236`  
Base revision: `854537bcbb10ad4c68b5a61f06171fffcec64961`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The complete source statement in `Docs/Stage0_Blueprint.md` is `广义函数空间`
("generalized-function space") under the catalog name `Sobolev空间` ("Sobolev space"). This is a
concept or parameterized family of definitions, not a truth-valued proposition. It supplies no
conclusion to elaborate. The accepted intake consequently records `canonical_statement: null` and
leaves the formal module and expression unset.

An exact Sobolev-space theorem would at minimum have to select:

- a theorem about the space, such as completeness, Hilbert structure, density, or another property;
- the ambient domain and its regularity, dimension, scalar field, and measure;
- the derivative order, exponent, weak-derivative convention, and norm or quotient model;
- all hypotheses, ordered binders, endpoints, and degenerate cases.

These choices produce inequivalent propositions. In particular, selecting completeness or the
Hilbert-space result at exponent two would invent a claim absent from the source. Substituting a
Sobolev embedding, compact embedding, or Poincare inequality is also forbidden because those are
separate catalog targets (`THM-M-1237`, `THM-M-1238`, and `THM-M-1239`). The metadata value
`已验证` is expressly untrusted and cannot supply statement identity.

Rev-5.6 section 5 treats statement ambiguity and a missing elaborated-expression fingerprint as
hard blockers. Section 5.1 additionally requires meaningful removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations. With no proposition, there is no faithful Lean
expression, minimal import set, normalized expression hash, alternate-form wrapper, or mutation
fixture to check. Creating an arbitrary `Prop` merely to make Lean elaborate would be a broadened
or substituted theorem and is not admissible evidence.

## Required unblock

An accountable source reviewer must amend the target by selecting one exact proposition and a
pinpointed primary source (edition, theorem/page, referenced definitions, and errata). The amendment
must freeze every domain and parameter above plus the foundation profile and boundary cases. A
later statement worker can then encode that exact claim, minimize pinned imports, serialize and
hash the elaborated expression and environment, compile any credited transports, and run all four
required mutation classes.

## Narrow validation evidence

Commands ran in this worker clone on 2026-07-12. The existing pinned Lake artifacts were only read;
no update, build, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1236` | 0 | rank 419, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C /home/sansha-2/external/awesome_theorems/Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Stage1_Instances/THM-M-1236/intake.json` | 0 | hashes `651c8acc...b1d2`, `321626c8...2d81`, and `4ad9b200...edcd` |

Known failures are exact human-claim identity, a canonical Lean target, minimal-import
determination, expression/environment fingerprints, checked transports, and meaningful mutation
tests. The assigned phase is therefore not genuinely self-tested or complete, and no
`.stage1-worker-selftest.json` is emitted. No downstream-node or theorem-completion credit is
claimed.
