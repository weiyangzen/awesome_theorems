# Exact-statement gate: blocked

Item: `S56-M-1112-STATEMENT`  
Theorem: `THM-M-1112`  
Base revision: `2734644ab66534a403c2062af16eda4fb799e018`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record gives only the title "random graph", the gloss "Erdos-Renyi random graph model", the year
1959, and the authors Erdos/Renyi. It supplies no theorem number, page, exact statement,
quantifiers, hypotheses, or conclusion. The accepted intake therefore correctly leaves the model
variant and theorem-level consequence open.

The wording does not determine even the probability law. Erdos and Renyi's 1959 paper studies the
uniform fixed-edge model `G(n, m)`, while the independent-edge model `G(n, p)` is associated with
Gilbert's 1959 paper and is also commonly called the Erdos-Renyi model. These choices are not
definitionally or propositionally interchangeable without a separately selected theorem and
transport. The repository record also does not fix labelled versus unlabelled graphs, the vertex
type, parameter ranges, or whether the conclusion is a mass formula, uniformity, independence,
coupling, or an asymptotic graph property.

Pinned mathlib contains the nearby module
`Mathlib.Probability.Combinatorics.BinomialRandomGraph.Defs`. It defines the independent-edge law
`SimpleGraph.binomialRandom` and proves probability-measure, endpoint, and singleton-mass lemmas.
The module explicitly notes that Erdos and Renyi introduced a different model. This is useful
future anchor evidence, but selecting one of those declarations as the root would substitute a
specific `G(n, p)` result for the repository's unresolved model-family label. It cannot resolve the
statement gate.

Consequently there is no canonical human theorem to map to an expression, no honest minimal-import
claim, no elaborated-expression fingerprint, and no meaningful removed-hypothesis, changed-domain,
binder-scope, or boundary mutation suite. No Lean declaration, axiom, placeholder, assumed
distributional property, broadened family assertion, or weakened special case was introduced.
Machine state remains `M4`; statement acceptance and theorem completion are false.

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

Commands ran inside this worker clone. The canonical `.lake` artifacts were read through the
existing worker link; no update, build, clone, or fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1112` | 0 | Rank 552, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C /home/sansha-2/external/awesome_theorems/Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for the title, model name, primary-paper titles, and random-graph phrases | 0 | Found underspecified metadata, the intake citations, a duplicate underspecified target, and an unrelated Erdos-Renyi probability lemma; no source-frozen proposition for this target |
| pinned-mathlib `rg` search for random graphs and Erdos-Renyi terminology | 0 | Found `BinomialRandomGraph/Defs.lean`, whose `G(V,p)` model does not select the unresolved target claim |
| `git diff --check -- Stage1_Instances/THM-M-1112` | 0 | No whitespace errors |

There is no applicable `lake env lean <target>.lean` validation because an exact proposition does
not exist. Elaborating mathlib's available `G(V, p)` definition or one of its endpoint/mass lemmas
would validate a substituted statement, not the assigned theorem.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact
theorem/page, dispose of errata, and freeze `G(n, m)` versus `G(n, p)`, graph labelling, parameter
ranges, every ordered binder and hypothesis, the conclusion, and all boundary cases. It must also
separate this target from `THM-M-0848` (another underspecified Erdos-Renyi random-graph record) and
the scheduled phase-transition, giant-component, connectivity-threshold, and Hamiltonicity
targets. A later statement run can then encode the selected claim, minimize imports, fingerprint
the elaboration, crosswalk it row by row, and run the required structural mutations.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
