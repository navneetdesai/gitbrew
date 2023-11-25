# Gitbrew: Your LLM-Powered GitHub Companion 🚀✨

Welcome to Gitbrew, the innovative tool that harnesses the power of language models to streamline your GitHub experience. Gitbrew is designed to assist developers in managing repositories, handling issues, reviewing pull requests, and generating beautiful READMEs with ease.

### Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction👋
Gitbrew is a command-line application that simplifies your GitHub workflow. It uses advanced language models to interpret natural language commands, generate git commands, handle GitHub issues, and create comprehensive READMEs for your projects. Gitbrew is your go-to utility for a more efficient and intelligent way to interact with GitHub.

## Features🌟
- **Command Handling**: Process user input to generate and execute git commands safely with user confirmation.
- **Issue Management**: Manage GitHub issues by listing, creating, finding duplicates, and identifying similar issues.
- **Pull Request Review**: Automate the review of GitHub pull requests with insightful comments and suggestions.
- **Readme Generation**: Generate visually appealing READMEs with structured content and visual elements.
- **Interactive Shell Interface**: Use Gitbrew's interactive CLI to perform a variety of GitHub-related tasks.

## Technologies
Gitbrew is built with a variety of technologies and integrates with several APIs to provide its functionalities:
- **Python 3.9**: The primary programming language used for development.
- **OpenAI API**: For interacting with language models to generate text and commands.
- **GitHub API**: To fetch repository contents, manage issues, pull requests, and more.
- **Cohere API**: Another language model service used alongside OpenAI.
- **Poetry**: For dependency management and packaging of the Python project.
- **PyInquirer**: To create interactive command-line prompts.
- **Rich**: To enhance console output with rich text and formatting.

## Installation🛠️📦 
```bash
pip install gitbrew
```

## Usage💻
1. **Run `gitbrew` in your Terminal:**
   ```bash
   gitbrew
   ```
   This will launch the Gitbrew interactive shell.
2. Provide the API keys for GitHub, openai, pinecone etc
3. Start using Gitbrew!

## Contributing 🤝🌐
Contributions and feature requests are welcome! 

### Issues and Feature Requests
Please use the [issue tracker](https://github.com/navneetdesai/gitbrew/issues) to report any bugs or file feature requests.

### Development
1. Fork and clone the repository.
2. Make your changes and commit them with a descriptive commit message.
3. Install pre-commit hooks by running `pre-commit install`.
4. Push your changes to your fork and submit a pull request.


---

Thank you for checking out Gitbrew! By using Gitbrew, you're taking a step towards a more efficient and enjoyable GitHub experience. Let's brew some code together! ☕👨‍💻👩‍💻