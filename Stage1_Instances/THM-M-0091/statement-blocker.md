# Exact-statement gate: blocked

Item: `S56-M-0091-STATEMENT`

Theorem: `THM-M-0091`

Base revision: `d266c6f5ce5732e1fccd687e2f9ce9aa2a0ed1fe` (tree
`e77c8d6d5b41cb13d9d8acab2753ac37c4ebd6b4`).

## Decision

The statement item remains `[ ]`. Its prerequisite, `S56-M-0091-INTAKE`, has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt has `accepted: false`, is not
content-addressed, and has no accepted receipt ID. It deliberately leaves both the canonical
mathematical statement and formal target null. The old intake validator also cannot replay the
current authoritative execution state: it expects the intake item to remain `[ ]`, whereas the
integration lane now records the provisional `[_]` state. This requires integration-lane review;
the statement inspection does not rewrite the historical intake evidence.

Independently and decisively, the exact-statement gate cannot pass from the received source record.
The repository gives the title "Weyl dimension formula," attributes it to Hermann Weyl in 1925,
and says only "dimensions of irreducible representations of compact Lie groups." It supplies no
formula, bibliography, theorem or formula number, page, incorporated definitions, ordered binders,
assumptions, correction history, boundary policy, or independent source approval. The catalog's
`已验证` label is explicitly untrusted under rev-5.6.

The intake authenticated Weyl's 1925 part-I paper as a bibliographic lead (DOI
`10.1007/BF01506234`, pages 271-309), but no lawful content passage was preserved or reviewed.
OpenAlex reports that the paper is closed access and has no repository full text. Crossref exposes
metadata and a text-mining link, not a reviewed theorem passage. Neither source fixes which modern
compact-group formulation the catalog intends.

A precise modern candidate was also inspected: Pavel Etingof's 2024 MIT OpenCourseWare notes,
section 26.5, Proposition 26.8 (printed page 142), state
`dim L_lambda = product_(alpha in R+) (alpha, lambda + rho) / (alpha, rho)` for the finite-dimensional
irreducible module of dominant integral highest weight `lambda` of a complex semisimple Lie algebra.
That proposition and the notes' separate representation-equivalence and compact-group structure
results are useful retry inputs, but they do not themselves state the catalog's broad compact-Lie-
group claim or settle its connected, central-torus, and disconnected boundaries. Selecting this
Lie-algebra proposition as the root still requires accountable source-scope approval and a checked
transport, so it is not credited as statement identity here.

Material proposition choices therefore remain open:

- compact connected semisimple versus compact connected reductive groups, and the treatment of
  disconnected groups;
- continuous finite-dimensional complex group representations versus corresponding highest-weight
  Lie-algebra modules;
- maximal torus, positive-root system, highest-weight dominance and integrality, and Weyl-vector
  conventions;
- root versus coroot pairing and its normalization;
- equality in naturals, integers, rationals, reals, or complexes, including coercions and a proof
  that every denominator is nonzero;
- central-torus, empty-root, rank-zero, trivial-weight, and other boundary cases;
- whether the root is the product formula itself or a checked specialization of the Weyl character
  formula at the identity.

Each choice changes binders, hypotheses, conclusion, or boundary behavior. Selecting a familiar
product from memory, encoding only an abstract root-system identity, or postulating a structure
field containing the desired equality would invent, narrow, or substitute the received theorem.
Rev-5.6 sections 5 and 5.1 make this ambiguity and the missing elaborated-expression fingerprint
hard blockers.

There is consequently no honest canonical Lean target whose imports can be certified minimal, no
credited alternate encoding, and no meaningful removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutation suite. The lifecycle stays `planned`, the debt
vector stays `[H1, M3, R4]`, and no statement receipt or worker completion claim is emitted.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated with the pinned environment. Its
four direct imports expose adjacent root-pairing, Lie-weight, representation,
character-at-identity, and Lie-group interfaces. It checks `RootPairing`,
`RootPairing.Base.IsPos`, `LieModule.Weight`, `LieAlgebra.IsKilling.rootSystem`,
`LieAlgebra.IsKilling.apply_coroot_eq_cast`, `Representation`, `FDRep`, `FDRep.char_one`,
`Representation.char_one`, and `LieGroup`.

The probe does not declare the Weyl dimension formula, connect a compact-group irreducible to
highest-weight root data, or define a product. A bounded case-insensitive search of repo-local Lean
and pinned mathlib found no relevant Weyl-dimension declaration. Therefore its imports are only a
statement-feasibility boundary and cannot be called minimal imports for an absent target. The
complete probe stdout has SHA-256
`aaaff85b6fe2b320be4102feb62ab447710b4e428e120a35b3926936d63704de`.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, dependency clone, fetch,
or other `.lake` mutation was performed.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0091` | 0 | rank 1108; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base identifiers appear above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0091/IntakeProbe.lean` | 0 | twelve adjacent APIs elaborated; five theorem interfaces reported only `propext`, `Classical.choice`, and `Quot.sound`; no target declaration or proof body; stdout hash recorded above |
| bounded Weyl-dimension search in pinned mathlib and repo-local Lean | 0 | no relevant declaration or complete compact-group/highest-weight/product bridge found |
| bounded OpenAlex and Crossref DOI metadata queries | 0 | authenticated the historical paper and closed-access boundary; no exact theorem passage was inspected or credited |
| `python3 -B Stage1_Instances/THM-M-0091/check_intake.py --worker-packet .stage1-worker-selftest.json` | 1 | historical intake replay stops at its assertion that the authoritative intake item still has state `[ ]`; it is now provisional `[_]` |

The structured blocker was also parsed and checked for null target/fingerprints, unchanged debt,
four unavailable mutation classes, false completion flags, and blocked status. A prohibited Lean
construct scan over the owned Lean probe found no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`,
`opaque`, or `unsafe` declaration. New-file and scoped whitespace checks passed. Exact commands and
results are duplicated in `statement-blocker.json` for machine inspection.

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash a lawful immutable primary or authoritative theorem
passage and independently select its exact modern formulation. They must fix every incorporated
definition, ordered binder, hypothesis, conclusion, correction, erratum, normalization, coercion,
and boundary case, together with any checked transport from Weyl's historical semisimple setting to
the selected compact-group formulation. A future statement run may then encode exactly that source
model, minimize pinned imports, serialize and hash the elaborated expression and environment,
compile every credited transport, and execute all four required mutation classes. The integration
lane must also revalidate and master-accept the intake dependency before accepting that transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. `audit_complete: false` and `theorem_complete: false`; no debt-vector change is
proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master acceptance is claimed.
