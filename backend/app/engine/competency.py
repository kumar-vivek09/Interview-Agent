class CompetencyGraph:
    # A logical narrative flow of topics based on the curriculum.
    NARRATIVE_FLOW = [
        7,  # Embeddings Explained
        8,  # Vector Databases
        10, # Retrieval & Matching Engine
        11, # RAG End-to-End
        16, # Chatbot Backend
        21, # LangChain Agents
        22, # Multi-Agent Orchestration
        23, # MCP
        24, # Agentic Integration
        28, # Docker & Kubernetes Deployment
        29, # Monitoring, Logging
        30, # Production Readiness
        31  # Capstone
    ]

    @classmethod
    def get_next_topic(cls, current_day: int, available_days: list[int]) -> int:
        """
        Returns the next logical day in the narrative flow that is also in available_days.
        """
        try:
            current_index = cls.NARRATIVE_FLOW.index(current_day)
        except ValueError:
            current_index = -1
        
        for day in cls.NARRATIVE_FLOW[current_index + 1:]:
            if day in available_days:
                return day
        
        # Fallback if no matching downstream topics are available
        for day in available_days:
            if day not in cls.NARRATIVE_FLOW[:current_index + 1]:
                return day
        
        return available_days[0] if available_days else -1
