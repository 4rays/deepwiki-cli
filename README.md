# DeepWiki CLI

A command-line tool for querying [DeepWiki](https://deepwiki.com) documentation for any GitHub repository.

DeepWiki provides AI-generated documentation for open source repositories. This CLI lets you explore documentation structure, read contents, or ask questions about any repository directly from your terminal.

## Installation

### Using uvx (recommended)

```bash
uvx deepwiki-cli --help
```

### Using pip

```bash
pip install deepwiki-cli
```

### From source

```bash
git clone https://github.com/4rays/deepwiki-cli
cd deepwiki-cli
uv sync
uv run deepwiki-cli --help
```

## Usage

### Get Documentation Structure

View the table of contents for a repository's documentation:

```bash
deepwiki-cli structure facebook/react
```

Output:
```
1. Overview
  1.1 Repository Purpose
  1.2 Key Technologies
2. Architecture
  2.1 Fiber Reconciler
  2.2 Scheduler
...
```

### Get Full Documentation

Retrieve the complete documentation contents:

```bash
deepwiki-cli contents vercel/next.js
```

Note: This may return a large amount of text for repositories with extensive documentation.

### Ask Questions

Ask natural language questions about a repository:

```bash
deepwiki-cli ask facebook/react "What is Fiber?"
```

Output:
```
Fiber is React's reconciliation algorithm introduced in React 16...
```

More examples:

```bash
deepwiki-cli ask langchain-ai/langchain "How do I create a chain?"
deepwiki-cli ask pytorch/pytorch "What optimizers are available?"
deepwiki-cli ask microsoft/vscode "How does the extension API work?"
```

## Commands

| Command | Description |
|---------|-------------|
| `deepwiki-cli structure <repo>` | Get documentation structure (table of contents) |
| `deepwiki-cli contents <repo>` | Get full documentation contents |
| `deepwiki-cli ask <repo> "<question>"` | Ask a question about the repository |
| `deepwiki-cli --version` | Show version |
| `deepwiki --help` | Show help |

## Repository Format

All commands expect the repository in `owner/repo` format:

- `facebook/react`
- `vercel/next.js`
- `langchain-ai/langchain`
- `microsoft/typescript`

## Requirements

- Python 3.10+

## License

MIT
