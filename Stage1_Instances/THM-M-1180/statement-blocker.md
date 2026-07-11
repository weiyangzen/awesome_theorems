# Statement-phase blocker

Item: `S56-M-1180-STATEMENT`

Base revision: `168aae8f6c98f025672f9f8fcfedb2a74785e4b9`.

Verdict: blocked. No canonical Lean target, statement fingerprint, statement-phase receipt, or
statement-phase completion is claimed.

## First failed gate

The intake freezes only the umbrella label "Caffarelli regularity theory" and expressly leaves the
exact primary-source theorem open. The repository description, "regularity of the Monge-Ampere
equation," does not determine one proposition. In particular, it does not select between the two
primary-source candidates already identified by the intake, nor does it fix the solution notion,
domain geometry, density hypotheses, exponent, estimate, or regularity conclusion. Consequently
there is no exact human claim to which a Lean expression can truthfully be mapped.

This fails the hard statement gate in section 5 of `Docs/Stage1_Blueprint_rev-5.6.md`: statement
ambiguity prevents an exact elaborated expression and its fingerprint. The retry condition is an
inspected primary source with one exact theorem/page selected and a complete assumption/conclusion
crosswalk approved for this target.

## Legacy Lean artifact boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_148.lean` elaborates in the pinned environment,
but it is not the required exact target. Its own documentation calls `StatementShape` a
`ContDiffOn R 2` surrogate and encodes the missing solution and localization mathematics as
user-supplied proposition fields. Crediting that declaration would substitute a conditional
surrogate for the unspecified source theorem, contrary to the intake exclusions and the rev-5.6
non-substitution rule. The legacy file was inspected and validated only as negative evidence about
the current boundary; it was not modified and supplies no statement-phase receipt.

## Commands and results

All commands ran from the worker clone unless the table gives a narrower working directory.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1180` | exit 0; rank 148, planned, L0/rework_required, theorem_complete false |
| `git rev-parse HEAD` | exit 0; `168aae8f6c98f025672f9f8fcfedb2a74785e4b9` |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_148.lean` | exit 0; the legacy surrogate declarations elaborated with no Lean errors |
| `curl -L --fail --silent --show-error -o /tmp/caffarelli-w2p.pdf https://annals.math.princeton.edu/wp-content/uploads/annals-v131-n1-p05.pdf` | exit 22; the guessed publisher PDF URL returned HTTP 404, so no source text was used |
| `curl -L --silent https://api.crossref.org/works/10.2307%2F1971510` | exit 0; bibliographic metadata confirms DOI `10.2307/1971510`, volume 131, issue 1, page 135, but provides no theorem text |
| `curl -L --silent https://api.openalex.org/works/https://doi.org/10.2307/1971510` | exit 0; reports the article closed-access with no repository full text |

The successful Lean command establishes only that an existing surrogate is syntactically and
kernel elaborable. It cannot cure source-statement ambiguity and is not evidence that the exact
Caffarelli theorem has elaborated.

## Remaining statement obligations

1. Select and inspect one primary theorem, including its definitions, theorem number, exact pages,
   dependencies, and errata status.
2. Freeze every ordered binder, domain and dimension restriction, convexity and solution notion,
   density hypothesis, local/global qualifier, exponent, constant dependency, and conclusion.
3. Encode that claim without assuming the regularity conclusion or its substantive localization
   package as structure fields.
4. Minimize pinned imports, elaborate the exact proposition, serialize its expression and
   environment fingerprints, and compile credited transports.
5. Run the required removed-hypothesis, changed-domain, binder-scope, and boundary-case mutation
   tests.

Because the first obligation is unresolved, creating a `.stage1-worker-selftest.json` would
misrepresent the assigned phase as genuinely self-tested. No such manifest is emitted.
