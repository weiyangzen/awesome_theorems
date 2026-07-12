# Exact-statement gate: blocked

Item: `S56-M-1139-STATEMENT`  
Theorem: `THM-M-1139`  
Base revision: `6bf36d02b85429a55c272e015740031c598c25bb`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The only theorem-specific wording is the title "Hopf lemma" and the gloss "the sign of the
derivative at the boundary." The record names Eberhard Hopf and 1952, but supplies no work,
edition, theorem number, page, exact statement, or definitions. The intake therefore correctly
left the canonical formal target open.

The label and gloss do not determine a unique proposition. In particular, they do not fix:

- the harmonic special case or a general second-order elliptic operator and its coefficient,
  ellipticity, and zeroth-order hypotheses;
- the dimension, domain representation, connectedness, and boundary regularity;
- the interior sphere condition and its exact tangent-ball witnesses;
- a maximum or minimum formulation, local or global extremum, and the required strictness;
- inward or outward normal orientation;
- a classical boundary directional derivative or a one-sided liminf quotient; or
- the solution regularity and whether the constant case is excluded by hypothesis or conclusion.

Each choice changes binders, hypotheses, or the conclusion. Selecting a familiar textbook
variant, combining variants, or replacing the PDE result with an abstract implication would
broaden or substitute the unknown source theorem. Consequently there is no canonical expression
whose imports can be minimized, no elaborated-expression fingerprint, no checked alternate
transport, and no meaningful removed-hypothesis, changed-domain, binder-scope, or boundary-case
mutation suite. No Lean declaration, axiom, placeholder, or assumed Hopf predicate was introduced.
Machine state remains `M4`; statement acceptance and theorem completion are false.

## Pinned environment and search

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Commands ran inside this worker clone. The existing `.lake` artifacts were read only; no update,
build, clone, or fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1139` | 0 | Rank 344, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search recorded below | 0 | Found only the underspecified metadata; no source-frozen proposition |
| pinned-mathlib `rg` search recorded below | 0 | Found unrelated Hopf-algebra/topology APIs and divergence-theorem prose; no elliptic Hopf boundary-point theorem or exact target |
| `git diff --check -- Stage1_Instances/THM-M-1139` | 0 | No whitespace errors |

The exact repository search was:

```bash
rg -n -i -C 3 \
  'Hopf引理|Hopf lemma|Hopf boundary|boundary point lemma|边界上的导数符号' \
  Docs Stage1_Instances Formalizations \
  --glob '!Stage1_Instances/THM-M-1139/**' \
  --glob '!Docs/Stage1_Execution_DAG_rev-5.6.json' \
  --glob '!Docs/Stage1_Blueprint_rev-5.6.md' \
  --glob '!Docs/Stage1_Targets_rev-5.6.json' \
  --glob '!Docs/Stage1_Blueprint_Applicable_Theorems.md'
```

The exact pinned-mathlib search, run from
`Formalizations/Lean/.lake/packages/mathlib`, was:

```bash
rg -n -i \
  'Hopf|boundary point lemma|interior sphere|interior ball condition|normal derivative' \
  Mathlib --glob '*.lean'
```

There is no applicable `lake env lean <target>.lean` check: the canonical human claim fails before
a Lean expression exists. Elaborating a chosen textbook variant or a structure that assumes the
desired conclusion would be fake statement evidence rather than the assigned deliverable.

## Retry condition

An accountable source review must select an immutable primary edition and exact theorem/page,
resolve errata, and freeze every operator, domain, geometry, regularity, extremum, normal, and
derivative convention listed above. It must crosswalk those choices premise by premise and verify
the 1952 attribution. A later statement run can then encode that exact result, determine genuinely
minimal pinned imports, preserve its elaborated expression and environment fingerprint, check all
credited transports, and execute the four required mutation classes.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
