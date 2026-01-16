"""MCP client wrapper for DeepWiki API."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from mcp import ClientSession, types
from mcp.client.streamable_http import streamablehttp_client

# Suppress noisy SSE warnings from httpx-sse
logging.getLogger("httpx_sse").setLevel(logging.ERROR)
logging.getLogger("mcp.client.streamable_http").setLevel(logging.ERROR)

DEEPWIKI_MCP_URL = "https://mcp.deepwiki.com/mcp"


class DeepWikiError(Exception):
    """Base exception for DeepWiki errors."""

    pass


class ConnectionError(DeepWikiError):
    """Failed to connect to DeepWiki server."""

    pass


class ToolError(DeepWikiError):
    """Error from MCP tool execution."""

    pass


class DeepWikiClient:
    """Client for interacting with DeepWiki via MCP."""

    def __init__(self, base_url: str = DEEPWIKI_MCP_URL) -> None:
        self.base_url = base_url

    async def _call_tool(self, tool_name: str, arguments: dict[str, Any]) -> str:
        """Connect to DeepWiki and call a tool."""
        try:
            async with streamablehttp_client(self.base_url) as (
                read_stream,
                write_stream,
                _,
            ):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    result = await session.call_tool(tool_name, arguments)
                    return self._extract_text_content(result)
        except Exception as e:
            error_msg = str(e)
            if "connection" in error_msg.lower() or "timeout" in error_msg.lower():
                raise ConnectionError(
                    f"Failed to connect to DeepWiki server: {error_msg}"
                ) from e
            raise ToolError(f"Tool '{tool_name}' failed: {error_msg}") from e

    def _extract_text_content(self, result: types.CallToolResult) -> str:
        """Extract text content from tool result."""
        if result.isError:
            error_text = ""
            for content in result.content:
                if isinstance(content, types.TextContent):
                    error_text += content.text
            raise ToolError(error_text or "Unknown tool error")

        text_parts: list[str] = []
        for content in result.content:
            if isinstance(content, types.TextContent):
                text_parts.append(content.text)
        return "\n".join(text_parts)

    async def read_wiki_structure(self, repo_name: str) -> str:
        """Get the documentation structure (table of contents) for a repository.

        Args:
            repo_name: Repository in format "owner/repo" (e.g., "facebook/react")

        Returns:
            Formatted documentation structure
        """
        return await self._call_tool("read_wiki_structure", {"repoName": repo_name})

    async def read_wiki_contents(self, repo_name: str) -> str:
        """Get the full documentation contents for a repository.

        Args:
            repo_name: Repository in format "owner/repo" (e.g., "facebook/react")

        Returns:
            Full documentation content
        """
        return await self._call_tool("read_wiki_contents", {"repoName": repo_name})

    async def ask_question(self, repo_name: str, question: str) -> str:
        """Ask a question about a repository.

        Args:
            repo_name: Repository in format "owner/repo" (e.g., "facebook/react")
            question: Question to ask about the repository

        Returns:
            Answer to the question
        """
        return await self._call_tool(
            "ask_question", {"repoName": repo_name, "question": question}
        )


def run_async(coro: Any) -> Any:
    """Run an async coroutine synchronously."""
    return asyncio.run(coro)
