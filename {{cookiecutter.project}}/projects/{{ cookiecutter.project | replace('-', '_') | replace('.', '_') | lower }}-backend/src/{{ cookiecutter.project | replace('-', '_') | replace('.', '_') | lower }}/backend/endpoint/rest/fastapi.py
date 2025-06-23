from fastapi import APIRouter
from {{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.backend.leaderboard.rest.fastapi import router as leaderboard_router

endpoint = APIRouter(prefix="/api/v1")

