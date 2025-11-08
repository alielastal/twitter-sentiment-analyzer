# Contributing to Twitter Sentiment Analyzer

First off, thank you for considering contributing to Twitter Sentiment Analyzer! 🎉

## 🌟 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include screenshots if applicable**
- **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List any alternatives you've considered**

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Follow the coding style** used in the project
3. **Write clear commit messages**
4. **Test your changes** thoroughly
5. **Update documentation** if needed
6. **Submit a pull request**

## 🔧 Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/twitter-sentiment-analyzer.git
cd twitter-sentiment-analyzer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your Twitter API keys

# Run the app
streamlit run app.py
```

## 📝 Coding Guidelines

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and concise
- Use type hints where appropriate

### Code Structure

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of what the function does

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value
    """
    # Implementation
    return True
```

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests when relevant

Examples:
```
Add support for French language
Fix timeout error in data fetching
Update README with installation instructions
```

## 🧪 Testing

Before submitting a pull request:

1. **Test manually** with different scenarios
2. **Check for errors** in the console/logs
3. **Test with both English and Arabic** interfaces
4. **Verify all features work** as expected

## 🌍 Adding New Languages

To add support for a new language:

1. Open `config/translations.py`
2. Add your language code to the `TRANSLATIONS` dictionary
3. Translate all keys from English version
4. Update `app.py` to include the new language in the selector
5. Test thoroughly

Example:
```python
TRANSLATIONS = {
    'en': { ... },
    'ar': { ... },
    'fr': {  # French
        'app_title': '🐦 Analyseur de Sentiments Twitter',
        # ... rest of translations
    }
}
```

## 📚 Documentation

- Update README.md for major changes
- Add comments for complex logic
- Update UPDATES.md for new features
- Include examples where helpful

## 🎯 Priority Areas

We're especially interested in contributions for:

- **Accuracy improvements** for Arabic sentiment analysis
- **New analysis methods** and algorithms
- **Performance optimizations**
- **UI/UX enhancements**
- **Additional language support**
- **Bug fixes** and error handling
- **Documentation improvements**
- **Test coverage**

## ⚠️ Important Notes

### Security

- **NEVER commit** API keys or credentials
- Always use `.env` for sensitive data
- Review `.gitignore` before committing
- Report security vulnerabilities privately

### API Keys

- Do not include real API keys in examples
- Use placeholder values in documentation
- Remind users to get their own keys

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism gracefully
- Focus on what is best for the community

## 🤝 Getting Help

- Check existing [Issues](../../issues)
- Read the [Documentation](README.md)
- Ask questions in [Discussions](../../discussions)

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to Twitter Sentiment Analyzer!** 🙏

Every contribution, no matter how small, is valued and appreciated.
