from src.adapters.storage import (
    load_json,
    load_transcript,
    save_json,
    save_processed_data,
    save_raw_data,
    save_transcript,
    save_transcript_payload,
)
from src.app.core.config import get_settings


def test_save_transcript_writes_json_payload(tmp_path) -> None:
    path = tmp_path / "transcript.json"
    payload = {
        "video_id": "abc123",
        "transcript": "Clean transcript",
        "status": "available",
    }

    save_transcript(str(path), payload)

    assert path.exists()
    assert path.read_text(encoding="utf-8") == (
        '{\n'
        '  "video_id": "abc123",\n'
        '  "transcript": "Clean transcript",\n'
        '  "status": "available"\n'
        '}'
    )


def test_load_transcript_reads_json_payload(tmp_path) -> None:
    path = tmp_path / "transcript.json"
    path.write_text(
        '{\n'
        '  "video_id": "missing-video",\n'
        '  "transcript": "",\n'
        '  "status": "missing"\n'
        '}',
        encoding="utf-8",
    )

    payload = load_transcript(str(path))

    assert payload == {
        "video_id": "missing-video",
        "transcript": "",
        "status": "missing",
    }


def test_report_storage_uses_configured_reports_dir(monkeypatch, tmp_path) -> None:
    reports_dir = tmp_path / "data" / "reports"
    monkeypatch.setenv("REPORTS_DIR", str(reports_dir))
    get_settings.cache_clear()

    path = reports_dir / "report_20260529.json"
    save_json(path, {"gameweek": 38})

    assert load_json(path) == {"gameweek": 38}
    assert path.parent == reports_dir
    get_settings.cache_clear()


def test_raw_processed_and_transcript_storage_use_configured_data_dirs(monkeypatch, tmp_path) -> None:
    data_dir = tmp_path / "data"
    monkeypatch.setenv("DATA_DIR", str(data_dir))
    get_settings.cache_clear()

    raw_path = save_raw_data("fixtures.json", {"fixtures": []})
    processed_path = save_processed_data("predictions.csv", {"rows": []})
    transcript_path = save_transcript_payload(
        "run_001.json",
        {
            "video_id": "run_001",
            "transcript": "Cached transcript",
            "status": "available",
        },
    )

    assert raw_path == data_dir / "raw" / "fixtures.json"
    assert processed_path == data_dir / "processed" / "predictions.csv"
    assert transcript_path == data_dir / "transcripts" / "run_001.json"
    assert load_json(raw_path) == {"fixtures": []}
    assert load_json(processed_path) == {"rows": []}
    assert load_transcript(str(transcript_path))["transcript"] == "Cached transcript"
    get_settings.cache_clear()
