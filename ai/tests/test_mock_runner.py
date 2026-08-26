"""Tests for AI pipeline interfaces and mock runner (DESIGN.md §33.2, §35)."""

import uuid

from ai.pipeline.runner import MockPipelineRunner, PipelineRunner


def test_mock_pipeline_runner_protocol() -> None:
    runner: PipelineRunner = MockPipelineRunner()
    topic_id = uuid.uuid4()
    run_id = runner.run_topic_discovery(topic_id)
    assert isinstance(run_id, uuid.UUID)
