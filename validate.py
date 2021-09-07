from praatio import tgio
import json
from pydub import AudioSegment
import sys

def make_textgrid(filename):
    main_tg = tgio.Textgrid()
    to_transc = []
    seg = AudioSegment.from_wav("audios/"+filename.replace(".json", ".wav"))
    dur = len(seg)/1000
    with open(filename, mode="r", encoding="utf-8") as jfile:
        transc = json.load(jfile)
    for key  in transc.keys():
        if transc[key]["transcription"] != "":
            interval = tgio.Interval(transc[key]["start"], transc[key]["end"], transc[key]["transcription"])
            to_transc.append(interval)
    trans_tier = tgio.IntervalTier("text", to_transc, minT=0, maxT=dur)
    main_tg.addTier(tier=trans_tier)
    main_tg.save("{}.TextGrid".format(filename.replace(".json", "")))

if __name__ == '__main__':
    filename = sys.argv[1]
    make_textgrid(filename)