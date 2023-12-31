from fastapi import APIRouter
from app.utils.utils import import_routers

from app.repositories.studio_repository import StudioRepository

studio_repo = StudioRepository()
router = APIRouter()

import_routers(__name__)
