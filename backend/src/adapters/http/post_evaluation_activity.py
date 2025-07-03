import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Path, status

from src.adapters.http.schemas import EvaluationRequest, EvaluationResponse
from src.application.ports.input.evaluation_activity_port import EvaluationActivityPort
from src.config.dependencies import get_evaluation_activity_service
from src.domain.entities.evaluation import ParticipantEvaluation, Rating

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/activity/{activity_id}/evaluation",
    summary="Submit an evaluation for a specific activity",
    status_code= status.HTTP_200_OK,
    response_model= EvaluationResponse,
    responses= {
        status.HTTP_200_OK: {
            "description": "Evaluation submitted successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Activity not found with the provided identifier."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Server responded with an unknown error."
        },
    },
)
async def post_activity_evaluation(
    evaluation_request: EvaluationRequest,
    activity_id: Annotated[UUID, Path(title="The identifier of the actvity")],
    participant_id: Annotated[
        UUID, Header(alias="X-Participant-Id", title="The identifier of the participant")
    ],
    evaluation_activity_service: EvaluationActivityPort = Depends(get_evaluation_activity_service),
):
    """Submit an evaluation for a given activity and participant."""

    log_data = {"activity_id": activity_id, "request": evaluation_request}

    try:
        logger.debug("[POST_ACTIVITY_EVALUATION] Request Received", extra=log_data)

        participant_evaluation = ParticipantEvaluation(
            participant_id=participant_id,
            ratings=[
                Rating(
                    principle_id=r.principle_id,
                    score=r.score,
                    comments=r.comments,
                ) for r in evaluation_request.ratings],
        )

        log_data["participant_evaluation"] = participant_evaluation
        logger.debug("[POST_ACTIVITY_EVALUATION] Data Mounted", extra=log_data)

        evaluation = await evaluation_activity_service.execute(
            activity_id, participant_evaluation
        )

    except ReferenceError as error:
        raise handle_not_found(error) from error

    except Exception as error:
        log_data["error"] = str(error)
        raise handle_unexpected_error(log_data, error) from error

    return EvaluationResponse(
        activity_id=str(activity_id),
        evaluation_id=str(evaluation.id),
    )

def handle_not_found(error: ReferenceError) -> HTTPException:
    """Handle the case when an activity is not found."""

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Activity not found: {error}"
    )

def handle_unexpected_error(log_data: dict, error: Exception) -> HTTPException:
    """Handle unexpected errors, logging them."""

    logger.exception("[POST_ACTIVITY_EVALUATION] Unexpected error", extra=log_data)

    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Unexpected error occurred: {error}"
    )
