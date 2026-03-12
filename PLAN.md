# THIS IS A DEVELOPMENT PLAN
also , it is a "directory design" for to24

## directory tree of to24
```bash
to24/
├── python/          # Python implementation
│   └── to24/        # Project name
│       ├── to24/    # Library code
│       ├── test/    # Test case
│       └── app/     # Example
├── c/               # C implementation (shared library/executable)
│   ├── src/
│   ├── include/
│   ├── CMakeLists.txt
│   └── README.md
├── cpp/             # C++ implementation
│   ├── src/
│   ├── CMakeLists.txt
│   └── ...
├── nodejs/          # Node.js (TypeScript/JavaScript)
│   ├── src/
│   ├── package.json
│   └── tsconfig.json
├── rust/            # Rust implementation
│   ├── src/
│   ├── Cargo.toml
│   └── ...
├── go/              # Go implementation
│   ├── cmd/
│   ├── pkg/
│   └── go.mod
├── web/             # Pure HTML + JavaScript (frontend demo)
│   ├── index.html
│   └── style.css
├── scripts/         # Helper scripts (e.g., packaging scripts)
│   ├── package.py   # Python script to package builds by platform
│   └── build_all.sh # One-click build for all languages
└── README.md        # Overall documentation
```