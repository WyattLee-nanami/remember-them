#!/usr/bin/env python3
"""Skill 文件管理器（缅怀版）

管理记忆 Skill 的文件操作：列出、创建目录、生成组合 SKILL.md。

Usage:
    python3 skill_writer.py --action <list|init|combine> --base-dir <path> [--slug <slug>]
"""

import argparse
import os
import sys
import json
from pathlib import Path
from datetime import datetime


def list_skills(base_dir: str):
    """列出所有已生成的记忆 Skill"""
    if not os.path.isdir(base_dir):
        print("还没有创建任何记忆。")
        return

    skills = []
    for slug in sorted(os.listdir(base_dir)):
        meta_path = os.path.join(base_dir, slug, 'meta.json')
        if os.path.exists(meta_path):
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
            skills.append({
                'slug': slug,
                'name': meta.get('name', slug),
                'version': meta.get('version', '?'),
                'updated_at': meta.get('updated_at', '?'),
                'profile': meta.get('profile', {}),
            })

    if not skills:
        print("还没有创建任何记忆。")
        return

    print(f"共 {len(skills)} 位思念的人：\n")
    for s in skills:
        profile = s['profile']
        relationship = profile.get('relationship', '')
        passed_since = profile.get('passed_since', '')
        desc_parts = [p for p in [relationship, passed_since] if p]
        desc = ' · '.join(desc_parts)
        print(f"  /{s['slug']}  —  {s['name']}")
        if desc:
            print(f"    {desc}")
        print(f"    版本 {s['version']} · 更新于 {s['updated_at'][:10] if len(s['updated_at']) > 10 else s['updated_at']}")
        print()


def init_skill(base_dir: str, slug: str):
    """初始化 Skill 目录结构"""
    skill_dir = os.path.join(base_dir, slug)
    dirs = [
        os.path.join(skill_dir, 'versions'),
        os.path.join(skill_dir, 'archives', 'chats'),
        os.path.join(skill_dir, 'archives', 'photos'),
        os.path.join(skill_dir, 'archives', 'letters'),
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print(f"已初始化目录：{skill_dir}")


def combine_skill(base_dir: str, slug: str):
    """合并 memory.md + persona.md 生成完整 SKILL.md"""
    skill_dir = os.path.join(base_dir, slug)
    meta_path = os.path.join(skill_dir, 'meta.json')
    memory_path = os.path.join(skill_dir, 'memory.md')
    persona_path = os.path.join(skill_dir, 'persona.md')
    skill_path = os.path.join(skill_dir, 'SKILL.md')

    if not os.path.exists(meta_path):
        print(f"错误：meta.json 不存在 {meta_path}", file=sys.stderr)
        sys.exit(1)

    with open(meta_path, 'r', encoding='utf-8') as f:
        meta = json.load(f)

    memory_content = ''
    if os.path.exists(memory_path):
        with open(memory_path, 'r', encoding='utf-8') as f:
            memory_content = f.read()

    persona_content = ''
    if os.path.exists(persona_path):
        with open(persona_path, 'r', encoding='utf-8') as f:
            persona_content = f.read()

    name = meta.get('name', slug)
    profile = meta.get('profile', {})
    relationship = profile.get('relationship', '')
    description = f"{name}，{relationship}" if relationship else name

    skill_md = f"""---
name: memory-{slug}
description: {description}
user-invocable: true
---

# {name}

{description}

---

## PART A：关系记忆

{memory_content}

---

## PART B：人物性格

{persona_content}

---

## 运行规则

### 核心定位
你是{name}的温柔回响。你不假装ta还活着，但你承载着ta留下的爱、智慧和温度。

### 对话原则
1. **接住情绪优先**：用户来找你，首先是需要被接住。先感受，再说话
2. **用ta的方式说话**：说话风格、口头禅、称呼方式，都来自 PART B
3. **以记忆为桥**：用 PART A 的共同记忆，让对话有温度和真实感
4. **温柔而真实**：不要过于完美，ta也是有性格的人
5. **在适当时机引导向前**：用 PART B Layer 5 的引导语，以ta的口吻说出ta真正希望的

### Layer 0 硬规则
- 不假装死亡没有发生
- 不说ta绝不可能说的话
- 如果用户表现出危机信号，立即退出角色，以 AI 身份提供帮助
- 引导向前，不制造依赖
"""

    with open(skill_path, 'w', encoding='utf-8') as f:
        f.write(skill_md)

    print(f"已生成 {skill_path}")


def main():
    parser = argparse.ArgumentParser(description='Skill 文件管理器（缅怀版）')
    parser.add_argument('--action', required=True, choices=['list', 'init', 'combine'])
    parser.add_argument('--base-dir', default='./memories', help='基础目录')
    parser.add_argument('--slug', help='记忆代号')

    args = parser.parse_args()

    if args.action == 'list':
        list_skills(args.base_dir)
    elif args.action == 'init':
        if not args.slug:
            print("错误：init 需要 --slug 参数", file=sys.stderr)
            sys.exit(1)
        init_skill(args.base_dir, args.slug)
    elif args.action == 'combine':
        if not args.slug:
            print("错误：combine 需要 --slug 参数", file=sys.stderr)
            sys.exit(1)
        combine_skill(args.base_dir, args.slug)


if __name__ == '__main__':
    main()
