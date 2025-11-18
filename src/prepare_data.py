import argparse
import pandas as pd
import os

def parse():
    parser = argparse.ArgumentParser(description="Script to prepare ASR/TD/SD/DMT/DST data")
    parser.add_argument('--task', nargs='+', type=str, choices=['asr', 'asr_tag', 'td', 'sd', 'dmt', 'dst', 'mt'], default=['dst'], help='What tasks are the prepared data for?')
    parser.add_argument('--audio-dir', type=str, default='ind_speech', help='Directory for the downloaded audio data (both for LVCSR and struct_amb)')
    parser.add_argument('--out-dir', type=str, default='struct_amb_data', help='Directory for the downloaded audio data (both for LVCSR and struct_amb)')
    args = parser.parse_args()
    return args

def read_text_file(text_file_path):
    with open(text_file_path, "r") as fh:
        data = [x.strip() for x in fh.readlines()]

    return { 
            parts[0]: {"ambiguous": parts[1].strip(), "not_ambiguous": parts[2].strip()} 
            for x in data 
            for parts in [x.split("|")]
        }

def get_split_uttr_sent_ids(split):
    # get list of speakers for this split
    with open(f"keys/split_to_spk_keys/{split}_spk", "r") as fh:
        speakers = [x.strip() for x in fh.readlines()]

    # get sent and uttr ids for each speakers
    split_uttr_ids = []
    split_sent_ids = []

    for spk in speakers:
        with open(f"keys/spk_to_sent_keys/{spk}", "r") as fh:
            spk_to_sent_keys = [x.strip() for x in fh.readlines()]
            split_sent_ids.extend(spk_to_sent_keys)
            spk_uttr_ids = [f"ID_{spk}_{"_".join(x.strip().split("_")[1:])}" for x in spk_to_sent_keys]
            split_uttr_ids.extend(spk_uttr_ids)

    return sorted(split_uttr_ids), sorted(set(split_sent_ids))

def save_to_tsv(data, task, split, out_dir):
    df = pd.DataFrame(data)
    dir_path = os.path.join(out_dir, task)
    os.makedirs(dir_path, exist_ok=True)
    df.to_csv(os.path.join(dir_path, f"{split}_struct_amb.tsv"), sep="\t")

def prepare_data_for_asr(args, id_amb_disam_sent, split_uttr_ids, split, **kwargs):
    data = []
    for id in split_uttr_ids:
        parts = id.split("_")
        nospk_id = "_".join([parts[0], parts[2], parts[3]])
        audio = os.path.join(os.path.abspath(args.audio_dir), f"{id}.wav")
        transcript = id_amb_disam_sent[nospk_id]["ambiguous"]
        data.append({
            "id": id,
            "audio": audio,
            "transcript": transcript
        })
    save_to_tsv(data, "asr", split, args.out_dir)
    return data

def prepare_data_for_asr_tag(args, id_amb_disam_sent, split_uttr_ids, split, **kwargs):
    data = []
    for id in split_uttr_ids:
        parts = id.split("_")
        nospk_id = "_".join([parts[0], parts[2], parts[3]])
        audio = os.path.join(os.path.abspath(args.audio_dir), f"{id}.wav")
        transcript = id_amb_disam_sent[nospk_id]["ambiguous"]
        meaning_tag = f"<{id[-1]}>"
        data.append({
            "id": id,
            "audio": audio,
            "transcript_with_meaning_tag": meaning_tag + " " + transcript
        })
    save_to_tsv(data, "asr_tag", split, args.out_dir)
    return data

def prepare_data_for_sd(args, id_amb_disam_sent, split_uttr_ids, split, **kwargs):
    data = []
    for id in split_uttr_ids:
        parts = id.split("_")
        nospk_id = "_".join([parts[0], parts[2], parts[3]])
        audio = os.path.join(os.path.abspath(args.audio_dir), f"{id}.wav")
        meaning_interpretation = id_amb_disam_sent[nospk_id]["not_ambiguous"]
        data.append({
            "id": id,
            "audio": audio,
            "meaning_interpretation": meaning_interpretation
        })
    save_to_tsv(data, "sd", split, args.out_dir)
    return data

def prepare_data_for_dst(args, en_amb_disam_sent, split_uttr_ids, split, **kwargs):
    data = []
    for id in split_uttr_ids:
        parts = id.split("_")
        nospk_id = "_".join(["EN", parts[2], parts[3]])
        audio = os.path.join(os.path.abspath(args.audio_dir), f"{id}.wav")
        meaning_interpretation = en_amb_disam_sent[nospk_id]["not_ambiguous"]
        data.append({
            "id": id,
            "audio": audio,
            "unambiguous_translation": meaning_interpretation
        })
    save_to_tsv(data, "dst", split, args.out_dir)
    return data

def prepare_data_for_td(args, id_amb_disam_sent, split_sent_ids, split, **kwargs):
    data = []
    for id in split_sent_ids:
        meaning_tag = f"<{id[-1]}>"
        data.append({
            "id": id,
            "src_text": meaning_tag + " " + id_amb_disam_sent[id]["ambiguous"],
            "meaning_interpretation": id_amb_disam_sent[id]["not_ambiguous"]
        })
    save_to_tsv(data, "td", split, args.out_dir)
    return data

def prepare_data_for_dmt(args, id_amb_disam_sent, en_amb_disam_sent, split_sent_ids, split, **kwargs):
    data = []
    for id in split_sent_ids:
        meaning_tag = f"<{id[-1]}>"
        data.append({
            "id": id,
            "src_text": meaning_tag + " " + id_amb_disam_sent[id]["ambiguous"],
            "meaning_interpretation": en_amb_disam_sent[id.replace("ID","EN")]["not_ambiguous"]
        })
    save_to_tsv(data, "dmt", split, args.out_dir)
    return data

def prepare_data_for_mt(args, id_amb_disam_sent, en_amb_disam_sent, split_sent_ids, split, **kwargs):
    data = []
    for id in split_sent_ids:
        meaning_tag = f"<{id[-1]}>"
        data.append({
            "id": id,
            "src_text": id_amb_disam_sent[id]["not_ambiguous"],
            "tgt_text": en_amb_disam_sent[id.replace("ID","EN")]["not_ambiguous"]
        })
    save_to_tsv(data, "mt", split, args.out_dir)
    return data

prepare_data_for = {
    "asr": prepare_data_for_asr,
    "asr_tag": prepare_data_for_asr_tag,
    "sd": prepare_data_for_sd,
    "dst": prepare_data_for_dst,
    "td": prepare_data_for_td,
    "dmt": prepare_data_for_dmt,
    "mt": prepare_data_for_mt,
}

if __name__=="__main__":
    args = parse()

    # read text files
    id_amb_disam_sent = read_text_file("text/ID_amb_disam_sent.txt")
    en_amb_disam_sent = read_text_file("text/EN_amb_disam_sent.txt")

    # prepare data for each task
    for split in ["train", "valid", "test"]:
        split_uttr_ids, split_sent_ids = get_split_uttr_sent_ids(split)

        for task in args.task:
            data = prepare_data_for[task](
                args, 
                id_amb_disam_sent=id_amb_disam_sent, 
                en_amb_disam_sent=en_amb_disam_sent,
                split_uttr_ids=split_uttr_ids,
                split_sent_ids=split_sent_ids,
                split=split
            )
            print(f"SPLIT: {split.upper()} | TASK: {task.upper()} | Number of data: {len(data)}")
