from app.models.interview import InterviewState
from app.engine.probes import QuestionType, ProbeType
from app.engine.competency import CompetencyGraph
import random

class QuestionDecisionEngine:
    def decide(self, state: InterviewState) -> dict:
        """
        Decides the what: Topic Selection, Probe Selection, Difficulty, Question Type, and Reason.
        """
        # Are we doing a follow-up or a new topic?
        is_follow_up = False
        if state.turn_count > 0 and state.follow_up_count < 2 and state.current_topic:
            # Random chance to follow up, or follow up if last evaluation was weak
            if random.random() > 0.3:
                is_follow_up = True
        
        if is_follow_up:
            probe = random.choice([ProbeType.WHY, ProbeType.TRADEOFF, ProbeType.DEBUGGING, ProbeType.ALTERNATIVE])
            q_type = QuestionType.DEBUGGING if probe == ProbeType.DEBUGGING else QuestionType.TRADEOFF
            reason = f"Candidate provided an answer on {state.current_topic.title}. Probing deeper on {probe.value.lower()}."
            day = state.current_topic.day
            title = state.current_topic.title
            
            return {
                "is_follow_up": True,
                "day": day,
                "title": title,
                "difficulty": state.difficulty,
                "probe": probe,
                "q_type": q_type,
                "reason": reason
            }
        else:
            # New topic
            available_days = state.required_days
            remaining_days = [d for d in available_days if d not in state.covered_days]
            
            if remaining_days:
                next_day = CompetencyGraph.get_next_topic(
                    state.current_topic.day if state.current_topic else 0, 
                    remaining_days
                )
            else:
                # If all required are covered, just pick a random narrative flow topic not covered
                all_narrative = [d for d in CompetencyGraph.NARRATIVE_FLOW if d not in state.covered_days]
                next_day = all_narrative[0] if all_narrative else 31 # default to capstone
                
            q_type = QuestionType.CONCEPT
            if next_day >= 20:
                q_type = QuestionType.SYSTEM_DESIGN
            if next_day >= 28:
                q_type = QuestionType.PRODUCTION
            if next_day == 31:
                q_type = QuestionType.CAPSTONE
                
            probe = ProbeType.CLARIFY
            
            # TODO: We would use curriculum_retriever to get title, for now assume we get it elsewhere or pass it
            
            return {
                "is_follow_up": False,
                "day": next_day,
                "title": f"Topic {next_day}", # This will be hydrated by planner
                "difficulty": state.difficulty,
                "probe": probe,
                "q_type": q_type,
                "reason": f"Transitioning to new topic in narrative flow: Day {next_day}."
            }

decision_engine = QuestionDecisionEngine()
