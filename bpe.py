from bpemb import BPEmb
bpemb_en = BPEmb(lang="uk")

s = bpemb_en.encode("недооцінюванонавчальний")
print(s)
# from wordsegment import load, segment
# load()
# print(segment('itispredefined'))
