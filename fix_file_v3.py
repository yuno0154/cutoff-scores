
import re

file_path = r'd:\Antigravity\추정분할점수\나이스 학기말 추정분할점수 산출.html'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

trailing_functions = """
        function refreshViewByRound() {
            const select = document.getElementById('viewRoundSelect');
            if (!select) return;
            project.papers[currentPaperIdx].currentRound = parseInt(select.value);
            // 현재 보이는 뷰가 있으면 갱신
            const vc = document.getElementById('viewContainer');
            if (vc && vc.innerHTML.includes('교사별')) showTeacherView();
            else if (vc && vc.innerHTML.includes('문항 범주')) showCategoryView();
            else if (vc && vc.innerHTML.includes('예상')) showFinalView();
        }

        function getViewRound() {
            const select = document.getElementById('viewRoundSelect');
            return select ? parseInt(select.value) : project.papers[currentPaperIdx].currentRound;
        }

        // === 추정분할점수 산출결과 모달 ===
        function calculateRoundResult(roundIdx) {
            const paper = project.papers[currentPaperIdx];
            const cats = paper.categories;
            const mode = paper.scoreMode || 5;
            const cols = mode === 5 ? 5 : 4;
            const sums = Array(cols).fill(0);
            let cnt = 0;

            project.teachers.forEach(t => {
                const td = paper.teacherData[t];
                if (!td || !td.rounds[roundIdx]) return;

                const isComplete = td.rounds[roundIdx].length >= cats.length && td.rounds[roundIdx].every(row => {
                    if (!row) return false;
                    for (let n = 0; n < cols; n++) {
                        if (row[n] === null || row[n] === undefined || row[n] === '') return false;
                    }
                    return true;
                });
                if (isComplete) {
                    cats.forEach((cat, ci) => {
                        const vals = td.rounds[roundIdx][ci];
                        for (let vi = 0; vi < cols; vi++) {
                            sums[vi] += cat.totalScore * (parseFloat(vals[vi]) / 100);
                        }
                    });
                    cnt++;
                }
            });
            return { avgs: sums.map(s => cnt > 0 ? (s / cnt) : 0), cnt };
        }

        function openResultModal() {
            const paper = project.papers[currentPaperIdx];
            const maxRounds = Math.max(...project.teachers.map(t => paper.teacherData[t]?.rounds?.length || 0));
            
            let html = `<h4>📊 [${paper.name}] 라운드별 산출 결과</h4>`;
            html += '<table><thead><tr><th>라운드</th><th>구분</th><th>A/B</th><th>B/C</th><th>C/D</th><th>D/E</th>' + (paper.scoreMode === 5 ? '<th>E/미도달</th>' : '') + '<th>교사용</th></tr></thead><tbody>';

            for (let r = 0; r < maxRounds; r++) {
                const res = calculateRoundResult(r);
                html += `<tr><td rowspan="2" style="font-weight:bold;background:#f8fafc;">${r + 1}라운드<br><span style="font-size:0.75rem;color:#64748b;">(${res.cnt}명 완료)</span></td>
                        <td style="color:#1e40af;font-weight:bold;background:#f8fafc;">추정분할점수</td>`;
                res.avgs.forEach(v => html += `<td style="color:#1e40af;font-weight:bold;background:#f8fafc;">${v.toFixed(2)}</td>`);
                html += `<td rowspan="2" style="text-align:center;"><button class="btn btn-primary btn-sm" onclick="project.papers[${currentPaperIdx}].selectedResultRound=${r};openApprovalFromResult()">승인요청</button></td></tr>`;
                
                html += `<tr><td style="color:#64748b;font-size:0.85rem;">(참고: 원점수)</td>`;
                res.avgs.forEach(v => html += `<td style="color:#64748b;font-size:0.85rem;">${v.toFixed(1)}</td>`);
                html += '</tr>';
            }
            html += '</tbody></table>';
            html += `<div style="text-align:right;margin-top:15px;"><button class="btn btn-success" onclick="exportRoundResultsToExcel()">📥 결과 엑셀 내보내기</button></div>`;

            document.getElementById('resultModalContent').innerHTML = html;
            document.getElementById('resultModal').style.display = 'flex';
        }
"""

start_marker = "function refreshViewByRound()"
end_marker = "function exportTeacherInputToExcel()"

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if start_marker in line:
        start_idx = i
    if end_marker in line:
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    new_lines = lines[:start_idx] + [trailing_functions] + lines[end_idx:]
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("Restore successful.")
else:
    print(f"Could not find markers: {start_idx}, {end_idx}")
