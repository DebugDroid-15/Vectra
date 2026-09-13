# Vectra Release Process & Distribution

## Overview
Vectra follows Semantic Versioning (`MAJOR.MINOR.PATCH`).

## Release Pipeline

1. **Local Test & Lint Verification**:
   - Run `pytest tests/` (must pass 100%).
2. **Tagging Release**:
   - Create git tag `vX.Y.Z` and push to GitHub.
3. **GitHub Actions CI/CD**:
   - Automated workflow runs test matrix across Python versions 3.10, 3.11, 3.12 on Windows and Ubuntu.
