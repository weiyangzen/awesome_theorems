# Lean anchor audit

Item: `S56-M-0711-ANCHOR_AUDIT`. Audit date: 2026-07-12. Repository base:
`136ebf643dcdcbc42cef34e415177189578060ef`. The frozen target is
`Stage1.THM_M_0711.NovikovBooneTarget` in `Statement.lean`.

## Result

No exact or transport-ready Lean 4 proof of the frozen Novikov-Boone target was found. The pinned
mathlib supplies the group-presentation representation and a terminal halting-problem theorem, but
it supplies neither a group word-problem undecidability declaration nor a reduction from halting to
that problem. The external projects inspected below formalize adjacent undecidability results, not
the construction of a finitely presented group required by the target. This is a completed negative
anchor audit, not theorem closure: the root remains `[H1, M4, R4]`.

## Pinned local inventory

The canonical manifest pins mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (Lean `v4.29.0`, Lean commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`). A case-insensitive search of every Lean source in
`Mathlib/` found zero files matching `Novikov|Boone` and zero matching
`word[ _-]?problem|wordProblem`. The same terminal-name search found zero files in each other
manifest-pinned package (`Cli`, `LeanSearchClient`, `Qq`, `aesop`, `batteries`, `checkdecls`,
`flt-regular`, `importGraph`, `plausible`, and `proofwidgets`).

| Candidate | Immutable source | Audited type/role | Exactness and provenance verdict |
|---|---|---|---|
| `PresentedGroup`, `PresentedGroup.mk` | `Mathlib/GroupTheory/PresentedGroup.lean`, lines 36-49; file SHA-256 `4226ec95821cd97aaf33a5fd22d3c58dd3b8de4cd3c46e4b8b92e232b77297a9` | quotient of a free group by the normal closure and its quotient map | Representation anchor only; no computability or undecidability conclusion |
| `PresentedGroup.mk_eq_one_iff` | same module, lines 59-61 | quotient equality is membership in `Subgroup.normalClosure rels` | Useful future bridge; `#print axioms` reports `[propext, Classical.choice, Quot.sound]`, and it does not decide membership |
| `ComputablePred` | `Mathlib/Computability/Halting.lean`, lines 131-133; file SHA-256 `c2a073a05c631e7fc957577a66025e9ac36dac741f9aa865e0f053b17f0c85de` | existence of a `DecidablePred` whose Boolean indicator is computable | Exact computational vocabulary used by the target, not a proof |
| `ComputablePred.halting_problem` | same module, lines 240-242 | `forall n, not (ComputablePred (fun c => (eval c n).Dom))` | Terminal adjacent theorem; `#print axioms` reports `[propext, Classical.choice, Quot.sound]`; predicate differs from presented-group identity and no reduction was found |

`AnchorAudit.lean` kernel-checks these names and the explicit type of `ComputablePred.halting_problem` against the
pinned environment. The target itself was separately re-elaborated during this audit. Nothing in
this table is credited as an exact terminal proof body for `NovikovBooneTarget`.

## Immutable external candidates

External discovery used GitHub repository search queries for Novikov-Boone, undecidable word
problem, Lean computability, and Lean undecidability. Candidate repositories were downloaded as
archives at the recorded commit, inspected outside the repository, and never added to `.lake`.
Exact target-term searches used
`Novikov|Boone|word[ _-]?problem|PresentedGroup|FreeGroup|finitely presented group` over Lean and
Markdown sources.

| Project and revision | Toolchain / mathlib revision | Candidate declarations | Audit verdict |
|---|---|---|---|
| `DiagonaLean/DiagonaLean@1fe44b0d04182845c4948244892dee3a1f414a8b` (2026-07-02) | Lean `v4.32.0-rc1`; mathlib `9aa409007908aecdb6a12049b8d664360ebaa9f7`; CSLib `1dbda5335e3fc06c414b84ca885a35d4c6d4ab7c` | `self_halt_undecidable`, `halt_undecidable`, `halt_iff_pcp`, `halt_iff_mpcp` | No target-term match in 17 Lean files. Adjacent reduction library only. No executable `sorry`/`axiom` line found, but revision and dependency stack differ and there is no group-presentation reduction. Not import-ready or exact. |
| `edemaine/lean-wang@0420a39309cf59b1803d75622449b298e0f9f185` (2026-07-10) | Lean `v4.31.0`; mathlib `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f` | `encoded_domino_problem_undecidable`, `domino_problem_undecidable` in `LeanWang/Final.lean` | No target-term match in 152 Lean files and no executable `sorry`/`axiom` line found. Proves Wang tiling undecidability, with a different predicate and newer dependency stack; no checked reduction to a presented-group word problem. Not import-ready or exact. |
| `tannerduve/computability@e07f3a17c5285e777af6b5b08fb4059fdfb28379` (2026-05-28) | Lean `v4.24.0`; mathlib `f897ebcf72cd16f89ab4577d0c826cd14afaafc7` | `rel_halting_not_computable`, `jump_not_reducible` | No target-term match in 18 Lean files. At least 20 executable placeholder lines occur, including the named adjacent results. Different predicate and dependency stack; rejected for both exactness and proof provenance. |

The two GitHub repository-name queries for `"Novikov-Boone" Lean` and
`"undecidable word problem" Lean` each returned zero repositories at audit time. Repository search
is not a proof of global nonexistence, so the negative result is bounded to the pinned local trees,
the named immutable projects, and the recorded search protocol.

## Integration and debt decision

- Exact external closure: none found. No external theorem can be credited as `M0`.
- Closest terminal source: mathlib's `ComputablePred.halting_problem`; it needs an explicit computable reduction
  into identity equality for a constructed finite presentation.
- Closest representation bridge: `PresentedGroup.mk_eq_one_iff`; it changes quotient equality into
  normal-closure membership but provides no decision or undecidability result.
- First formal cut: construct and encode a finite presentation and prove a computable many-one
  reduction whose correctness identifies halting (or another pinned undecidable predicate) with
  `PresentedGroup.mk rels (evalWord word) = 1`.
- Source debt is independent: immutable Novikov/Boone primary theorem passages and an independent
  source review remain absent, so the audit does not promote `H1`.
- No proof, accepted receipt, audit-complete claim, or theorem-complete claim is made. Master
  acceptance remains required for this phase receipt.
