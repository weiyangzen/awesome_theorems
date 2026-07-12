# Exact-statement gate: blocked

Item: `S56-M-0730-STATEMENT`  
Theorem: `THM-M-0730`  
Base revision: `f12b1ccbda307337d488a2993eddbf883b722be6`

## Decision

No exact Lean 4 target can yet be selected without substituting one of several inequivalent results.
The repository's complete claim is the title `PCP定理的更强形式` ("stronger form of the PCP
theorem"), attributed to Irit Dinur in 2007, plus the gloss `PCP的组合证明` ("a combinatorial proof
of PCP"). The gloss describes a proof method rather than a proposition, while "stronger" does not
identify which strengthened result or parameter profile is intended.

The statement phase inspected a primary-source candidate rather than guessing from the title: Irit
Dinur, *The PCP Theorem by Gap Amplification*, ECCC TR05-046, dated 2005-04-16, the prepublication
version of the 2007 JACM article (DOI `10.1145/1236457.1236459`). The downloaded 22-page PDF had
SHA-256 `4e568c44155e4ca7ad141afc609c04ac7dd9a8608f2df4f4c38191e9f6cf21dd`.
That source does not resolve the repository ambiguity. It contains at least these materially
different candidate roots:

1. Theorem 4.1, a polynomial-time, linear-size constraint-graph transformation that preserves
   satisfiability and raises the unsatisfiability gap to `min (2 * gap(G)) alpha`, for constants
   depending on a constant-size alphabet.
2. Corollary 4.2, the ordinary PCP consequence that Gap-3SAT is NP-hard, alternatively
   `SAT in PCP_{1/2,1}[O(log n), O(1)]`.
3. Theorem 7.1, the stronger short-PCP parameter result
   `SAT in PCP_{1/2,1}[log_2(n * polylog n), O(1)]`.
4. The abstract's assignment-testers/PCPs-of-proximity extension, described as "slightly stronger
   objects than PCPs" and distinct from all three claims above.

These candidates quantify different objects and prove different conclusions. Selecting Corollary
4.2 merely because the gloss says "proof of PCP" would discard "stronger" and silently substitute
the ordinary PCP theorem. Selecting Theorem 7.1 merely because it has stronger parameters would
discard the gloss's focus on the combinatorial proof. Selecting Theorem 4.1 or the assignment-tester
extension would instead make an internal transformation or stronger proof object the root. The
repository supplies no crosswalk that decides among them.

Consequently the rev-5.6 section 5.1 gate stops before encoding. There is no canonical human claim,
so no faithful ordered binders, hypotheses, boundary conventions, normalized kernel expression,
or expression hash can be produced. A Lean declaration introduced at this point would encode a
worker-selected replacement, even if it elaborated. For the same reason, removed-hypothesis,
changed-domain, binder-scope, and boundary mutations would test that replacement rather than the
repository theorem. No `Statement.lean`, statement receipt, or proof credit is emitted.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated using the pinned environment. It checks only
general finite simple-graph, finite-set, and rational APIs. Those APIs neither define constraint
graphs with edge predicates nor formalize polynomial-time reductions, NP-hardness, PCP verifiers,
assignment testers, or the source's parameter conventions. The successful probe establishes that
the Lean installation is usable; it is not a canonical target.

Lean was `4.29.0` at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib was pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Existing `.lake` artifacts were used read-only. No
update, build, fetch, clone, or dependency mutation was run.

## Validation evidence

Commands ran on 2026-07-12 (`Asia/Shanghai`) in this worker clone.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0730` | 0 | rank 767, planned, legacy artifacts unaccepted, theorem incomplete |
| `curl -L --fail --max-time 30 https://www.wisdom.weizmann.ac.il/~dinuri/mypapers/PCP.pdf` | 56 | connection reset; no artifact was accepted from this failed retrieval |
| `curl -L --fail --max-time 30 https://eccc.weizmann.ac.il/report/2005/046/download -o /tmp/dinur-pcp.pdf` | 0 | retrieved the 22-page ECCC TR05-046 PDF |
| `sha256sum /tmp/dinur-pcp.pdf` | 0 | source snapshot hash `4e568c...21dd` |
| `pdftotext -layout /tmp/dinur-pcp.pdf /tmp/dinur-pcp.txt` and scoped `rg`/`sed` inspection | 0 | located Theorem 4.1, Corollary 4.2, Theorem 7.1, and the stronger-object language in the abstract |
| `curl -L --fail --max-time 30 https://api.crossref.org/works/10.1145/1236457.1236459` | 0 | confirmed the 2007 JACM bibliographic record and abstract; this mutable service response is discovery evidence only |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | pinned Lean version and commit above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0730/IntakeProbe.lean)` | 0 | seven general encoding API checks elaborated; no theorem target asserted |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0730 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |
| `python3 -m json.tool Stage1_Instances/THM-M-0730/instance.json` | 0 | valid intake JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0730/task-dag.json` | 0 | valid task-DAG JSON |

## Retry condition and boundary

An accountable source decision must select one exact result and immutable edition, then freeze all
incorporated definitions, complexity model and encodings, asymptotic conventions, constant
dependencies, ordered quantifiers, hypotheses, conclusion, and degenerate cases. An independent
source review must confirm that selection against the repository label. Only then can the exact
Lean target and minimal imports be chosen and all four required mutation classes be run.

Verdict: `blocked`. The statement node remains `[ ]`; lifecycle remains `planned`; the root remains
`[H3, M4, R4]`; `audit_complete` and `theorem_complete` remain false. This assigned phase is not
genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
