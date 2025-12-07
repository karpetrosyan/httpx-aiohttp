---
icon: material/hand-coin-outline
---

## Getting Started

1. **Fork the repository**: Fork [](https://github.com/karpetrosyan/httpx-aiohttp/) to your GitHub account

2. **Clone and create a branch**:
```bash
git clone https://github.com/username/httpx-aiohttp
cd httpx-aiohttp
git switch -c my-feature-name
```

3. **Install dependencies**: This project uses `uv` for dependency management. Make sure you have it installed, then install the project dependencies:
```bash
uv sync --all-extras
```


## Releasing (Maintainers Only)

This section is for maintainers who have permissions to publish new releases.

### Release Process

1. **Update the version** in `pyproject.toml`:
   ```diff
   [project]
   - version = "0.0.1"
   + version = "0.0.2"
   ```

2. **Generate the changelog** using `git cliff`:
   ```bash
   git cliff --output CHANGELOG.md --tag 0.0.2
   ```
   - Specify the new release tag with `--tag`

3. **Commit the changes** with an unconventional commit message:
   ```bash
   git add pyproject.toml CHANGELOG.md
   git commit -m "Version 0.0.2"
   ```

4. **Create a git tag** for the release:
   ```bash
   git tag 0.0.2
   ```

5. **Push to GitHub** (both commits and tags):
   ```bash
   git push
   git push --tags
   ```

6. **Ensure CI passes** - Wait for all GitHub Actions workflows to complete successfully

7. **Done!** - The release is published once CI passes
