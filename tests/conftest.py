from __future__ import annotations

from pathlib import Path
from typing import Generator

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--run-browser",
        action="store_true",
        default=False,
        help="Run Selenium UI tests that require a browser",
    )


def _build_driver():
    pytest.importorskip("selenium")
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service as ChromeService

    pytest.importorskip("webdriver_manager")
    from webdriver_manager.chrome import ChromeDriverManager

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options,
    )


@pytest.fixture(scope="session")
def browser(request: pytest.FixtureRequest) -> Generator:
    if not request.config.getoption("--run-browser"):
        pytest.skip("Browser tests are disabled. Use --run-browser to enable.")

    driver = _build_driver()
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def local_login_page() -> Path:
    resources_dir = Path(__file__).parent / "resources"
    page = resources_dir / "login_page.html"
    if not page.exists():
        pytest.skip("Sample login page is missing; ensure repository files are intact.")
    return page
