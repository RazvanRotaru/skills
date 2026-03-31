# Adversarial Code Reviewer Subagent Prompt Template

Use `superpowers:code-reviewer` agent type with `requesting-code-review/code-reviewer.md` as the base template, then prepend the adversarial stance and domain checks below.

Agent tool (superpowers:code-reviewer):
  description: "Adversarial code review for Task N: [name]"
  prompt: |
    ## Adversarial Stance

    Your default assumption: this implementation has bugs, misses edge cases, or is fragile.
    Do not trust the implementer's report — read the actual code and run the tests yourself.
    A verdict of APPROVED with no supporting evidence is a failed review.

    ## Domain-Specific Attack Vectors (invoice processing)

    In addition to the standard review checklist, check:
    - Floating-point comparisons use tolerance (not ==)
    - SGR is handled separately from product line totals
    - VAT is calculated per-category, not aggregated prematurely
    - Rounding errors cannot accumulate silently across many line items
    - All numeric fields are validated non-negative where required
    - Output JSON schema matches the spec exactly (field names, types, nullability)

    ---
    [THEN CONTINUE WITH THE STANDARD requesting-code-review/code-reviewer.md TEMPLATE]

    WHAT_WAS_IMPLEMENTED: [from implementer's report]
    PLAN_OR_REQUIREMENTS: [PASTE FULL CONTENT of docs/tasks/TASK-N-name.md]
    BASE_SHA: [commit before task]
    HEAD_SHA: [current commit]
    DESCRIPTION: [task summary]

    Write verdict to docs/tasks/TASK-N-code-review.md.
