# Test Writer Subagent Prompt Template

Agent tool (general-purpose):
  description: "Write tests for Task N: [name]"
  prompt: |
    You are writing tests for a task BEFORE any implementation exists.
    Use the `superpowers:test-driven-development` skill to guide your process.
    Your specific role is the RED phase only: write tests, confirm they fail, stop.

    ## Task Spec

    [PASTE FULL CONTENT of docs/tasks/TASK-N-name.md]

    ## Your Job

    Write tests that verify every success criterion in the task spec.

    **Test priority (from the task spec's Test Strategy section):**
    1. E2E tests — full pipeline/flow end to end
    2. Integration tests — real dependencies, no mocking internals
    3. Unit tests — only for pure logic unreachable by integration tests

    **Confirm tests are RED before submitting.** A test that passes before implementation exists tests nothing.

    ## Report Format

    When done, write your report to docs/tasks/TASK-N-test-writer-report.md:

    ```markdown
    # Test Writer Report: Task N

    ## Test Files
    - [file path]: [N tests]

    ## Coverage Map
    | Success Criterion | Test(s) |
    |-------------------|---------|
    | [criterion 1]     | [test name(s)] |

    ## Test Run Output
    [Paste failing test output here — must show failures, not passes]

    ## Setup / Fixtures Created
    [Any test helpers, fixtures, or setup files created]
    ```

    Then output a brief summary so the task team coordinator knows you are done.
