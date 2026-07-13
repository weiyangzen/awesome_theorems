# THM-M-0478 exact-statement gate: blocked

Item: `S56-M-0478-STATEMENT`

Base revision: `444860f481e8bbf64a3357008fd4d01a52006f08` (tree
`dee24a14497f877ebd81712a99d2da08de62d7ad`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0478-INTAKE` is only in provisional
worker state `[_]`: `intake-receipt.json` has `accepted: false`, is not content-addressed, has no
accepted receipt IDs, and binds an older repository base and older blueprint/DAG hashes. It is
useful discovery input, but it is not current master-accepted dependency evidence.

The exact-statement gate also fails independently of that dependency. The catalog says only
"reciprocity property of the Legendre symbol." It gives no formula, domains, binders, prime and
oddness premises, Legendre-symbol definition or argument convention, sign exponent, distinctness
policy, equality case, or boundary policy. The intake therefore deliberately leaves the canonical
statement, claim, module, declaration or expression, elaborated-expression hash, ordered binders,
hypotheses, alternate encodings, and canonical-target environment fingerprint unresolved.

At least the following familiar propositions fit the gloss but are not the same Lean target:

```text
legendreSym q p * legendreSym p q = (-1) ^ (p / 2 * (q / 2))
  for distinct odd natural primes p and q

legendreSym q p = (-1) ^ (p / 2 * (q / 2)) * legendreSym p q
  for odd natural primes p and q, including p = q through zero symbols
```

The modulo-four equality/negated-equality case split and the `IsSquare`-over-`ZMod` formulation introduce
further proposition-level choices. In mathlib, `legendreSym p a` denotes the conventional symbol
`(a / p)`, so even argument orientation must be frozen explicitly. Article 131 of Gauss's
*Disquisitiones Arithmeticae* is a strong family lead in signed-prime residue/nonresidue language,
but the catalog does not cite it and no accepted immutable transcription, translation,
definition-chain transport, correction/errata review, or independent identity review exists.

Selecting any candidate now would override the intake boundary and silently provide missing
mathematics. Rev-5.6 consequently fails closed before canonical elaboration. There is no truthful
canonical expression whose direct imports can be certified minimal, no expression/environment
fingerprint to preserve, and no approved alternate encoding to transport. Removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are not meaningful without that
root. The vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` was re-elaborated with the existing pinned environment. Its
direct import, `Mathlib.NumberTheory.LegendreSymbol.QuadraticReciprocity`, exposes the Legendre
definition, the distinct-prime product theorem, the equality theorem that includes equal primes,
both modulo-four branches, and two square-predicate forms. The two main candidate axiom reports
list `propext`, `Classical.choice`, and `Quot.sound`.

That successful probe establishes only a usable `M3` candidate surface. It does not choose the
canonical root, certify the probe import as minimal for a missing target, provide source fidelity,
or supply proof credit. For example, the explicit product proposition can be spelled using the
narrower pinned `Mathlib.NumberTheory.LegendreSymbol.Basic` module, while the reciprocity module is
needed to inspect the existing theorem declarations. Which import is relevant cannot be decided
until the proposition and statement/proof boundary are approved.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The probe stdout SHA-256 is
`775d93407ed1b75f73dc6640374d2a1dcc6625f5bf9c6d80234daea5baf35a9a`. The automation-provided
canonical `.lake` symlink was used read-only. No dependency update, build, clone, fetch, or other
`.lake` mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0478` | 0 | rank 1359; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all; git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided untracked `Formalizations/Lean/.lake`; base revision and tree appear above |
| `git blame -L 3511,3516 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'; git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0478/IntakeProbe.lean` | 0 | seven candidate interfaces elaborated; both main candidate axiom reports list `propext`, `Classical.choice`, and `Quot.sound`; stdout digest recorded above |
| explicit product-candidate probe with `import Mathlib.NumberTheory.LegendreSymbol.Basic` | 0 | the distinct odd-prime product proposition elaborated with fully explicit output; candidate-spelling evidence only, not canonical-target selection or certified minimality |
| `python3 -B Stage1_Instances/THM-M-0478/check_intake.py` | 1 | historical intake validator rejected the integration-updated intake state `[_]` at its intake-time `[ ]` assertion; it is stale intake evidence and was not modified |
| prohibited Lean declaration scan over `Stage1_Instances/THM-M-0478/*.lean` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration was found |
| `python3 -m json.tool Stage1_Instances/THM-M-0478/statement-blocker.json` | 0 | blocker record is valid JSON |
| scoped whitespace checks over both blocker artifacts | 0 | no trailing whitespace, tab, carriage-return, or missing-final-newline defect; tracked diff check was also clean |

The historical intake validator is bound to base `0f70149d...`, older authority hashes, the exact
nine-file intake inventory, and intake-time state `[ ]`. Authority now records intake `[_]`, and
this phase adds blocker artifacts. Repairing the historical checker would exceed this statement
assignment, so its fail-closed result is recorded rather than hidden.

## Retry Condition And Status Boundary

The integration lane must first accept current intake evidence. Accountable reviewers must then
lawfully preserve and hash a primary or authoritative source, select and independently approve one
exact proposition, and freeze the domains, ordered binders, prime/odd/distinctness premises,
Legendre-symbol convention and orientation, sign formula, equality and modulo-four boundaries,
proof boundary, and corrections or errata. A later statement run can encode only that claim,
minimize its pinned imports, serialize the elaborated expression and environment, compile every
credited transport, and execute all four required mutation classes.

This is truthful blocker evidence, not completion of this node or any downstream node. No
canonical target, statement fingerprint, node receipt, root worker self-test, worker `[_]`, master
acceptance, proof credit, debt reduction, audit completion, or theorem completion is claimed.
Because the assigned phase did not self-test successfully, no `.stage1-worker-selftest.json` is
emitted.
