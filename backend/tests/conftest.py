"""Shared test fixtures for CropFolio tests."""

import pytest

from app.domain.crops import MYANMAR_CROPS, CropProfile


@pytest.fixture
def rice() -> CropProfile:
    """Rice crop profile fixture."""
    return MYANMAR_CROPS["rice"]


@pytest.fixture
def black_gram() -> CropProfile:
    """Black gram crop profile fixture."""
    return MYANMAR_CROPS["black_gram"]


@pytest.fixture
def sesame() -> CropProfile:
    """Sesame crop profile fixture."""
    return MYANMAR_CROPS["sesame"]


@pytest.fixture
def all_crops() -> list[CropProfile]:
    """All Myanmar crop profiles."""
    return list(MYANMAR_CROPS.values())


@pytest.fixture
def three_crops(
    rice: CropProfile,
    black_gram: CropProfile,
    sesame: CropProfile,
) -> list[CropProfile]:
    """Three diversified crops: rice + pulse + oilseed."""
    return [rice, black_gram, sesame]
