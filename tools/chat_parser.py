#!/usr/bin/env python3
"""聊天记录解析器（缅怀版）

支持微信、短信、QQ 等多种格式的聊天记录，
提取说话风格、口头禅、关心方式等用于构建 Persona。

Usage:
    python3 chat_parser.py --file <path> --target "<name>" --output <path> [--format auto]
"""

import argparse
import re
import sys
from pathlib import Path
from collections import Counter


def detect_format(content: str) -> str:
    """自动检测聊天记录格式"""
    if '"msg_type"' in content or '"content"' in content:
        return 'json'
    if '<html' in content.lower() or '<div' in content.lower():
        return 'html'
    # 微信 txt 格式：2023-01-01 12:00:00 名字\n内容
    if re.search(r'\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}', content):
        return 'wechat_txt'
    # 短信格式
    if re.search(r'\d{4}/\d{2}/\d{2}', content):
        return 'sms'
    return 'plain'


def parse_wechat_txt(content: str, target: str) -> list[dict]:
    """解析微信 txt 格式"""
    messages = []
    pattern = r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(.+?)\n(.*?)(?=\d{4}-\d{2}-\d{2}|\Z)'
    for m in re.finditer(pattern, content, re.DOTALL):
        timestamp, sender, text = m.group(1), m.group(2).strip(), m.group(3).strip()
        messages.append({
            'time': timestamp,
            'sender': sender,
            'text': text,
            'is_target': target.lower() in sender.lower()
        })
    return messages


def parse_plain(content: str, target: str) -> list[dict]:
    """解析纯文本粘贴内容"""
    messages = []
    lines = content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 尝试识别发言者
        is_target = target.lower() in line.lower()
        messages.append({
            'time': '',
            'sender': target if is_target else '我',
            'text': line,
            'is_target': is_target
        })
    return messages


def extract_features(messages: list[dict]) -> dict:
    """从消息列表中提取特征"""
    target_messages = [m for m in messages if m['is_target']]

    if not target_messages:
        return {'error': '未找到目标人物的消息'}

    all_text = ' '.join(m['text'] for m in target_messages)

    # 提取口头禅（高频短语）
    words = re.findall(r'[\u4e00-\u9fff]{2,4}|[a-zA-Z]{2,}', all_text)
    word_freq = Counter(words)
    # 过滤常见词
    stopwords = {'一个', '这个', '那个', '什么', '知道', '可以', '没有', '就是', '但是', '因为', '所以'}
    catchphrases = [(w, c) for w, c in word_freq.most_common(30) if w not in stopwords and c >= 2]

    # 提取语气词
    particles = re.findall(r'[哈嗯哦噢哎唉啊呀嘛呢吧啦哟喔]', all_text)
    particle_freq = Counter(particles)

    # 提取标点习惯
    has_period = '。' in all_text
    has_ellipsis = '……' in all_text or '...' in all_text
    has_exclaim = '！' in all_text or '!' in all_text
    has_wave = '～' in all_text or '~' in all_text

    # 消息长度分析
    lengths = [len(m['text']) for m in target_messages]
    avg_length = sum(lengths) / len(lengths) if lengths else 0

    # 提取关心语句（包含特定关键词的消息）
    care_keywords = ['吃了', '睡了', '注意', '小心', '身体', '辛苦', '加油', '没事', '好好', '乖']
    care_messages = [m['text'] for m in target_messages
                     if any(kw in m['text'] for kw in care_keywords)]

    # 提取鼓励语句
    encourage_keywords = ['你能', '你可以', '相信', '没问题', '加油', '好样的', '厉害']
    encourage_messages = [m['text'] for m in target_messages
                          if any(kw in m['text'] for kw in encourage_keywords)]

    return {
        'total_messages': len(target_messages),
        'avg_length': round(avg_length, 1),
        'catchphrases': catchphrases[:10],
        'particle_freq': particle_freq.most_common(5),
        'punctuation': {
            'period': has_period,
            'ellipsis': has_ellipsis,
            'exclaim': has_exclaim,
            'wave': has_wave,
        },
        'care_messages': care_messages[:5],
        'encourage_messages': encourage_messages[:5],
        'sample_messages': [m['text'] for m in target_messages[:10]],
    }


def format_output(features: dict, target: str) -> str:
    """格式化输出结果"""
    if 'error' in features:
        return f"错误：{features['error']}"

    lines = [
        f"# {target} — 聊天记录分析结果",
        f"\n共分析 {features['total_messages']} 条消息，平均长度 {features['avg_length']} 字",
        "\n## 高频词 / 口头禅",
    ]

    for word, count in features['catchphrases']:
        lines.append(f"  - {word}（出现 {count} 次）")

    lines.append("\n## 语气词偏好")
    for particle, count in features['particle_freq']:
        lines.append(f"  - {particle}（{count} 次）")

    p = features['punctuation']
    punct_desc = []
    if p['period']: punct_desc.append("用句号")
    else: punct_desc.append("不用句号")
    if p['ellipsis']: punct_desc.append("用省略号")
    if p['exclaim']: punct_desc.append("用感叹号")
    if p['wave']: punct_desc.append("用波浪号～")
    lines.append(f"\n## 标点习惯\n  {' / '.join(punct_desc)}")

    if features['care_messages']:
        lines.append("\n## 关心方式（原文摘录）")
        for msg in features['care_messages']:
            lines.append(f"  - "{msg[:80]}"")

    if features['encourage_messages']:
        lines.append("\n## 鼓励方式（原文摘录）")
        for msg in features['encourage_messages']:
            lines.append(f"  - "{msg[:80]}"")

    lines.append("\n## 消息样本（前10条）")
    for msg in features['sample_messages']:
        lines.append(f"  - "{msg[:100]}"")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='聊天记录解析器（缅怀版）')
    parser.add_argument('--file', required=True, help='聊天记录文件路径')
    parser.add_argument('--target', required=True, help='目标人物名称')
    parser.add_argument('--output', required=True, help='输出文件路径')
    parser.add_argument('--format', default='auto', choices=['auto', 'wechat_txt', 'plain', 'json'])

    args = parser.parse_args()

    try:
        with open(args.file, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"错误：找不到文件 {args.file}", file=sys.stderr)
        sys.exit(1)

    fmt = args.format if args.format != 'auto' else detect_format(content)

    if fmt == 'wechat_txt':
        messages = parse_wechat_txt(content, args.target)
    else:
        messages = parse_plain(content, args.target)

    features = extract_features(messages)
    output = format_output(features, args.target)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"解析完成，共处理 {len(messages)} 条消息。结果已写入 {args.output}")


if __name__ == '__main__':
    main()
