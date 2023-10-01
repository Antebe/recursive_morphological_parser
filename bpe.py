from bpemb import BPEmb
bpemb_en = BPEmb(lang="en")

s = bpemb_en.encode("i see a lot of toxicity that i must detoxify", vs = 90)
print(s)
# from wordsegment import load, segment
# load()
# print(segment('itispredefined'))
