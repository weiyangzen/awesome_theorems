# THM-M-0074 exact-statement gate: blocked

- Item: `S56-M-0074-STATEMENT`
- Base revision: `2612b21a0cd5f3f13bd2223af801c73511f950c0` (tree
  `62baf871bcb662ecc80ad61fc2909e065d211ab5`)
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## First failed gate

The exact-statement gate in section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` cannot be
truthfully completed from the repository record and provisional intake. The catalog supplies only
Robert Griess, 1982, and `魔群的存在性` (existence of the Monster group). It gives no definition of
the Monster, exact proposition, theorem locator, incorporated construction, ordered binders,
hypotheses, conclusion, proof boundary, correction history, or independent source review. Stage0
explicitly leaves the precise definitions and premises open, and the catalog's `已验证` label is
untrusted metadata under rev-5.6.

The intake identifies Griess's *The friendly giant*, *Inventiones mathematicae* 69 (1982), 1-102,
DOI `10.1007/BF01389186`, as the matching complete primary-paper lead. Its inspected public surface
was bibliographic only, so the exact passage, construction boundary, definitions, proof, and errata
were not preserved or reviewed. Griess's 1981 PNAS announcement, DOI
`10.1073/pnas.78.2.689`, is a more precise statement witness: it announces a finite simple group
`F1` of the Monster order, constructed through a 196883-dimensional rational commutative
nonassociative algebra. The note calls itself an announcement, and the intake correctly does not
use it as a complete proof source or as authority for the exact 1982 root.

The unresolved choices change the proposition rather than merely its notation:

- pure existence of a group called the Monster;
- existence of some finite simple group with the Monster order;
- construction of a subgroup of, or the full automorphism group of, a source-defined Griess
  algebra together with the required simplicity and order bridges;
- identity or recognition up to `MulEquiv`, and possible uniqueness, completeness,
  representation, or automorphism conclusions; and
- the scalar field, algebra, invariant form, dimensions, universes, typeclass representation,
  ordered binders, and every degenerate case.

Choosing the convenient exact-order envelope in `IntakeProbe.lean` would be a weaker substitution:
the intake explicitly marks that envelope nonterminal because it does not identify its witness with
the source-selected Monster construction. Conversely, adding an uninterpreted `Monster` constant,
an `IsMonster` predicate, or hypotheses containing the construction properties would assume the
missing mathematics. There is therefore no canonical expression on which to certify minimal target
imports, serialize an expression fingerprint, compile checked transports, or run the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations. Those tests
are undefined, not passed. The root remains `[H1, M4, R4]`.

The intake prerequisite is provisional `[_]` in the authoritative execution DAG. Its worker
receipt declares `accepted: false`, and the instance has no accepted receipt IDs. Master acceptance
of that dependency is independently open, although the first substantive statement failure remains
the absent source-complete proposition and construction boundary.

## Pinned Lean boundary

`StatementProbe.lean` imports only `Mathlib.Data.Finite.Card` and
`Mathlib.GroupTheory.Subgroup.Simple`. It elaborates `Finite`, `Nat.card`, `Nat.card_congr`,
`IsSimpleGroup`, `MulEquiv`, and `MulEquiv.isSimpleGroup_congr` in the pinned environment. Removing
either direct import makes its corresponding checks fail. Thus these are narrow imports for the
probe, but they are not claimed to be the minimal imports for an unidentified canonical target.
The probe declares no Monster object, Griess algebra, statement envelope, or theorem.

The older `IntakeProbe.lean` also re-elaborates adjacent interfaces and an explicitly nonterminal
exact-order envelope. A bounded focused search found no Griess, Friendly Giant, Fischer-Griess, or
Monster-group declaration in repository-local Lean or pinned mathlib. This is statement-phase
feasibility evidence, not a downstream anchor audit or a global absence proof.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided
`Formalizations/Lean/.lake` symlink points to canonical pinned artifacts and was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0074` | 0 | rank 1024; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| scoped reads of the blueprint, skill, manifest, catalog, Stage0 record, and complete intake dossier | 0 | the literal existence gloss is not a binder-complete proposition; the intake intentionally leaves the canonical statement and formal target null |
| `sha256sum` over authority, intake, toolchain, lockfile, probe, and relevant mathlib inputs | 0 | exact current digests are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0074/check_intake.py` | 1 | historical intake checker rejects the now-updated authoritative blueprint hash; this phase did not rewrite intake evidence |
| `cd Formalizations/Lean && lake env lean --version` and `lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0074/StatementProbe.lean` | 0 | six narrow substrate APIs elaborated; output 462 bytes, 7 lines, SHA-256 `568b470d277f995eb631cdbc7e304040e8d3d6259273676cabbaeaa0c076691f` |
| repeat the statement probe from temporary copies while omitting each direct import | 1 each | omission makes its finite/cardinality or simple-group checks unknown, as recorded in the structured blocker |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0074/IntakeProbe.lean` | 0 | adjacent APIs and the nonterminal envelope re-elaborated; no canonical Monster target or proof body was declared |
| bounded exact-target `rg` over repository-local Lean and pinned mathlib | 1 | expected no-match exit for the focused Griess and Monster-group spellings |
| prohibited-construct scan over owned Lean | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0074/statement-blocker.json` and scoped invariant/hash assertions | 0 | structured blocker syntax, identity, null target/imports, four undefined mutations, unchanged vector, exact three-file scope, current input hashes, and absent self-test agree |
| `git diff --check -- Stage1_Instances/THM-M-0074` plus per-added-file `git diff --no-index --check` | 0 aggregate | no whitespace diagnostics; each raw no-index command returned the expected new-file difference exit 1 |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest exists because the exact-statement deliverable did not pass |

The intake checker is a historical intake-only validator. Its receipt froze an earlier blueprint
hash, while the integration lane has since projected the intake item to provisional `[_]`. This
statement attempt does not rewrite the historical intake manifest, receipt, checker, task DAG,
generated blueprint, or authoritative execution DAG to manufacture freshness.

## Retry condition

The integration lane must master-accept refreshed intake evidence. An accountable scope authority
must then approve one exact canonical claim. Under the current intake policy, that requires source
reviewers to preserve and hash the complete 1982 primary source, identify the exact theorem or
construction passage and proof boundary, audit definitions and corrections, and independently
approve whether the root is pure existence, an exact-order simple-group result, the concrete
automorphism-group construction, or a stronger package. This source work does not itself imply
`H0`; unresolved human-proof mapping may remain recorded as `H1`. Every binder, hypothesis,
conclusion, identity convention, construction object, transport, foundation choice, and boundary
case must be frozen.

A later statement worker can then encode exactly that claim, minimize its pinned imports, serialize
and hash the elaborated expression and environment, compile every credited transport, and run all
four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node.
`audit_complete` and `theorem_complete` remain false. Because the assigned phase is not genuinely
self-tested to its completion gate, no `.stage1-worker-selftest.json`, node receipt, worker `[_]`,
or master acceptance is claimed.
