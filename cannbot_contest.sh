#!/usr/bin/env bash
# 串行补全 contest/ 缺失的周赛与双周赛题解
# 逻辑：算出本地缺失的场次（周赛编号 >= 300，双周赛编号 < 300）
#       -> 每场 Q1→Q4 逐题检查题解文件是否存在
#       -> 缺失则调用 cannbot 写一道，写完再写下一道（不并发）
set -uo pipefail

WORKDIR="$(cd "$(dirname "$0")" && pwd)"
SKILL="$WORKDIR/contest/SKILL.md"
CONTEST_DIR="$WORKDIR/contest"

cd "$WORKDIR"
echo ">>> 工作目录: $(pwd)"

# ========== 1. 计算待检查的周赛与双周赛场次 ==========
# 规则：下一场即将开赛的场次编号（LeetCode upcomingContests）减一 = 已结束的最新场次
# 范围：从本地该类型最小场次到最新已结束场次（逐题判缺，覆盖部分完成的场次）
# 区分：周赛编号 >= 300（当前 5xx），双周赛编号 < 300（当前 19x）
mapfile -t MISSING_LIST < <(curl -s 'https://leetcode.com/graphql' \
    -H 'Content-Type: application/json' \
    -d '{"query":"query { upcomingContests { titleSlug } }"}' | python3 -c "
import os, re, json, sys

data = json.load(sys.stdin)
upcoming = [c['titleSlug'] for c in data['data']['upcomingContests']]

# 本地已有的场次编号（纯数字目录）
local = [int(d) for d in os.listdir('contest')
         if re.fullmatch(r'\d+', d) and os.path.isdir(os.path.join('contest', d))]

for prefix, kind in (('weekly-contest-', '周赛'), ('biweekly-contest-', '双周赛')):
    slug = next((s for s in upcoming if s.startswith(prefix)), None)
    if slug is None:
        continue
    latest_done = int(slug.rsplit('-', 1)[1]) - 1
    if kind == '周赛':
        pool = [n for n in local if n >= 300]
    else:
        pool = [n for n in local if n < 300]
    start = min(pool, default=latest_done + 1)
    numbers = range(latest_done, start - 1, -1) if kind == '周赛' else range(start, latest_done + 1)
    for n in numbers:
        print(f'{prefix}{n}')
")

if [ "${#MISSING_LIST[@]}" -eq 0 ]; then
    echo ">>> 没有缺失的周赛/双周赛，退出"
    exit 0
fi
echo ">>> 待检查的场次: ${MISSING_LIST[*]}"

# ========== 2. 每场：逐题串行补全 ==========
for slug in "${MISSING_LIST[@]}"; do
    num="${slug##*-}"
    if [[ "$slug" == weekly-* ]]; then
        KIND="周赛"
    else
        KIND="双周赛"
    fi
    echo
    echo "======== 第 $num 场${KIND} ========"

    # 四题题解齐全则整场跳过（避免多余的 API 调用）
    COMPLETE=1
    for q in 1 2 3 4; do
        if ! compgen -G "$CONTEST_DIR/$num/Q${q}.*.md" > /dev/null; then
            COMPLETE=0
            break
        fi
    done
    if [ "$COMPLETE" -eq 1 ]; then
        echo ">>> 第 $num 场${KIND} 四题齐全，跳过"
        continue
    fi

    # 拉取该场 Q1-Q4 题目列表（leetcode.cn GraphQL）
    QUESTIONS_JSON=$(curl -s 'https://leetcode.cn/graphql' \
        -H 'Content-Type: application/json' \
        -d "{\"query\":\"query contestDetail(\$titleSlug:String!){contest(titleSlug:\$titleSlug){questions{questionId title titleSlug}}}\",\"variables\":{\"titleSlug\":\"${slug}\"}")
    echo ">>> 题目列表: $(echo "$QUESTIONS_JSON" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)['data']['contest']
    print(' | '.join(f\"Q{i+1}.{q['title']}\" for i, q in enumerate(d['questions'])))
except Exception:
    print('(获取失败，不影响流程)')
")"

    mkdir -p "$CONTEST_DIR/$num"

    for q in 1 2 3 4; do
        # 已有该题题解则跳过（文件名形如 Q1.<题目名>题解.md）
        if compgen -G "$CONTEST_DIR/$num/Q${q}.*.md" > /dev/null; then
            echo ">>> [第 $num 场${KIND} Q$q] 已存在题解，跳过"
            continue
        fi

        MESSAGE="使用${SKILL}写一下第 ${num} 场${KIND} Q${q} 的题解"
        echo ">>> [第 $num 场${KIND} Q$q] 发送: $MESSAGE"
        if cannbot run "$MESSAGE"; then
            echo ">>> [第 $num 场${KIND} Q$q] 完成"
        else
            echo ">>> [第 $num 场${KIND} Q$q] 警告: cannbot 执行失败，继续下一题" >&2
        fi
    done

    # 每场题解处理完成后单独提交
    COMMIT_MESSAGE="请把第 ${num} 场${KIND}题解产生的所有改动 git 提交"
    echo
    echo "======== 第 $num 场${KIND}提交 ========"
    echo ">>> 发送: $COMMIT_MESSAGE"
    cannbot run "$COMMIT_MESSAGE"
done

# ========== 3. 全部写完后提交并推送 ==========
GIT_MESSAGE="请把本次周赛和双周赛题解产生的所有改动 git 提交并推送到远程仓库"
echo
echo "======== 提交并推送 ========"
echo ">>> 发送: $GIT_MESSAGE"
cannbot run "$GIT_MESSAGE"

echo
echo ">>> 全部缺失周赛/双周赛题解补全完毕"
