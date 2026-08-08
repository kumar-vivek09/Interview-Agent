from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uuid

from app.session.manager import session_manager
from app.profiler.candidate_profiler import candidate_profiler
from app.curriculum.curriculum_retriever import curriculum_retriever
from app.engine.planner import planner
from app.llm.interviewer import interviewer
from app.llm.evaluator import evaluator
from app.llm.feedback import feedback_generator
from app.evidence.builder import evidence_builder
from app.evidence.store import evidence_store
from app.models.interview import InterviewState, TopicRecord
from app.models.question import QuestionContext

router = APIRouter()

class StartRequest(BaseModel):
    sessionId: str
    candidate: Dict[str, Any]

class TurnRequest(BaseModel):
    sessionId: str
    message: str

@router.post("/interview")
async def handle_interview(req: Dict[str, Any]):
    session_id = req.get("sessionId")
    if not session_id:
        raise HTTPException(status_code=400, detail="sessionId is required")
        
    candidate_data = req.get("candidate")
    message = req.get("message")
    
    # 1. Start Interview
    if candidate_data:
        # Generate initial state
        candidate_id = candidate_data.get("member", {}).get("id")
        if not candidate_id:
            # Try to register candidate in memory if it's dynamic, for now assume it's in our dataset
            raise HTTPException(status_code=400, detail="Valid candidate data required")
            
        profile = candidate_profiler.get_candidate_profile(candidate_id)
        
        # Initialize required days from curriculum modules
        required = []
        for m in curriculum_retriever.get_all_days():
            if m.type in ["BUILD", "AI_CORE", "SHIP_IT", "OPTIMIZE", "CAPSTONE"]:
                required.append(m.day)
                
        state = InterviewState(
            session_id=session_id,
            candidate_id=candidate_id,
            candidate_profile=profile,
            required_days=required
        )
        
        session_manager.create_session(session_id, state)
        
        return {
            "reply": f"Welcome to the interview. Let's begin. I see you have {profile.experience} years of experience as a {profile.role}. Let's get started.",
            "done": False
        }
        
    # 2. Conversation Turn
    elif message:
        state = session_manager.get_session(session_id)
        if not state:
            raise HTTPException(status_code=404, detail="Session not found")
            
        # Record candidate answer
        state.transcript.append({"role": "candidate", "content": message})
        
        # Evaluate answer if there was a previous question
        if state.turn_count > 0 and state.current_topic:
            context_for_eval = {
                "phase": state.phase,
                "question": state.transcript[-2]["content"] if len(state.transcript) >= 2 else "UNKNOWN"
            }
            eval_result = evaluator.evaluate(message, context_for_eval)
            state.evaluations.append(eval_result)
            
            # Build and store evidence
            evidence_items = evidence_builder.build_from_evaluation(eval_result, state)
            state.evidence.extend(evidence_items)
            evidence_store.add_evidence(session_id, evidence_items)
            
        # Planner decides next step
        plan = planner.determine_next_action(state)
        
        if plan["action"] == "FINISH":
            # End Interview
            final_feedback = feedback_generator.generate_feedback({"candidate_profile": state.candidate_profile.model_dump()}, state.evidence)
            return {
                "reply": "Interview completed. Thank you for your time.",
                "done": True,
                "feedback": final_feedback.model_dump()
            }
            
        # Continue Interview
        decision = plan["decision"]
        is_follow_up = decision.get("is_follow_up", False)
        
        # Update State
        state.turn_count += 1
        state.question_count += 1
        if is_follow_up:
            state.follow_up_count += 1
        else:
            state.primary_question_count += 1
            if decision["day"] not in state.covered_days:
                state.covered_days.append(decision["day"])
        
        state.current_topic = TopicRecord(day=decision["day"], title=curriculum_retriever.get_topic_title(decision["day"]))
        state.current_question_id = f"Q-{uuid.uuid4().hex[:6]}"
        state.difficulty = decision["difficulty"]
        state.probe_type = decision["probe"].value
        
        # Build Context for LLM
        q_context = QuestionContext(
            candidate_role=state.candidate_profile.role,
            candidate_experience=state.candidate_profile.experience,
            phase=state.phase,
            question_count=state.question_count,
            covered_days=state.covered_days,
            remaining_required_days=[d for d in state.required_days if d not in state.covered_days],
            current_topic_day=state.current_topic.day,
            current_topic_title=state.current_topic.title,
            previous_answers=[{"question": state.transcript[-2]["content"], "answer": state.transcript[-1]["content"]} if len(state.transcript) >= 2 else {}],
            probe_type=state.probe_type,
            difficulty=state.difficulty
        )
        
        # Generate Question
        reply = interviewer.generate_question(q_context.model_dump())
        state.transcript.append({"role": "interviewer", "content": reply})
        
        session_manager.update_session(session_id, state)
        
        # In debug mode, you can append decision to the response or pass it as metadata.
        # But per spec, we just return reply and done.
        return {
            "reply": reply,
            "done": False,
            "debug_decision": decision # Included for the UI debug panel!
        }
        
    else:
        raise HTTPException(status_code=400, detail="Invalid request")
