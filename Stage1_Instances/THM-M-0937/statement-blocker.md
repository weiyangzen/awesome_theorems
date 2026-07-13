# THM-M-0937 exact-statement gate: blocked

Item: `S56-M-0937-STATEMENT`

Base revision: `9c75282d42a7ef447d885d1d56997a79418bcd8a` (tree
`cc5285432a02107fadffb68c698690d1b98ac5f2`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only the title Vosper theorem, the attribution A. G. Vosper, the year 1956,
and the gloss `Cauchy-Davenport定理的逆` ("the inverse of the Cauchy-Davenport theorem"). It
contains no formula, incorporated definitions, ordered binders, hypotheses, conclusion, proof
boundary, correction history, boundary cases, or formal declaration. The catalog's `已验证` label
is untrusted metadata under rev-5.6.

The intake predecessor has provisional worker state `[_]`, not master-accepted state `[x]`. Its
receipt declares `accepted: false`, is not content-addressed, and contains no accepted receipt ID.
Rev-5.6 section 10.2 permits this dependency-ordered blocker attempt, but master closure remains
dependency ordered. More importantly, intake deliberately leaves the canonical claim, Lean module
and expression, expression hash, canonical-target environment fingerprint, ordered binders, and
hypotheses null or empty.

The family gloss does not decide among materially different propositions:

- the complete classification of every critical nonempty pair in `Z/pZ`;
- an equality-case inverse theorem with additional cardinality and non-saturation hypotheses;
- a progression-only corollary after excluding saturation, complement, and singleton cases;
- an affine-normalized interval formulation; or
- a formulation over an arbitrary group of prime order with an explicit transport to `Z/pZ`.

Even after selecting one of those roots, proposition-critical choices remain: `Finset` versus
finite `Set`, criticality versus equality hypotheses, inclusive versus exclusive exceptional
branches, small-prime policy, natural-number subtraction, and the definition of an arbitrary-length
arithmetic progression. The length/cardinality relationship, zero or nonzero common difference,
wraparound, repeated terms, singleton overlap, ordered binders, foundation profile, and every
degenerate case are also open.

The primary article and its addendum have been identified but not textually inspected:

- A. G. Vosper, *The Critical Pairs of Subsets of a Group of Prime Order*, JLMS s1-31(2)
  (1956), 200-205, DOI `10.1112/jlms/s1-31.2.200`;
- A. G. Vosper, *Addendum to "The Critical Pairs of Subsets of a Group of Prime Order"*,
  JLMS s1-31(3) (1956), 280-282, DOI `10.1112/jlms/s1-31.3.280`.

The addendum is a mandatory correction or extension boundary, not evidence that the original paper
alone supplies the current exact statement. No primary premise, conclusion, definition, proof, or
correction crosswalk has been independently approved.

Boothby, DeVos, and Montejano, arXiv:1301.0095v2, Theorem 1.3, is an inspected exact secondary
lead. It states a four-way classification for nonempty `A, B` in `Z/pZ` with `p` prime and
`|A + B| < |A| + |B|`: whole-group saturation, the one-missing-element boundary, a singleton
factor, or two arithmetic progressions with a common difference. The catalog does not cite or
select that "version I" root. Promoting it now would substitute an unapproved variant rather than
elaborate the exact received target.

Sections 5 and 5.1 of the blueprint make statement ambiguity and a missing expression fingerprint
hard blockers. There is therefore no honest expression for which imports can be certified minimal,
no credited alternate encoding, and no checked transport. The required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined rather than passed.
No `Statement.lean`, theorem declaration, proof body, weakened special case, or broadened interface
was added. The vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with the single direct import
`Mathlib.Combinatorics.Additive.CauchyDavenport`. It checks `Finset`, nonempty finite sets, ranges,
images, `ZMod`, the forward `ZMod.cauchy_davenport` lower bound, its minimum-order generalization,
and a finite-sumset upper bound. The complete deterministic probe output has SHA-256
`b604d21b1cbd82703c4f2687f03abe3452db61d920ff43d6919598821b06c421`.

Those APIs are adjacent substrate only. In particular, `ZMod.cauchy_davenport` is the forward
cardinality lower bound, not Vosper's inverse classification. The probe declares no canonical
target, source transport, or proof body, so its import cannot be called minimal for the absent
target and receives no statement or proof credit.

A bounded search of repo-local Lean and pinned mathlib found no declaration named for Vosper,
critical pairs, or an inverse of Cauchy-Davenport. The nearby `ThreeAPFree` library concerns
progressions of length three and does not directly encode arbitrary finite progressions in the
candidate theorem. This is narrow statement-feasibility evidence, not the downstream immutable
anchor audit or proof of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository
root unless another working directory is shown.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0937` | 0 | rank 1476; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided untracked `.lake` symlink existed; base revision and tree appear above |
| catalog, Stage0, primary/addendum, secondary-candidate, intake, and identity-history inspection | 0 | confirmed the sparse family gloss, null canonical target, uninspected primary texts, noncanonical secondary restatement, and pre-dedup ID trap |
| authority, intake, toolchain, lockfile, and pinned source SHA-256 checks | 0 | exact current hashes are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib `git rev-parse HEAD 'HEAD^{tree}'` and `git status --short` | 0 | revision and tree above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0937/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout SHA-256 `b604d21b1cbd82703c4f2687f03abe3452db61d920ff43d6919598821b06c421`; no target declaration or proof body |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 1, expected no match | no Vosper, critical-pair, or inverse-Cauchy-Davenport declaration matched; discovery only |
| `python3 -B Stage1_Instances/THM-M-0937/check_intake.py` | 1 | the historical intake receipt binds an older blueprint hash and replay now fails that freshness check; this phase records rather than rewrites historical evidence |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, scoped invariants, whitespace, and absent-self-test checks are recorded in the structured
blocker beside this report.

The historical intake checker is frozen to its pre-integration authority hashes and original
nine-file inventory. Integration subsequently regenerated the blueprint and execution projection.
Adding these two statement artifacts also makes that intake-only inventory historical. This run
records the limitation instead of rewriting the intake checker, receipt, instance, task DAG,
generated blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then lawfully preserve immutable primary article and addendum editions, select and independently
approve one exact source root, and map every incorporated definition, ordered binder, hypothesis,
exceptional branch, conclusion, proof boundary, correction, erratum, and boundary case. They must
freeze the carrier, criticality, progression, common-difference, foundation, and transport
conventions.

A fresh statement worker can then encode precisely that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
execute all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt change
is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
