# Contributing to lukin e nimi kon

Thank you for your interest in contributing to the lukin e nimi kon project! 🎉

## 🤝 How to Contribute

### Reporting Issues
- Check existing issues before creating a new one
- Use a clear and descriptive title
- Include steps to reproduce the issue
- Provide example input text and expected vs actual output
- Specify your operating system and Python version

### Suggesting Enhancements
- Use the GitHub issue tracker to suggest new features
- Explain why this enhancement would be useful
- Provide examples of how it would work

### Pull Requests
1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Add tests if applicable
5. Update documentation if needed
6. Commit your changes (`git commit -am 'Add your feature'`)
7. Push to your branch (`git push origin feature/your-feature-name`)
8. Create a Pull Request

## 📋 Development Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use clear, descriptive variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and under 50 lines when possible
- Use type hints where appropriate

### Testing
- Test your changes with various cipher types
- Include both English and French text examples
- Test edge cases (short text, no text, special characters)
- Verify that existing functionality still works

### Documentation
- Update README.md if you add new features
- Add docstrings to new functions
- Include examples in your code comments
- Update command-line help text if needed

## 🎯 Areas for Contribution

### High Priority
- Additional language support (German, Spanish, Italian)
- Performance improvements for large texts
- Better handling of punctuation and special characters
- Unit tests and test coverage

### Medium Priority
- Vigenère cipher support
- Statistical analysis reports
- Web interface using Flask/Django
- Better visualization options

### Low Priority
- Machine learning enhancements
- Support for historical cipher variants
- Mobile app version
- Integration with external APIs

## 📝 Commit Message Guidelines

Use clear and meaningful commit messages:
- `feat: add support for German language analysis`
- `fix: handle empty input text gracefully`
- `docs: update README with new examples`
- `test: add unit tests for Caesar cipher detection`
- `refactor: simplify frequency analysis logic`

## 🧪 Setting Up Development Environment

1. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/lukin-e-nimi-kon.git
   cd lukin-e-nimi-kon
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run tests:
   ```bash
   python cipher_analyzer.py --demo
   python cipher_analyzer.py -f test_french_cipher.txt
   ```

## 🔍 Code Review Process

- All pull requests require review before merging
- Reviewers will check for code quality, functionality, and documentation
- Be responsive to feedback and willing to make changes
- Maintainers reserve the right to edit your PR before merging

## 📚 Learning Resources

If you're new to cryptanalysis or frequency analysis:
- [Frequency Analysis on Wikipedia](https://en.wikipedia.org/wiki/Frequency_analysis)
- [Classical Cryptography Techniques](https://crypto.stanford.edu/pbc/notes/crypto/classical.html)
- [Python Cryptography Tutorials](https://cryptography.io/en/latest/)

## 🏆 Recognition

Contributors will be recognized in the following ways:
- Listed in the README.md file
- Mentioned in release notes for significant contributions
- Given appropriate credit in code comments

## ❓ Questions?

If you have questions about contributing:
- Open a GitHub issue with the "question" label
- Check existing issues and pull requests for similar discussions
- Review the project documentation thoroughly

Thank you for helping make lukin e nimi kon better! 🚀 