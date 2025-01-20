from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.tavily import TavilyTools
from phi.tools.crawl4ai_tools import Crawl4aiTools
from phi.workflow import Workflow, RunResponse, RunEvent
from phi.storage.workflow.sqlite import SqlWorkflowStorage
from phi.utils.log import logger
import os
from dotenv import load_dotenv
from pydantic import PrivateAttr
from typing import Iterator, List, Dict


# Load environment variables
load_dotenv()

# Access environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
PHI_API_KEY = os.getenv("PHI_API_KEY")

# Define the workflow class
class EclipseAgentWorkflow(Workflow):
    agent: Agent = Agent(
        model=OpenAIChat(id="gpt-4o"),
        tools=[TavilyTools(), Crawl4aiTools(max_length=None)],
        description="AI agent assisting developers with 'eclipse', the L2 layer solution, providing relevant code samples where neccesary.",
        instructions=[
            "For a given query, search for the top 3 links.",
            "Then read each URL and scrape them for information; if a URL isn't available, ignore it.",
            "Analyze gathered information and prepare a comprehensive reply.",
        ],
        markdown=True,
        show_tool_calls=True,
        add_datetime_to_instructions=True,
        debug=True,
        monitoring=True
    )

    # Define conversation_history as a private attribute
    _conversation_history: List[Dict[str, str]] = PrivateAttr(default_factory=list)

    def run(self, query: str, use_cache: bool = True) -> Iterator[RunResponse]:
        logger.info(f"Processing query: {query}")

        # Load cached responses if available
        if use_cache and "responses" in self.session_state:
            logger.info("Checking for cached response.")
            for cached in self.session_state["responses"]:
                if cached["query"] == query:
                    logger.info("Found cached response.")
                    yield RunResponse(content=cached["response"], event=RunEvent.workflow_completed)
                    return

        # Append conversation history to context
        conversation_context = "\n".join(
            [f"User: {entry['query']}\nAgent: {entry['response']}" for entry in self._conversation_history]
        )
        extended_query = f"{conversation_context}\nUser: {query}\nAgent:" if conversation_context else query

        # Generate new response
        response = self.agent.run(extended_query)

        # Save the new interaction in conversation history
        self._conversation_history.append({"query": query, "response": response.content})

        # Cache the new response
        if "responses" not in self.session_state:
            self.session_state["responses"] = []
        self.session_state["responses"].append({"query": query, "response": response.content})

        yield RunResponse(content=response.content, event=RunEvent.workflow_completed)

