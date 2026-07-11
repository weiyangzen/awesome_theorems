# THM-M-0393 Anchor Audit

## Audit Boundary

This artifact audits `S56-M-0393-ANCHOR_AUDIT` against the exact statement
`Stage1.THM_M_0393.ThueStatement`. A usable terminal candidate must prove finiteness of the ordered
integer solution pairs of `F(x,y) = m` for a rationally irreducible homogeneous integral binary
form of degree at least three and nonzero `m`. Definitions, approximation infrastructure, finite
special cases, differently scoped legacy predicates, documentation rows, and declarations with
placeholders receive no root proof credit.

The repository base is `922250ad97c8d0b19b95c52f442aa2bf25be4f79`. The reused canonical Lake
manifest pins mathlib4 at `8a178386ffc0f5fef0b77738bb5449d50efeea95`; the checked-out mathlib HEAD
matches that revision. No dependency was updated, built, cloned, or fetched into `.lake`.

## Candidate Ledger

| Candidate | Immutable revision | Exact location | Classification and decision |
|---|---|---|---|
| Repo-local canonical target | repository base above | `Stage1_Instances/THM-M-0393/Statement.lean`, `Stage1.THM_M_0393.ThueStatement` | Exact statement interface, elaborated below; it is a `def : Prop`, not a theorem body. `M3`, no proof credit. |
| Legacy Stage1 artifact | repository base above | `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_006.lean`, `AwesomeTheorems.Stage1.S1_M_006.StatementShape` | Statement-only declaration with proposition-valued hypotheses and unrestricted right side. Its own source says it is not a proof. It is not the rev-5.6 canonical target and legacy evidence is ineligible. `M3`, rejected as a terminal anchor. |
| mathlib documentation row | `leanprover-community/mathlib4@8a178386ffc0f5fef0b77738bb5449d50efeea95` | `docs/1000.yaml`, `Q2378270` | The row is titled `Thue's theorem` but has no `decl`/`decls` field. It is a wish-list entry, not Lean proof evidence. Rejected. |
| mathlib object-model support | same mathlib revision | `Mathlib.RingTheory.MvPolynomial.Homogeneous`, `MvPolynomial.IsHomogeneous` and associated API | Supports the frozen statement. Full pinned-source searches found no `Thue`/`ThueEquation` declaration and no theorem about finiteness of binary-form fibers. `M3` substrate only, not a root proof. |
| Nearby mathlib number theory | same mathlib revision | `Mathlib.NumberTheory.Transcendental.Liouville.LiouvilleWith`; `Mathlib.NumberTheory.Height.MvPolynomial`; `Mathlib.RingTheory.Polynomial.Resultant.Basic` | Approximation, height, and resultant infrastructure may be useful in a future proof architecture, but none has the canonical conclusion. No wrapper from these declarations closes the root. |
| Formal Conjectures | `google-deepmind/formal-conjectures@b2e608fc52d765510915a244bb69b1a2741acc3c` | complete 1,204-entry tree; sole `Thue` text is a bibliography reference in `FormalConjectures/ErdosProblems/829.lean:112` | The immutable archive has no Thue-equation finiteness statement or proof. The nearby Stewart declaration concerns a lower bound for sums of cubes and contains `sorry`; it is neither a candidate nor evidence. Nothing can be integrated. |

Formal Conjectures uses Lean `v4.27.0` and mathlib `v4.27.0`. Its immutable archive SHA-256 is
`e67c2bfe909872e41a64e896837cfa6f0fb0f8ca14b0f7911aa14e4ae29294d3`; its complete GitHub tree
response SHA-256 is `76fa3f96fc2ff7fc85addfd1e85852dae3fcb5022fc1ef35b030a3dc1e3efc61`
and reports `truncated: false`. These external bytes were inspected under `/tmp`; they were not
installed or placed in the dependency closure.

## Discovery Ledger

On 2026-07-12 the searches used the aliases `Thue`, `ThueEquation`, `Thue equation`, `Thue
theorem`, `binary form`, and finiteness/Diophantine combinations, in this order: repo-local Lean,
pinned mathlib and every pinned dependency, mathlib documentation, Loogle, then the immutable
Formal Conjectures tree and archive. Loogle returned zero declaration-name hits for `Thue`,
`ThueEquation`, and `binary form`; response hashes were respectively
`200ecb6f5aa2a6b84e7ba4eb45b66ceecce7a38d5c7c31ac8d41fd62862d32d7`,
`3c8eb924fc67191e5bbc5487feefe42b0c1c9dff205105f94b574751d9e9599f`, and
`6f7de716e966cbfc28f9d715b7217ca6df492cfdbc16d26b91aa796c3f920198`.

Access limitations are explicit: unauthenticated GitHub code search returned HTTP 401 and
grep.app returned HTTP 429. Consequently this is a classified, replayable audit of the pinned
closure and the identified credible public Lean 4 project, not a claim that all public source code
has been exhaustively searched. The immutable negative inventories and Loogle queries compensate
for those unavailable discovery surfaces sufficiently for this node, but do not establish reviewed
global saturation.

## Validation Evidence

Run from repository root unless a `cwd` is stated:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups; 1546 uniform-L0 Lean 4 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0393
  exit 0: execution rank 6; lifecycle planned; theorem_complete=false
git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD
  exit 0: 8a178386ffc0f5fef0b77738bb5449d50efeea95
rg -n -i 'thue|thueequation|thue equation|binary form|diophantine.*finite|finite.*diophantine' \
  Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_006.lean \
  Formalizations/Lean/.lake/packages -g '*.lean' -g '*.md' -g '*.yaml'
  exit 0: only the legacy open audit, mathlib documentation rows, approximation prose, and a
  resultant comment matched; no terminal declaration matched
rg -n -i 'thue|binary form|thue equation' /tmp/thm393-formal-conjectures-src \
  -g '*.lean' -g '*.md' -g '*.yaml'
  exit 0: one bibliographic mention of "Cubic Thue equations" in ErdosProblems/829.lean
cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0393/Statement.lean
  exit 1: the reused canonical cache has no `Mathlib.olean` module root; per worker policy this
  audit did not build or otherwise mutate `.lake`
python3 -m json.tool Stage1_Instances/THM-M-0393/anchor-audit.json >/dev/null
  exit 0
git diff --check -- Stage1_Instances/THM-M-0393 .stage1-worker-selftest.json
  exit 0: no output
```

## Verdict And Debt Boundary

All four candidates in inventory `thm-m-0393-anchor-inventory-2026-07-12-v1` are classified. No
exact terminal proof body was found. The root therefore remains `M4` (full formalization debt), and
there is no `M1` repo-local integration task to create: importing the statement-only or unrelated
candidates cannot improve assurance. The anchor-audit phase is self-tested, but `audit_complete`
and `theorem_complete` both remain false. The next phase must freeze a genuine obligation tree;
eventual completion requires a local proof or a future immutable exact external proof plus all
validation and release gates. Master acceptance is still pending.

The missing `Mathlib.olean` prevents a fresh Lean replay in this worker and is retained as a known
validation failure. It does not turn any inspected source candidate into a proof and does not block
the negative source/provenance inventory itself. Statement acceptance and all later kernel gates
must retain their own evidence boundary.
