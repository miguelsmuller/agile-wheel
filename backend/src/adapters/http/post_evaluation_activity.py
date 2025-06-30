import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, Path, status
from fastapi.responses import JSONResponse
from src.adapters.http.schemas import EvaluationRequest, EvaluationResponse
from src.application.ports.input.evaluation_activity_port import EvaluationActivityPort
from src.config.dependencies import get_evaluation_activity_service
from src.domain.entities.evaluation import ParticipantEvaluation, Rating

logger = logging.getLogger(__name__)
logger_prefix = "[POST_ACTIVITY_EVALUATION]"

endpoint = APIRouter()
router_params = {
    "status_code": status.HTTP_200_OK,
    "responses": {
        status.HTTP_200_OK: {"description": "Close activity successfully."},
        status.HTTP_404_NOT_FOUND: {"description": "Activity not found."},
    },
    "response_model": EvaluationResponse,
}


@endpoint.post("/activity/{activity_id}/evaluation", **router_params)
async def post_activity_evaluation(
    evaluation_request: EvaluationRequest,
    activity_id: Annotated[UUID, Path(title="The identifier of the actvity")],
    participant_id: Annotated[
        UUID, Header(alias="X-Participant-Id", title="The identifier of the participant")
    ],
    evaluation_activity_service: EvaluationActivityPort = Depends(get_evaluation_activity_service),
):
    participant_evaluation = ParticipantEvaluation(
        participant_id=participant_id,
        ratings=[
            Rating(
                principle_id=r.principle_id,
                score=r.score,
                comments=r.comments,
            ) for r in evaluation_request.ratings],
    )

    try:
        logger.debug("%s Request: %s", logger_prefix, evaluation_request)
        evaluation = await evaluation_activity_service.execute(
            activity_id, participant_evaluation
        )
    except Exception as e:
        return JSONResponse({"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    return EvaluationResponse(
        activity_id=str(activity_id),
        evaluation_id=str(evaluation.id),
    )
