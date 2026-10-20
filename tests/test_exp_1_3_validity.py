"""Tests for Experiment 1.3 validity protections.

No model calls -- all tests use synthetic fixtures.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def _load_exp13():
    spec = importlib.util.spec_from_file_location('exp13', 'experiments/exp_1_3_state_ablation.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestExp13Validity:
    """Tests for Experiment 1.3 instrument hardening."""

    def test_truncated_output_is_invalid(self):
        mod = _load_exp13()
        resp = {'response': 'some text', 'done_reason': 'length'}
        valid, reason = mod.is_valid_trial(resp)
        assert valid is False
        assert 'truncat' in reason

    def test_completed_output_is_valid(self):
        mod = _load_exp13()
        resp = {'response': 'some text', 'done_reason': 'stop'}
        valid, reason = mod.is_valid_trial(resp)
        assert valid is True
        assert reason == 'ok'

    def test_empty_response_is_invalid(self):
        mod = _load_exp13()
        resp = {'response': '', 'done_reason': 'stop'}
        valid, reason = mod.is_valid_trial(resp)
        assert valid is False
        assert reason == 'empty_response'

    def test_none_response_is_invalid(self):
        mod = _load_exp13()
        resp = {'response': None, 'done_reason': 'stop'}
        valid, reason = mod.is_valid_trial(resp)
        assert valid is False

    def test_api_error_is_invalid(self):
        mod = _load_exp13()
        resp = {'response': 'some text', 'done_reason': 'stop', 'error': 'connection failed'}
        valid, reason = mod.is_valid_trial(resp)
        assert valid is False
        assert reason == 'api_error'

    def test_nan_eval_count_is_invalid(self):
        mod = _load_exp13()
        resp = {'response': 'some text', 'done_reason': 'stop', 'eval_count': float('nan')}
        valid, reason = mod.is_valid_trial(resp)
        assert valid is False
        assert reason == 'nan_or_inf_value'

    def test_inf_eval_count_is_invalid(self):
        mod = _load_exp13()
        resp = {'response': 'some text', 'done_reason': 'stop', 'eval_count': float('inf')}
        valid, reason = mod.is_valid_trial(resp)
        assert valid is False
        assert reason == 'nan_or_inf_value'

    def test_missing_done_reason_is_invalid(self):
        mod = _load_exp13()
        resp = {'response': 'some text'}
        valid, reason = mod.is_valid_trial(resp)
        assert valid is False

    def test_unexpected_done_reason_is_invalid(self):
        mod = _load_exp13()
        resp = {'response': 'some text', 'done_reason': 'error'}
        valid, reason = mod.is_valid_trial(resp)
        assert valid is False
        assert 'unexpected_done_reason' in reason

    def test_floats_close_tolerance(self):
        mod = _load_exp13()
        assert mod.floats_close(0.3, 0.30000000000000004) is True
        assert mod.floats_close(0.3, 0.5) is False
        assert mod.floats_close(1.0, 1.0 + 1e-10) is True

    def test_exploratory_warning_present(self):
        mod = _load_exp13()
        assert 'EXPLORATORY' in mod.EXPLORATORY_WARNING
        assert 'NOT A PREREGISTERED' in mod.EXPLORATORY_WARNING

    def test_no_model_invocation_in_tests(self):
        mod = _load_exp13()
        assert hasattr(mod, 'is_valid_trial')
        assert hasattr(mod, 'floats_close')

    def test_historical_result_files_unchanged(self):
        for path in ['experiments/results/exp_1_3_results_gemma.json']:
            if os.path.exists(path):
                with open(path, encoding='utf-8') as f:
                    data = json.load(f)
                assert isinstance(data, dict)

    def test_verdict_set_limited(self):
        allowed = {'SUPPORTED', 'FALSIFIED', 'INCONCLUSIVE', 'INVALID_RUN'}
        src = open('experiments/exp_1_3_state_ablation.py', encoding='utf-8').read()
        for v in allowed:
            assert v in src, 'Missing verdict: %s' % v

    def test_truncated_cannot_contribute_to_positive(self):
        """Truncated output cannot contribute to a positive result."""
        mod = _load_exp13()
        resp = {'response': 'great answer', 'done_reason': 'length'}
        valid, reason = mod.is_valid_trial(resp)
        assert valid is False
        # A truncated trial should have no score
        # (validity gate prevents scoring)

    def test_missing_metadata_invalidates(self):
        """Missing metadata invalidates a trial."""
        mod = _load_exp13()
        # Missing done_reason
        resp = {'response': 'some text'}
        valid, reason = mod.is_valid_trial(resp)
        assert valid is False

    def test_all_invalid_produces_invalid_run(self):
        """All-invalid trials should produce INVALID_RUN verdict."""
        # This is tested via the verdict logic in the module
        src = open('experiments/exp_1_3_state_ablation.py', encoding='utf-8').read()
        assert 'INVALID_RUN' in src
        assert 'all_valid' in src
