#!/usr/bin/env python3
"""Analyze a captured ROS 2 node list for the Lab08 training scenarios."""
import argparse, json
from pathlib import Path

REQUIRED = [
    '/controller_manager',
    '/motor_driver',
    '/sensor_node',
    '/state_publisher',
    '/tf_publisher',
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--scenario', choices=['normal','missing_sensor'], required=True)
    ap.add_argument('--json-out', required=True)
    args = ap.parse_args()

    observed = sorted({ln.strip() for ln in Path(args.input).read_text(encoding='utf-8').splitlines() if ln.strip()})
    missing = [n for n in REQUIRED if n not in observed]
    unexpected_missing = list(missing)

    if args.scenario == 'normal':
        ok = not missing
        observed_state = 'NORMAL' if ok else 'ABNORMAL'
        expected_missing = []
    else:
        expected_missing = ['/sensor_node']
        ok = missing == expected_missing
        observed_state = 'ABNORMAL'

    payload = {
        'schema_version': '1.0',
        'scenario': args.scenario,
        'result': 'PASS' if ok else 'FAIL',
        'observed_state': observed_state,
        'required_nodes': REQUIRED,
        'observed_nodes': observed,
        'missing_required_nodes': missing,
        'expected_missing_nodes': expected_missing,
        'operator_decision': (
            '업무 시작 가능' if args.scenario == 'normal' and ok
            else '업무 시작 금지; 상태 기록 후 유지보수 담당자에게 보고'
        ),
    }
    Path(args.json_out).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(0 if ok else 2)

if __name__ == '__main__':
    main()
