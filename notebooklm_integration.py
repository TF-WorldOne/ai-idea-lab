"""
NotebookLM Enterprise Integration Module
=========================================
Exports AI Idea Lab discussions to NotebookLM Enterprise for
audio summaries and interactive Q&A.
"""

import os
import json
import requests
from typing import Optional, Dict, Any
from datetime import datetime

# Try to import Google Auth
try:
    import google.auth
    import google.auth.transport.requests
    GOOGLE_AUTH_AVAILABLE = True
except ImportError:
    GOOGLE_AUTH_AVAILABLE = False


class NotebookLMClient:
    """Client for interacting with NotebookLM Enterprise API."""
    
    def __init__(
        self,
        project_number: Optional[str] = None,
        region: str = "us"
    ):
        """
        Initialize NotebookLM client.
        
        Args:
            project_number: GCP project number (not project ID)
            region: API region - "us", "eu", or "global"
        """
        self.project_number = project_number or os.getenv("GCP_PROJECT_NUMBER", "")
        self.region = region
        self.base_url = f"https://{region}-discoveryengine.googleapis.com/v1alpha"
        self._credentials = None
        self._token = None
    
    def _get_access_token(self) -> str:
        """Get access token for API authentication."""
        if not GOOGLE_AUTH_AVAILABLE:
            raise RuntimeError(
                "google-auth library not installed. "
                "Run: pip install google-auth google-auth-oauthlib"
            )
        
        if self._credentials is None:
            self._credentials, _ = google.auth.default(
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
        
        # Refresh if needed
        request = google.auth.transport.requests.Request()
        self._credentials.refresh(request)
        
        return self._credentials.token
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make authenticated API request."""
        url = f"{self.base_url}/projects/{self.project_number}/locations/{self.region}{endpoint}"
        
        headers = {
            "Authorization": f"Bearer {self._get_access_token()}",
            "Content-Type": "application/json"
        }
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json() if response.text else {}
            
        except requests.exceptions.HTTPError as e:
            error_detail = ""
            try:
                error_detail = e.response.json()
            except:
                error_detail = e.response.text
            raise RuntimeError(f"API Error: {e.response.status_code} - {error_detail}")
    
    def create_notebook(self, title: str) -> Dict[str, Any]:
        """
        Create a new NotebookLM notebook.
        
        Args:
            title: Display name for the notebook
            
        Returns:
            Notebook resource with 'name' (ID) and other metadata
        """
        data = {"title": title}
        return self._make_request("POST", "/notebooks", data)
    
    def add_text_source(
        self,
        notebook_id: str,
        title: str,
        content: str
    ) -> Dict[str, Any]:
        """
        Add a text source to an existing notebook.
        
        Args:
            notebook_id: The notebook resource name/ID
            title: Display name for this source
            content: The text content to add
            
        Returns:
            Source resource metadata
        """
        # Extract notebook ID from full resource name if needed
        if "/" in notebook_id:
            notebook_id = notebook_id.split("/")[-1]
        
        data = {
            "source": {
                "displayName": title,
                "inlineSource": {
                    "content": content,
                    "mimeType": "text/plain"
                }
            }
        }
        
        return self._make_request("POST", f"/notebooks/{notebook_id}/sources", data)
    
    def list_notebooks(self, page_size: int = 20) -> Dict[str, Any]:
        """List recently accessed notebooks."""
        return self._make_request("GET", f"/notebooks?pageSize={page_size}")


def format_discussion_for_export(
    topic: str,
    discussion_history: list,
    summary: str,
    include_metadata: bool = True
) -> str:
    """
    Format discussion history for NotebookLM export.
    
    Args:
        topic: The discussion topic
        discussion_history: List of discussion messages
        summary: The facilitator's summary
        include_metadata: Whether to include export metadata
        
    Returns:
        Formatted text content for NotebookLM
    """
    lines = []
    
    # Header
    if include_metadata:
        lines.append(f"# AI Idea Lab Discussion Export")
        lines.append(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append("")
    
    # Topic
    lines.append(f"## Topic")
    lines.append(topic)
    lines.append("")
    
    # Discussion
    lines.append("## Discussion")
    lines.append("")
    
    for msg in discussion_history:
        model = msg.get("model", "Unknown")
        personality = msg.get("personality", "")
        content = msg.get("content", "")
        
        if personality:
            lines.append(f"### {model} ({personality})")
        else:
            lines.append(f"### {model}")
        
        lines.append(content)
        lines.append("")
    
    # Summary
    lines.append("## Summary")
    lines.append(summary)
    
    return "\n".join(lines)


def export_discussion_to_notebooklm(
    topic: str,
    discussion_history: list,
    summary: str,
    project_number: Optional[str] = None,
    region: str = "us"
) -> Dict[str, Any]:
    """
    Export an AI Idea Lab discussion to NotebookLM Enterprise.
    
    Args:
        topic: The discussion topic
        discussion_history: List of discussion messages
        summary: The facilitator's summary
        project_number: GCP project number
        region: NotebookLM API region
        
    Returns:
        Dict with 'success', 'notebook_id', 'url', and 'error' keys
    """
    result = {
        "success": False,
        "notebook_id": None,
        "url": None,
        "error": None
    }
    
    try:
        # Initialize client
        client = NotebookLMClient(project_number=project_number, region=region)
        
        # Create notebook with topic as title
        notebook_title = f"AI Idea Lab: {topic[:50]}..."
        notebook = client.create_notebook(notebook_title)
        notebook_id = notebook.get("name", "").split("/")[-1]
        
        if not notebook_id:
            raise RuntimeError("Failed to get notebook ID from response")
        
        # Format and add discussion content
        content = format_discussion_for_export(topic, discussion_history, summary)
        client.add_text_source(notebook_id, "Discussion Export", content)
        
        # Build NotebookLM URL
        url = f"https://notebooklm.google.com/notebook/{notebook_id}"
        
        result["success"] = True
        result["notebook_id"] = notebook_id
        result["url"] = url
        
    except Exception as e:
        result["error"] = str(e)
    
    return result


# For testing
if __name__ == "__main__":
    # Test with sample data
    test_topic = "テスト議論トピック"
    test_history = [
        {"model": "GPT-4o", "personality": "創造者", "content": "テストメッセージ1"},
        {"model": "Claude Sonnet", "personality": "論理派", "content": "テストメッセージ2"},
    ]
    test_summary = "テストサマリー"
    
    # Format test
    formatted = format_discussion_for_export(test_topic, test_history, test_summary)
    print("Formatted content:")
    print(formatted)
