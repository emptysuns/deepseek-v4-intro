# Modal Startup UUID Compatibility Fix

**Date:** 2026-07-16
**Status:** Approved

## Problem

The container entrypoint enables `set -eu` and initializes `R_ID` and `PASSWORD` by reading `/proc/sys/kernel/random/uuid`. Modal's runtime does not expose that procfs entry. Each failed `cat` therefore makes the assignment command fail and terminates `start.sh` before Streamlit is executed. Nothing listens on port 8080, so Modal reports a web-server startup timeout after 60 seconds.

The existing Streamlit command already uses the required port and interface (`8080` and `0.0.0.0`), so changing its bind configuration or increasing Modal's startup timeout would only mask the actual entrypoint failure.

## Selected Design

Generate both default values with Python's standard-library `uuid.uuid4()` rather than reading procfs. Python 3.12 is guaranteed by the image's `python:3.12-alpine` base, and `uuid.uuid4()` preserves the standard UUID representation expected by the current configuration.

Explicit `R_ID` and `PASSWORD` environment values retain precedence. No dependency, Dockerfile, Streamlit, backend retry, or port configuration changes are required.

## Alternatives Considered

1. **OpenSSL random bytes:** OpenSSL is installed, but raw random output is not a standard UUID without additional formatting.
2. **Procfs with Python fallback:** This preserves the existing Linux-specific path but adds a branch without providing a benefit because Python is always available.
3. **Increase startup timeout:** Rejected because the entrypoint exits; waiting longer cannot make port 8080 available.

## Test Strategy

Add a startup regression test before changing production code. It will verify that:

- `start.sh` no longer depends on `/proc/sys/kernel/random/uuid`;
- the selected generator uses Python's standard-library UUID implementation;
- generated values parse as UUID version 4 values;
- environment-provided values continue to override generated defaults.

Then run the complete unit-test suite, a POSIX shell syntax check, and—when Docker is available—a container smoke test that confirms an HTTP response is available on port 8080.

## Scope and Risks

The change is limited to default credential generation in `start.sh` plus its regression test. UUID generation occurs only during container startup, so process-launch overhead is negligible. Logging behavior and all externally configurable environment variables remain unchanged.
