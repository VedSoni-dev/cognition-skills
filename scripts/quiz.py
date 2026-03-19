#!/usr/bin/env python3
"""Generate an interactive HTML quiz that opens in the browser.

Usage:
    python quiz.py --questions '[{"q":"What is X?","choices":["A","B","C","D"],"answer":"B","explanation":"Because...","concept":"concept-id"}]' --output /tmp/cognition-quiz.html

The quiz auto-grades, shows explanations, and displays a score summary.
"""

import argparse
import json
import webbrowser
from pathlib import Path


def generate_quiz_html(questions: list[dict], title: str = "Cognition Quiz") -> str:
    questions_json = json.dumps(questions)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f0f23; color: #e0e0e0; min-height: 100vh; display: flex; justify-content: center; padding: 40px 20px; }}
  .container {{ max-width: 640px; width: 100%; }}
  h1 {{ font-size: 24px; margin-bottom: 8px; color: #fff; }}
  .subtitle {{ color: #888; margin-bottom: 32px; font-size: 14px; }}
  .progress {{ background: #1a1a3e; border-radius: 8px; height: 6px; margin-bottom: 32px; overflow: hidden; }}
  .progress-bar {{ height: 100%; background: linear-gradient(90deg, #6366f1, #8b5cf6); transition: width 0.3s ease; }}
  .question-card {{ background: #1a1a3e; border-radius: 12px; padding: 28px; margin-bottom: 16px; border: 1px solid #2d2d5c; }}
  .q-num {{ color: #6366f1; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; }}
  .q-text {{ font-size: 18px; line-height: 1.5; margin-bottom: 20px; color: #fff; }}
  .choices {{ display: flex; flex-direction: column; gap: 10px; }}
  .choice {{ padding: 14px 18px; background: #252552; border: 2px solid #3d3d6c; border-radius: 8px; cursor: pointer; transition: all 0.2s; font-size: 15px; }}
  .choice:hover {{ border-color: #6366f1; background: #2d2d6c; }}
  .choice.selected {{ border-color: #6366f1; background: #2d2d6c; }}
  .choice.correct {{ border-color: #22c55e; background: #0f3d1e; }}
  .choice.incorrect {{ border-color: #ef4444; background: #3d0f0f; }}
  .choice.disabled {{ pointer-events: none; opacity: 0.7; }}
  .choice.disabled.correct {{ opacity: 1; }}
  .explanation {{ margin-top: 16px; padding: 16px; background: #15153a; border-radius: 8px; border-left: 3px solid #6366f1; display: none; font-size: 14px; line-height: 1.6; }}
  .explanation.show {{ display: block; }}
  .result {{ text-align: center; padding: 40px; }}
  .score {{ font-size: 64px; font-weight: 700; background: linear-gradient(135deg, #6366f1, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
  .score-label {{ color: #888; margin-top: 8px; font-size: 18px; }}
  .concept-results {{ margin-top: 24px; text-align: left; }}
  .concept-row {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #2d2d5c; }}
  .concept-name {{ color: #e0e0e0; }}
  .concept-status {{ font-weight: 600; }}
  .concept-status.pass {{ color: #22c55e; }}
  .concept-status.fail {{ color: #ef4444; }}
  .hidden {{ display: none; }}
</style>
</head>
<body>
<div class="container">
  <h1>{title}</h1>
  <div class="subtitle">Answer each question. Results update your Cognition knowledge model.</div>
  <div class="progress"><div class="progress-bar" id="progress" style="width:0%"></div></div>
  <div id="questions"></div>
  <div id="result" class="result hidden"></div>
</div>
<script>
const questions = {questions_json};
let current = 0, correct = 0, answers = [];

function render() {{
  const container = document.getElementById('questions');
  container.innerHTML = '';
  if (current >= questions.length) {{ showResult(); return; }}
  document.getElementById('progress').style.width = ((current / questions.length) * 100) + '%';
  const q = questions[current];
  const card = document.createElement('div');
  card.className = 'question-card';
  card.innerHTML = `
    <div class="q-num">Question ${{current + 1}} of ${{questions.length}}</div>
    <div class="q-text">${{q.q}}</div>
    <div class="choices">${{q.choices.map((c, i) => `<div class="choice" data-idx="${{i}}">${{c}}</div>`).join('')}}</div>
    <div class="explanation" id="explanation">${{q.explanation || ''}}</div>
  `;
  container.appendChild(card);
  card.querySelectorAll('.choice').forEach(el => {{
    el.addEventListener('click', () => handleAnswer(el, q));
  }});
}}

function handleAnswer(el, q) {{
  const chosen = el.textContent;
  const isCorrect = chosen === q.answer;
  if (isCorrect) correct++;
  answers.push({{ concept: q.concept, correct: isCorrect, chosen }});
  el.parentElement.querySelectorAll('.choice').forEach(c => {{
    c.classList.add('disabled');
    if (c.textContent === q.answer) c.classList.add('correct');
    else if (c === el && !isCorrect) c.classList.add('incorrect');
  }});
  document.getElementById('explanation').classList.add('show');
  setTimeout(() => {{ current++; render(); }}, 2000);
}}

function showResult() {{
  document.getElementById('progress').style.width = '100%';
  const pct = Math.round((correct / questions.length) * 100);
  const conceptRows = answers.map(a => `
    <div class="concept-row">
      <span class="concept-name">${{a.concept}}</span>
      <span class="concept-status ${{a.correct ? 'pass' : 'fail'}}">${{a.correct ? 'Correct' : 'Missed'}}</span>
    </div>
  `).join('');
  document.getElementById('result').innerHTML = `
    <div class="score">${{pct}}%</div>
    <div class="score-label">${{correct}} of ${{questions.length}} correct</div>
    <div class="concept-results">${{conceptRows}}</div>
  `;
  document.getElementById('result').classList.remove('hidden');
  document.getElementById('questions').classList.add('hidden');
}}

render();
</script>
</body>
</html>'''


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate interactive HTML quiz')
    parser.add_argument('--questions', required=True, help='JSON array of questions')
    parser.add_argument('--output', default='/tmp/cognition-quiz.html', help='Output HTML file path')
    parser.add_argument('--title', default='Cognition Quiz', help='Quiz title')
    args = parser.parse_args()

    questions = json.loads(args.questions)
    html = generate_quiz_html(questions, args.title)
    out = Path(args.output)
    out.write_text(html, encoding='utf-8')
    print(f'Quiz generated: {out.absolute()}')
    webbrowser.open(f'file://{out.absolute()}')
