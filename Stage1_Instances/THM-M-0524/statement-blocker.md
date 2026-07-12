# Exact-statement gate: blocked

Item: `S56-M-0524-STATEMENT`  
Theorem: `THM-M-0524`  
Base revision: `028e2535b68678b8296e63e2cacb05ed9775a2d8`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record supplies only the label "Shou-Wu Zhang formula", the year 1997, and the gloss "a
higher-dimensional generalization of the Gross-Zagier formula". It supplies no immutable primary
source, theorem or equation number, page, exact formula, definitions, or hypotheses. The intake
correctly treats Zhang's *Heights of Heegner cycles and derivatives of L-series* as an uninspected
discovery candidate rather than as a selected canonical statement.

The gloss does not determine a unique proposition. In particular, it does not fix:

- the modular eigenform or automorphic representation, weight, level, coefficient field, and local
  hypotheses;
- the imaginary quadratic field, discriminant, embedding and Heegner hypotheses, conductors,
  characters, and excluded primes;
- the Kuga-Sato or other ambient variety, cycle codimension and construction, projector,
  homological triviality, and coefficient conventions;
- the height pairing, measures, Petersson norm, completed or incomplete L-function, Euler factors,
  analytic continuation, functional-equation sign, and derivative order;
- the periods, volumes, discriminants, factorials, signs, and other normalization constants; or
- the scalar field of the equality and its boundary behavior when a cycle, height, derivative, or
  normalization factor vanishes.

Each choice changes the target's domains, ordered binders, assumptions, or conclusion. Choosing a
formula from the candidate paper without a source review, using the classical elliptic-curve
Gross-Zagier theorem, or replacing the arithmetic-geometric constructions with arbitrary abstract
functions would invent or substitute mathematics. The repository's `source_status_untrusted`
value `已验证` grants no statement or proof credit.

The canonical claim therefore fails before minimal imports, elaboration, expression hashing,
checked alternate transports, or meaningful removed-hypothesis, changed-domain, binder-scope, and
boundary mutations can be established. No Lean declaration, proxy proposition, assumed formula,
weakened special case, or broadened target was introduced. Lifecycle remains `planned`, root vector
remains `[H3, M4, R4]`, and statement acceptance and theorem completion remain false.

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

Commands ran inside this worker clone. The existing `.lake` symlink to the canonical pinned
artifacts was read only; no update, build, clone, or fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0524` | 0 | Rank 896, lifecycle `planned`, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| `rg -n -i -e '张寿武公式' -e 'Gross-Zagier公式的高维推广' -e 'Heights of Heegner cycles and derivatives of L-series' Docs Stage1_Instances Formalizations --glob '!Stage1_Instances/THM-M-0524/**' --glob '!Docs/Stage1_Blueprint_rev-5.6.md' --glob '!Docs/Stage1_Execution_DAG_rev-5.6.json' --glob '!Docs/Stage1_Targets_rev-5.6.json' --glob '!Docs/Stage1_Blueprint_Applicable_Theorems.md'` | 0 | Found only the underspecified inventory and Stage0 metadata; no source-frozen proposition or Lean target |
| `rg -n -i --glob '*.lean' -e 'Heegner (cycle|cycles)' -e 'Gross.?Zagier' -e 'Kuga.?Sato' -e 'Rankin (L-series|L series)' -e 'height pairing' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | No matching occurrence; no Heegner-cycle formula or required arithmetic-geometric API was located |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_044.lean` | 0 | The legacy elliptic Gross-Zagier interface elaborated; it is a different target and supplies no statement credit |
| `git diff --check -- Stage1_Instances/THM-M-0524` | 0 | No whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | No false worker-completion manifest exists |

There is no applicable `lake env lean <target>.lean` check: the prerequisite exact expression does
not exist. Elaborating a fabricated interface that assumes the desired equality would be false
statement evidence rather than validation of the assigned deliverable.

## Retry condition

An accountable source review must first select an immutable primary-source edition and exact
theorem or equation/page, dispose of errata, and freeze every datum, hypothesis, construction,
normalization, scalar field, and boundary case listed above. It must establish whether the intended
1997 target is the candidate paper's formula and distinguish it from the classical Gross-Zagier
theorem and later generalizations. A later statement run can then crosswalk the source row by row,
encode the actual arithmetic-geometric objects, minimize pinned imports, elaborate and fingerprint
the expression, check alternate forms, and run the required mutations.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
