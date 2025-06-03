# Contribution Guidelines

We welcome contributions to MANUS MCP for Roo! Here's how to get involved:

## How to Contribute
1. **Report Issues**: Use GitHub Issues to report bugs or suggest features
2. **Submit Pull Requests**:
   - Fork the repository
   - Create a new branch (`git checkout -b feature/your-feature`)
   - Commit your changes (`git commit -am 'Add some feature'`)
   - Push to the branch (`git push origin feature/your-feature`)
   - Open a pull request

## Development Setup
```bash
git clone https://github.com/0HASHMI0/manus-mcp-roo.git
cd manus-mcp-roo
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
pip install -r requirements-dev.txt
```

## Coding Standards
- Follow PEP 8 for Python code
- Use type hints for all function signatures
- Document public methods with docstrings
- Write tests for new features in `tests/` directory

## Testing
Run tests with:
```bash
pytest
```

## Release Process
1. Update version in `setup.py`
2. Update CHANGELOG.md
3. Create a release tag: `git tag v1.0.0`
4. Push tag: `git push origin v1.0.0`
5. Create GitHub release with release notes

## Community
Join our Discord for support and collaboration: [Discord Link]
