from  allosaurus.app import read_recognizer
import sys
import os, re
import _pickle as pickle
import json
from pydub import AudioSegment
from auditok import split, AudioRegion
import scipy.io.wavfile as wav
import Levenshtein

letters = re.compile(r"(rdd|rl|nj|ng|rr|dj|y|rd|rn|kk|k|h|l|m|b|d|n|w|r|a|e|i|o|u)")
def get_syll(insent):
    letters = re.compile(r"(rdd|rl|nj|ng|rr|dj|y|rd|rn|kk|k|h|l|m|b|d|n|w|r|a|e|i|o|u)")
    voy = ["a", "e", "i", "o", "u"]
    sylls = []
    sent = re.findall(letters, insent)
    syll=""
    isvoy = False
    out = []
    for i, char in enumerate(sent):
        if char not in voy and syll=="":
            syll=char
            out.append(char)
        elif syll!="" and i==len(sent)-1:

            sylls.append(syll+char)
            syll=char
        elif char in voy:
            syll = syll+char
            out.append(char)
        elif char not in voy and syll!="" and i==len(sent)-1:
            syll=syll+char
            out.append(char)
        elif char not in voy and syll !="" and sent[i+1] not in voy:
            syll = syll+char
            out.append(char)
        elif char not in voy and syll!="" and sent[i+1] in voy:


            sylls.append(syll)

            syll=char
            
            
        else:
            print(char)
            print(sent)
            exit()
    out_str = ""

    return(sylls)


def main(wav_fn):
    with open("sylls.json", mode="r", encoding="utf-8") as jfile:
        json_sylls = set(json.load(jfile))
    # lex = MyTrie()
    pairs = {"k": "kk", "kk": "k", "d": "rd", "rd": "d", "n" : "rn", "rn" : "n", "l" : "rr", "rr" : "l"}
    p2g = {"a" : "a", "b" : "b" ,"d" : "d", "ɛ" : "e", "ʔ": "h","v" : "v", "i" :"i", "ɑ" : "a" ,"ʃ" : "ch", " " : " ","h" : "h", "j": "y","o":"o", "f": "f", "k": "k", " " : " "
    ,"l":"l", "m": "m", "n":"n", "ɟ" : "dj", "ɔ" : "o", "s" : "s", "ɹ": "r","ɻ" : "r", "æ":"e", "ŋ": "ng", "ʈ" : "rd","ɖ" : "rd", "ɳ" : "rn", "ɭ" : "rl","r": "rr", "ɲ": "nj", "u": "u", "w":"w", "\n": "", 
    "p": "p", "t":"d", "$" : "tch"} 
    name = os.path.basename(wav_fn)
    name = name.replace(".wav", "")
    region = split(wav_fn)
    full = AudioSegment.from_wav(wav_fn)
    cpt=0
    out_dic = {}
    if not os.path.isdir("splits"):
        os.mkdir("splits")
    for r, reg in enumerate(region):
        print(reg.meta.start, reg.meta.end)
        sub = full[reg.meta.start*1000:reg.meta.end*1000]
        out_name = name+"_"+str(cpt)+".wav"
        sub.export("splits/"+out_name, format="wav")

        model = read_recognizer("big_kun")
        output = model.recognize("splits/"+out_name)
        print(output)

        graphs = "".join(p2g[x] for x in output).replace(" ", "")
        print(graphs)
        segs = set(get_syll(graphs))
        final = []
        for s in segs:
            if s in json_sylls:
                final.append(s)
                let = re.findall(letters, s)

                closest = [(x, Levenshtein.ratio(s,x))for x in json_sylls]
                closest = sorted(closest, key= lambda x : x[1], reverse=True)
                if len(segs)<=4:
                    final.append(closest[1][0])

            else:
                closest = [(x, Levenshtein.ratio(s,x))for x in json_sylls]
                closest = sorted(closest, key= lambda x : x[1], reverse=True)

                final.append(closest[0][0])
        if len(final)>2:
            out_dic[out_name] = {"syllables" : final, 
            "start" : reg.meta.start, "end" : reg.meta.end, "transcription" : ""}
            cpt+=1


    with open(os.path.basename(wav_fn).replace(".wav", "")+".json", mode="w", encoding="utf_8") as jfile:
        json.dump(out_dic, jfile)

if __name__ == '__main__':
    wav_fn = sys.argv[1]
    main(wav_fn)