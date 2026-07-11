# Source-statement crosswalk

| Claim component | Repository source | Lean candidate | Assessment |
|---|---|---|---|
| Name and attribution | `Docs/researches/math_theorems.md`: Stratonovich integral; Ruslan Stratonovich; 1966 | namespace `AwesomeTheorems.Stage1.S1_M_228` | discovery metadata only; no edition, theorem, page, or immutable source |
| Human wording | `Docs/Stage1_Blueprint.md`: "another definition of stochastic integral" | `StatementShape` | wording is not a proposition and does not determine the candidate's many fields |
| Symmetric sums | not stated in the source row | `midpointAverage`, `stratonovichRiemannSum` | mathematically plausible construction skeleton; discrete `Nat` indexing is not yet crosswalked to a primary definition |
| Limit/existence | absent | abstract field `midpointSumConverges` | placeholder-shaped interface in the legacy artifact, not evidence of convergence |
| Ito conversion and chain rule | absent | abstract interface fields | possible downstream results; broadening the root to include them would be unjustified |

The repository's `已验证` label is explicitly untrusted under rev-5.6 and supplies no proof credit.
Primary-source audit must identify a precise definition/theorem (including process class, partition
scheme, convergence mode, and normalization). Until then there is no truthful exact human-to-Lean
statement correspondence and the human status remains `H3`.

Discovery locations inspected: `Docs/Stage0_Blueprint.md`,
`Docs/researches/math_theorems.md`, `Docs/Stage1_Blueprint.md`, and
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_228.lean` at the recorded base revision.
