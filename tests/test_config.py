import sys
from os import path
from pathlib import Path

import pytest

from app.config import config


class TestResourcePath:
    """resource_path のリソース解決を検証する"""

    def test_uses_cwd_when_not_bundled(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """バンドルされていない場合は getcwd を基点に解決する"""
        monkeypatch.delattr(sys, "_MEIPASS", raising=False)
        monkeypatch.setattr(config, "getcwd", lambda: "/work")

        assert config.resource_path("images") == path.join("/work", "images")

    def test_uses_meipass_when_bundled(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """バンドルされている場合は _MEIPASS を基点に解決する"""
        monkeypatch.setattr(sys, "_MEIPASS", "/bundle", raising=False)

        assert config.resource_path("images") == path.join("/bundle", "images")


class TestUserDataDir:
    """user_data_dir の書き込み領域を検証する"""

    def test_creates_dir_under_appdata(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """APPDATA 配下に MazeGame ディレクトリを作成する"""
        monkeypatch.setenv("APPDATA", str(tmp_path))

        result = config.user_data_dir()

        expected = path.join(str(tmp_path), "MazeGame")
        assert result == expected
        assert path.isdir(expected)

    def test_falls_back_to_home_without_appdata(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """APPDATA が無ければホームディレクトリを基点にする"""
        monkeypatch.delenv("APPDATA", raising=False)
        monkeypatch.setattr("os.path.expanduser", lambda _: str(tmp_path))

        result = config.user_data_dir()

        expected = path.join(str(tmp_path), "MazeGame")
        assert result == expected
        assert path.isdir(expected)
