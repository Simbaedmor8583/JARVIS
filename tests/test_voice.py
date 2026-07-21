from pathlib import Path

import pytest

from main import _parse_args
from voice.speaker import Speaker, _clean_for_speech


def test_speech_cleanup_removes_markdown_and_urls():
    text = _clean_for_speech("**Status:** [report](https://example.com) is ready.")
    assert text == "Status: report is ready."


def test_skip_model_preload_flag():
    assert _parse_args(["--skip-model-preload"]).skip_model_preload is True


def test_speaker_falls_back_to_piper(monkeypatch, tmp_path):
    monkeypatch.setattr("voice.speaker.Config.EDGE_TTS_ENABLED", True)
    speaker = Speaker.__new__(Speaker)
    speaker.last_engine = ""
    speaker._stop = type("Stop", (), {"is_set": lambda self: False})()

    paths = iter([tmp_path / "edge.mp3", tmp_path / "piper.wav"])
    monkeypatch.setattr(speaker, "_temp_path", lambda suffix: Path(next(paths)))

    async def fail_edge(text, path):
        raise RuntimeError("HTTP 403")

    def synth_piper(text, path):
        path.write_bytes(b"RIFF" + b"0" * 64)

    monkeypatch.setattr(speaker, "_synth_edge", fail_edge)
    monkeypatch.setattr(speaker, "_synth_piper", synth_piper)

    output = speaker._synthesize("hello")
    assert output.name == "piper.wav"
    assert speaker.last_engine == "piper"


def test_wakeword_process_returns_real_model_score():
    import numpy as np
    from voice.wakeword import WakeWordEngine

    engine = WakeWordEngine(model_name="hey_jarvis", threshold=0.5)
    engine._model = type(
        "Model",
        (),
        {"predict": lambda self, _audio: {"hey_jarvis": 0.73}},
    )()
    assert engine.process(np.zeros(1280, dtype=np.int16)) == pytest.approx(0.73)
