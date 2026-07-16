# Modal Startup UUID Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ensure the container reaches Streamlit and listens on `0.0.0.0:8080` when Modal does not expose `/proc/sys/kernel/random/uuid`.

**Architecture:** Keep the entrypoint structure unchanged and replace its procfs-specific defaults with a small `generate_uuid` shell function backed by Python's standard-library `uuid.uuid4()`. Preserve environment-variable overrides through the existing POSIX parameter-expansion pattern and cover the behavior with the repository's existing `unittest`-based source contract tests plus shell/container verification.

**Tech Stack:** POSIX `sh`, Python 3.12 standard library, `unittest`, Streamlit, Docker

---

## File Map

- Modify `tests/test_requirements.py`: add regression coverage for portable UUID generation, UUID v4 validity, and environment override syntax.
- Modify `start.sh`: add the Python-backed UUID generator and use it only when `R_ID` or `PASSWORD` is unset or empty.

### Task 1: Add the startup regression test

**Files:**
- Modify: `tests/test_requirements.py`
- Test: `tests/test_requirements.py`

- [ ] **Step 1: Add imports and failing regression tests**

Add `subprocess` and `uuid` imports, then add these methods to `StartupRequirements`:

```python
    def test_uuid_defaults_do_not_depend_on_procfs(self):
        self.assertNotIn("/proc/sys/kernel/random/uuid", self.script)
        self.assertIn("generate_uuid()", self.script)
        self.assertIn("python3 -c 'import uuid; print(uuid.uuid4())'", self.script)

    def test_uuid_generator_produces_uuid4(self):
        generated = subprocess.run(
            ["python3", "-c", "import uuid; print(uuid.uuid4())"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        parsed = uuid.UUID(generated)
        self.assertEqual(parsed.version, 4)
        self.assertEqual(str(parsed), generated)

    def test_explicit_credentials_override_generated_defaults(self):
        self.assertIn('R_ID="${R_ID:-$(generate_uuid)}"', self.script)
        self.assertIn('PASSWORD="${PASSWORD:-$(generate_uuid)}"', self.script)
```

- [ ] **Step 2: Run the focused tests and confirm the new contract fails**

Run:

```bash
python3 -m unittest tests.test_requirements.StartupRequirements -v
```

Expected: the existing two tests pass, `test_uuid_generator_produces_uuid4` passes independently, and the two source-contract tests fail because `start.sh` still contains the procfs path and has no `generate_uuid` function.

- [ ] **Step 3: Commit the failing regression test**

```bash
git add tests/test_requirements.py
git commit -m "test: reproduce Modal UUID startup failure"
```

### Task 2: Implement portable UUID defaults

**Files:**
- Modify: `start.sh:4-7`
- Test: `tests/test_requirements.py`

- [ ] **Step 1: Add the minimal UUID generator and replace both defaults**

Replace the existing procfs-based assignments with:

```sh
generate_uuid() {
    python3 -c 'import uuid; print(uuid.uuid4())'
}

R_ID="${R_ID:-$(generate_uuid)}"
PASSWORD="${PASSWORD:-$(generate_uuid)}"
```

Do not modify the Streamlit command, backend retry timing, or any other startup behavior.

- [ ] **Step 2: Run the focused tests and confirm they pass**

Run:

```bash
python3 -m unittest tests.test_requirements.StartupRequirements -v
```

Expected: all five `StartupRequirements` tests pass.

- [ ] **Step 3: Check POSIX shell syntax**

Run:

```bash
/bin/sh -n start.sh
```

Expected: exit status 0 with no output.

- [ ] **Step 4: Commit the production fix**

```bash
git add start.sh
git commit -m "fix: generate startup UUIDs without procfs"
```

### Task 3: Verify the complete repository and runtime

**Files:**
- Verify: `start.sh`
- Verify: `tests/test_requirements.py`
- Verify: `Dockerfile`

- [ ] **Step 1: Run the complete unit-test suite**

Run:

```bash
python3 -m unittest discover -s tests -v
```

Expected: all tests pass with zero errors and zero failures.

- [ ] **Step 2: Check the final patch for whitespace and unintended changes**

Run:

```bash
git diff HEAD~2 --check
git status --short
git log -3 --oneline
```

Expected: `git diff --check` exits 0; status contains no uncommitted production or test changes; the log shows the test commit followed by the fix commit.

- [ ] **Step 3: Build the application image**

Run:

```bash
docker build -t deepseek-v4-intro:uuid-fix .
```

Expected: build exits 0 and produces `deepseek-v4-intro:uuid-fix`.

- [ ] **Step 4: Run a port-8080 smoke test**

Run:

```bash
container_id=$(docker run -d -p 127.0.0.1::8080 -e BACKEND_RETRY_DELAY=3600 deepseek-v4-intro:uuid-fix)
host_port=$(docker port "$container_id" 8080/tcp | sed 's/.*://')
for attempt in 1 2 3 4 5 6 7 8 9 10; do
    if curl --fail --silent --show-error "http://127.0.0.1:${host_port}/_stcore/health"; then
        break
    fi
    sleep 2
done
curl --fail --silent --show-error "http://127.0.0.1:${host_port}/_stcore/health"
docker logs "$container_id"
docker stop "$container_id"
```

Expected: the health endpoint returns `ok`, logs contain no `/proc/sys/kernel/random/uuid` error, and the container stops cleanly. If Docker is unavailable in the execution environment, record that limitation and rely on unit tests plus `/bin/sh -n` rather than claiming container-level verification.
