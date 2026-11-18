"""Opt-in regression for the browser-observed planning horizon/lead-time confusion."""
import argparse
import json
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from service import Service
from chat import ask

parser = argparse.ArgumentParser()
parser.add_argument('--run', action='store_true')
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
if not args.run:
    parser.error('Pass --run for real API usage.')
service = Service()
service.apply(service.preview_delay('CASE-002', 2)['id'])
prompt = 'Explain CASE-002 under the current approved plan. How many shortage days occur, on which date, and why does the order remain 10 units?'
result = ask(service, prompt)
answer = result['answer'].lower()
assert any(t['tool'] == 'inspect_sku' for t in result['trace'])
assert re.search(r'(one|1)[ -](day|stockout|shortage)', answer), answer
assert '2026-11-20' in answer and '10' in answer
assert '7' in answer and '3' in answer, answer
assert not re.search(r'(lead[ -]?time|lead)\s+(of\s+)?10\s+days', answer), answer
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps({'test': '11 planning horizon versus lead time', 'passed': True, 'prompt': prompt, **result}, indent=2, ensure_ascii=False))
print(result['answer'])
print('PASS planning horizon / lead time regression')
