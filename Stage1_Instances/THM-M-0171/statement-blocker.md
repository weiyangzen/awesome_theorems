# Statement gate blocker

Item: `S56-M-0171-STATEMENT`  
Theorem: `THM-M-0171`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The accepted intake does not identify a unique mathematical proposition. The repository gives only
the title "Gromov embedding theorem," an attribution to Mikhail Gromov, the year 1986, and the
gloss "a necessary-and-sufficient condition for metric-space embedding." It supplies no
publication, theorem/page, complete wording, or definitions of the source and target classes or of
"embedding." These omissions leave materially different readings open, including a
negative-type criterion for Hilbert-space embedding, a compact Gromov-Hausdorff statement, an
h-principle or Nash-Kuiper statement, and a Riemannian isometric-embedding statement.

The legacy module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_132.lean` deliberately selects a different,
provisional branch: the Kuratowski existence theorem for an isometric embedding of a separable
metric space into `lp (fun _ : Nat => Real) top`. That result is a sufficient existence theorem,
not the unidentified necessary-and-sufficient theorem in the metadata, and it is not established
by the dossier as a theorem of Gromov. Its successful elaboration is discovery evidence only.
Neither its elementary distance-preservation predicate nor its adjacent compact
Gromov-Hausdorff wrappers can supply the missing source identity.

Under sections 5 and 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md`, statement ambiguity and a missing
expression fingerprint are hard blockers. Choosing one reading now would invent source binders,
hypotheses, conventions, and a conclusion, or substitute a convenient theorem. Consequently the
ordered quantifiers, exact domain, hypotheses, conclusion, boundary cases, minimal imports,
normalized expression, expression hash, checked alternate transports, and meaningful mutation
tests cannot be frozen truthfully. The machine state remains `M4`; no formal declaration or proof
credit is introduced by this phase.

## Environment fingerprint

- Repository base revision: `1910c5876754c1f79457f083f780f71a3e4339b2`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Legacy discovery module SHA-256:
  `3e96fd4bf1e03888e5fc2af68afc8fce8f06af3aed29d346891e622df569b430`.

The worktree's `Formalizations/Lean/.lake` is an existing untracked link to the canonical pinned
Lake artifacts. It was used read-only. No dependency update, build, clone, or fetch command was
run.

## Validation evidence

Commands ran from this worker clone using the existing pinned environment.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard consistency passed: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0171` | 0 | Rank 132, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_132.lean` | 0 | Legacy Kuratowski/Gromov-Hausdorff discovery module elaborated; this does not identify or elaborate the exact root |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Checked mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_132.lean` | 0 | Produced the three hashes recorded above |
| `rg -n -i 'GromovEmbedding\|Gromov embedding\|Schoenberg\|negative type\|conditionally negative\|Nash[- ]?Kuiper' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | No matching named terminal theorem or source reference in pinned mathlib; exit 1 is the no-match result |

## Retry condition

An accountable source review must identify an immutable primary-source edition and exact
theorem/page, transcribe the complete claim, and fix the meaning of embedding, source and target
classes, regularity, dimensions, and all conventions and edge conditions. The next statement run
can then encode that proposition with the minimal pinned imports, serialize its elaborated
expression, and execute the removed-hypothesis, changed-domain, binder-scope, and boundary-case
mutations.

Until then, statement acceptance, audit completion, and theorem completion are false. Because the
assigned phase is not genuinely self-tested to its completion gate, no worker self-test manifest
is emitted.
