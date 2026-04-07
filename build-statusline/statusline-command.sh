#!/bin/bash
input=$(cat)
cwd=$(echo "$input" | jq -r '.cwd')
used=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
model_id=$(echo "$input" | jq -r '.model.id // empty')
ctx_used_tokens=$(echo "$input" | jq -r '(.context_window.total_input_tokens // 0) + (.context_window.total_output_tokens // 0)')
ctx_total_tokens=$(echo "$input" | jq -r '.context_window.context_window_size // empty')

# Format a token count compactly: >=1M -> "1.0M", >=1k -> "450k", else raw
format_tokens() {
  local n="$1"
  if [ -z "$n" ] || [ "$n" = "null" ] || [ "$n" = "0" ]; then
    echo ""
    return
  fi
  if [ "$n" -ge 1000000 ] 2>/dev/null; then
    awk -v n="$n" 'BEGIN { printf "%.1fM", n/1000000 }'
  elif [ "$n" -ge 1000 ] 2>/dev/null; then
    awk -v n="$n" 'BEGIN { printf "%dk", int(n/1000) }'
  else
    echo "$n"
  fi
}

# Replace home directory prefix with ~
home_dir="$HOME"
if [ -n "$home_dir" ] && [ "${cwd#"$home_dir"}" != "$cwd" ]; then
  cwd="~${cwd#"$home_dir"}"
fi

# Build git branch + dirty indicator field
raw_cwd=$(echo "$input" | jq -r '.cwd')
git_branch=$(git -C "$raw_cwd" rev-parse --abbrev-ref HEAD 2>/dev/null)
if [ -n "$git_branch" ]; then
  dirty_count=$(git -C "$raw_cwd" status --porcelain 2>/dev/null | wc -l)
  dirty_count=$(echo "$dirty_count" | tr -d ' ')
  unpushed=$(git -C "$raw_cwd" log @{u}..HEAD --oneline 2>/dev/null | wc -l)
  unpushed=$(echo "$unpushed" | tr -d ' ')
  git_str="⎇ ${git_branch}"
  suffix=""
  if [ "$dirty_count" -gt 0 ] 2>/dev/null; then
    suffix="*${dirty_count}"
  fi
  if [ "$unpushed" -gt 0 ] 2>/dev/null; then
    suffix="${suffix} ↑${unpushed}"
  fi
  if [ -n "$suffix" ]; then
    git_str="${git_str}(${suffix})"
  fi
else
  git_str=""
fi

# Build model field
if echo "$model_id" | grep -qi "opus"; then
  model_str="opus"
elif echo "$model_id" | grep -qi "sonnet"; then
  model_str="sonnet"
elif echo "$model_id" | grep -qi "haiku"; then
  model_str="haiku"
elif [ -n "$model_id" ]; then
  model_str="$model_id"
else
  model_str=""
fi

# Build combined context field: "ctx: 9k/1.0M (3%)" or "ctx: --"
tok_used_fmt=$(format_tokens "$ctx_used_tokens")
tok_total_fmt=$(format_tokens "$ctx_total_tokens")
if [ -n "$used" ] && [ -n "$tok_used_fmt" ] && [ -n "$tok_total_fmt" ]; then
  ctx_str="ctx: ${tok_used_fmt}/${tok_total_fmt} ($(printf '%.0f' "$used")%)"
else
  ctx_str="ctx: --"
fi

# Assemble output: path  [git]  [model]  ctx
out="\033[01;34m${cwd}\033[00m"
if [ -n "$git_str" ]; then
  out="${out}  \033[01;35m${git_str}\033[00m"
fi
if [ -n "$model_str" ]; then
  out="${out}  \033[01;36m${model_str}\033[00m"
fi
out="${out}  \033[01;32m${ctx_str}\033[00m"

printf "%b" "$out"
