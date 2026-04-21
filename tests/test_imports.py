from src.videosong.app import run


def test_run_symbol_exists() -> None:
    assert callable(run)
