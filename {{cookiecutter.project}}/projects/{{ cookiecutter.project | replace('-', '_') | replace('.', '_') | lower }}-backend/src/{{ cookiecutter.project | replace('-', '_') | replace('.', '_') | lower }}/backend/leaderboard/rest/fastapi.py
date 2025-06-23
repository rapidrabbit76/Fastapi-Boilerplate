from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Query, status

from {{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.backend.container import TetrowebContainer
from {{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.backend.leaderboard.use_case import LeaderboardUseCase

# from ..dtos.response import
from ..dtos.request import CreateLeaderBoardRequest
from ..dtos.response import LeaderBoardResponse

router = APIRouter()

get_exponse_use_case = Provide[TetrowebContainer.leaderboard.use_case]


@router.get(
    "",
    response_model=LeaderBoardResponse,
)
@inject
async def get_scores(
    use_case: LeaderboardUseCase = Depends(get_exponse_use_case),
    game: str = Query(..., description="Game name to filter the leaderboard"),
    tapk: int = Query(100, description="Number of top scores to return", ge=10, le=1000),
):
    results = await use_case.get_leader_board_by_game(game=game, topk=tapk)
    return LeaderBoardResponse(
        status=status.HTTP_200_OK,
        message="Successfully retrieved leaderboard",
        data=results,
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_scores(
    use_case: LeaderboardUseCase = Depends(get_exponse_use_case),
    payload: CreateLeaderBoardRequest = Body(),
):
    use_case.summit_score(payload=payload)
