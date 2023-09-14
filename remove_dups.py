import os, json, argparse

parser = argparse.ArgumentParser(description='Remove duplicate morphemes from a list of morphemes.')
parser.add_argument('-f', '--file', type=str, help='Path to file containing morphemes.')
args = parser.parse_args()

with open(args.file, 'r', encoding='utf-8') as f:
    morphemes = json.load(f)

morphemes = list(set(morphemes))
morphemes.sort()

with open(args.file, 'w', encoding='utf-8') as f:
    json.dump(morphemes, f, ensure_ascii=False, indent=4)