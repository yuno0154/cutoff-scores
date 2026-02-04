
import re

file_path = r'd:\Antigravity\추정분할점수\나이스 학기말 추정분할점수 산출.html'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_category_view = """
        function showCategoryView() {
            const paper = project.papers[currentPaperIdx];
            const cats = paper.categories;
            const viewRound = document.getElementById('viewRoundSelect')?.value ?? paper.currentRound;
            const roundIdx = parseInt(viewRound);
            const mode = paper.scoreMode || 5;
            const levels = mode === 5 ? ['A', 'B', 'C', 'D', 'E'] : ['A', 'B', 'C', 'D'];

            let html = `<h4>📊 문항 범주별 상세 통계 (${roundIdx + 1}라운드)</h4>`;
            html += '<div style="overflow-x:auto;"><table><thead><tr><th rowspan="2">문항유형</th><th rowspan="2">난이도</th>';
            levels.forEach(lv => {
                html += `<th colspan="4" style="text-align:center;background:#e0f2fe;">${lv}</th>`;
            });
            html += '</tr><tr>';
            levels.forEach(() => {
                html += '<th>평균</th><th>표준편차</th><th>최솟값</th><th>최댓값</th>';
            });
            html += '</tr></thead><tbody>';

            cats.forEach((cat, ci) => {
                const levelData = levels.map(() => []);
                project.teachers.forEach(t => {
                    const td = paper.teacherData[t];
                    if (!td || !td.rounds[roundIdx] || !td.rounds[roundIdx][ci]) return;
                    const vals = td.rounds[roundIdx][ci];
                    for (let c = 0; c < levels.length; c++) {
                        if (vals[c] !== null && vals[c] !== undefined && vals[c] !== '') {
                            levelData[c].push(parseFloat(vals[c]));
                        }
                    }
                });

                html += `<tr><td>${cat.type}</td><td>${cat.difficulty}</td>`;
                levelData.forEach(arr => {
                    if (arr.length === 0) {
                        html += '<td>-</td><td>-</td><td>-</td><td>-</td>';
                    } else {
                        const avg = arr.reduce((a, b) => a + b, 0) / arr.length;
                        const std = Math.sqrt(arr.reduce((a, b) => a + (b - avg) ** 2, 0) / arr.length);
                        const min = Math.min(...arr);
                        const max = Math.max(...arr);
                        html += `<td>${avg.toFixed(2)}</td><td>${std.toFixed(2)}</td><td>${min.toFixed(0)}</td><td>${max.toFixed(0)}</td>`;
                    }
                });
                html += '</tr>';
            });
            html += '</tbody></table></div>';
            document.getElementById('viewContainer').innerHTML = html;
        }

        function showFinalView() {
            const paper = project.papers[currentPaperIdx];
            const cats = paper.categories;
            const viewRound = document.getElementById('viewRoundSelect')?.value ?? paper.currentRound;
            const roundIdx = parseInt(viewRound);
            const mode = paper.scoreMode || 5;
            const headers = mode === 5 ? ['A/B', 'B/C', 'C/D', 'D/E', 'E/미도달'] : ['A/B', 'B/C', 'C/D', 'D/E'];

            const teacherScores = headers.map(() => []);
            project.teachers.forEach(t => {
                const td = paper.teacherData[t];
                if (!td || !td.rounds[roundIdx]) return;
                
                const isComplete = td.rounds[roundIdx].length >= cats.length && td.rounds[roundIdx].every(row => {
                    if (!row) return false;
                    for (let n = 0; n < headers.length; n++) {
                        if (row[n] === null || row[n] === undefined || row[n] === '') return false;
                    }
                    return true;
                });
                
                if (!isComplete) return;

                const scores = headers.map(() => 0);
                cats.forEach((cat, ci) => {
                    const vals = td.rounds[roundIdx][ci];
                    for (let vi = 0; vi < headers.length; vi++) {
                        scores[vi] += cat.totalScore * (parseFloat(vals[vi]) / 100);
                    }
                });
                scores.forEach((s, i) => teacherScores[i].push(s));
            });

            let html = `<h4>🏆 최종 예상 추정분할점수 (${roundIdx + 1}라운드)</h4>`;
            html += '<table><thead><tr><th>구분</th>';
            headers.forEach(h => html += `<th>${h}</th>`);
            html += '</tr></thead><tbody>';

            // 평균
            html += '<tr><td style="font-weight:bold;">평균</td>';
            teacherScores.forEach(arr => {
                const avg = arr.length > 0 ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
                html += `<td style="font-weight:bold;color:#1e40af;">${avg.toFixed(2)}</td>`;
            });
            html += '</tr>';

            // 표준편차
            html += '<tr><td style="font-weight:bold;">표준편차</td>';
            teacherScores.forEach(arr => {
                if (arr.length === 0) { html += '<td>-</td>'; return; }
                const avg = arr.reduce((a, b) => a + b, 0) / arr.length;
                const std = Math.sqrt(arr.reduce((a, b) => a + (b - avg) ** 2, 0) / arr.length);
                html += `<td>${std.toFixed(2)}</td>`;
            });
            html += '</tr>';

            // 최솟값
            html += '<tr><td style="font-weight:bold;">최솟값</td>';
            teacherScores.forEach(arr => {
                html += `<td>${arr.length > 0 ? Math.min(...arr).toFixed(2) : '-'}</td>`;
            });
            html += '</tr>';

            // 최댓값
            html += '<tr><td style="font-weight:bold;">최댓값</td>';
            teacherScores.forEach(arr => {
                html += `<td>${arr.length > 0 ? Math.max(...arr).toFixed(2) : '-'}</td>`;
            });
            html += '</tr>';

            html += '</tbody></table>';
            document.getElementById('viewContainer').innerHTML = html;
        }

        function renderViewRoundSelect() {
            const select = document.getElementById('viewRoundSelect');
            if (!select) return;
            const paper = project.papers[currentPaperIdx];
            let opts = '';
            const maxRounds = Math.max(...project.teachers.map(t => paper.teacherData[t]?.rounds?.length || 0));
            for (let r = 0; r < maxRounds; r++) {
                opts += `<option value="${r}" ${r === paper.currentRound ? 'selected' : ''}>${r + 1}라운드</option>`;
            }
            select.innerHTML = opts || '<option value="0">1라운드</option>';
        }
"""

start_marker = "function showCategoryView()"
end_marker = "function refreshViewByRound()"

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if start_marker in line:
        start_idx = i
    if end_marker in line:
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    new_lines = lines[:start_idx] + [new_category_view] + lines[end_idx:]
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("Restore successful.")
else:
    print(f"Could not find markers: {start_idx}, {end_idx}")
