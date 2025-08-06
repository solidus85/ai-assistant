# Offline Docker Builds with Local Wheels 🚀

## The Problem Solved
- **Before**: Every requirements.txt change = download 1GB+ from internet
- **After**: Download once, reuse forever (even with requirements changes!)

## Quick Start

### 1. Download all wheels (one time)
```bash
./download-wheels.sh
```
This creates a `wheels/` directory with all packages (~1-2GB).

### 2. Build with local wheels
```bash
# Option A: Offline build (no internet needed)
docker-compose -f docker-compose.offline.yml build

# Option B: Local wheels with PyPI fallback
docker build -f Dockerfile.wheels -t ai-assistant:wheels .
```

### 3. Run the container
```bash
docker-compose -f docker-compose.offline.yml up
```

## How It Works

```
Traditional Docker Build:
requirements.txt → Internet → Download ALL packages → Install

Our Offline Build:
requirements.txt → wheels/ folder → Install from disk → No internet needed!
```

### The Wheels Directory Structure
```
wheels/
├── numpy-1.26.4-cp311-linux_x86_64.whl     (18 MB)
├── torch-2.0.0-cp311-linux_x86_64.whl      (800 MB)
├── flask-3.0.0-py3-none-any.whl            (95 KB)
├── chromadb-0.4.22-py3-none-any.whl        (500 KB)
└── ... (100+ more packages)
```

## Three Dockerfile Options

### 1. **Dockerfile.wheels** (Recommended)
- Uses local wheels first
- Falls back to PyPI if package missing
- Best for development

### 2. **Dockerfile.offline** (Fully Offline)
- ONLY uses local wheels
- Fails if package not found locally
- Best for air-gapped environments

### 3. **Dockerfile.cached** (Volume Caching)
- Uses Docker volume for pip cache
- Still needs internet
- Good for CI/CD

## Workflow Examples

### Adding a New Package
```bash
# 1. Add to requirements.txt
echo "pandas==2.0.0" >> requirements.txt

# 2. Download the new wheel
./download-wheels.sh

# 3. Build (will use local wheel)
docker-compose -f docker-compose.offline.yml build
```

### Updating Package Versions
```bash
# 1. Update requirements.txt
# Change: flask==3.0.0 → flask==3.1.0

# 2. Download new version
./download-wheels.sh

# 3. Build (old and new versions both cached)
docker-compose -f docker-compose.offline.yml build
```

## Advanced Usage

### Download Specific Packages
```bash
# Download single package
pip download --dest ./wheels pandas

# Download from different requirements file
pip download --dest ./wheels -r requirements-dev.txt
```

### Clean Old Wheels
```bash
# Remove wheels not in current requirements
pip-sync --dry-run  # See what would be removed
rm wheels/*.whl      # Remove all and re-download
./download-wheels.sh # Fresh download
```

### Check Wheel Compatibility
```bash
# List all wheels
ls -lh wheels/

# Check wheel details
pip show -f wheels/numpy*.whl

# Verify all requirements covered
pip install --dry-run --find-links ./wheels -r requirements.txt
```

## Build Time Comparison

| Method | First Build | Subsequent Builds | Internet Required |
|--------|------------|-------------------|-------------------|
| Original Dockerfile | 5-10 min | 5-10 min | Yes (every time) |
| Layer Caching | 5-10 min | 30 sec* | Yes (if changed) |
| Volume Caching | 5-10 min | 2-3 min | Yes (always) |
| **Local Wheels** | 5-10 min** | 30 sec | **No** |

\* Only if requirements.txt unchanged
\** First time only to download wheels

## Troubleshooting

### "No matching distribution found"
```bash
# Package missing from wheels, download it:
pip download --dest ./wheels missing-package
```

### "Platform mismatch" errors
```bash
# Download platform-specific wheels:
pip download --dest ./wheels --platform linux_x86_64 package-name
```

### Wheels directory too large
```bash
# Remove unused wheels:
find wheels/ -name "*.whl" -mtime +30 -delete  # Remove 30+ days old
```

## Storage Considerations

- Wheels directory: ~1-2GB (one-time)
- Shared across all builds
- Can be backed up/copied to other machines
- Can be mounted as Docker volume for multiple projects

## CI/CD Integration

```yaml
# .github/workflows/build.yml
- name: Cache wheels
  uses: actions/cache@v3
  with:
    path: wheels
    key: ${{ runner.os }}-wheels-${{ hashFiles('requirements.txt') }}

- name: Download missing wheels
  run: ./download-wheels.sh

- name: Build Docker image
  run: docker build -f Dockerfile.offline -t app .
```

## Summary

✅ **One-time download** of all packages
✅ **No internet needed** for Docker builds  
✅ **Survives requirements.txt changes**
✅ **Portable** (copy wheels/ to any machine)
✅ **Fast** (30 second rebuilds)