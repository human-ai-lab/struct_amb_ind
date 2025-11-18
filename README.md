# STRUCT_AMB_IND

This dataset contains **the first Indonesian speech dataset for structurally/ syntactically ambiguous utterances and each of two disambiguation texts + the English translations**

The structurally ambiguous sentences were adapted from Types 4,5,6, and 10 of Types Of Syntactic Ambiguity in English by [[Taha et al., 1983](https://doi.org/10.1515/iral.1983.21.4.251)]. For each chosen type, 100 structurally ambiguous sentences in Indonesian were made by crowdsourcing. Each Indonesian ambiguous sentence has two possible interpretations, resulting in two meaning interpretation text outputs for each ambiguous sentence. Each meaning interpretation text is made up of two sentences. All of the sentences have been checked by linguists.

We also translated the structurally ambiguous transcriptions and the meaning interpretation texts to English by crowdsourcing. 

## Directories and files in this corpus
This corpus contains directories as follows.
1. `ind_speech`  
Contains recording results of syntactically ambiguous sentences in Indonesian based on their interpretations. This recording process involved 22 speakers, 2 of them (F01 and M01) are professional speakers and the rest 20 (F02-F11, M02-M11) are undergraduate students. The recordings are grouped by speaker. In total, there are 4800 .wav files.
    >Format of recording files:
    >```
    >ID_F01_Type04_00011.wav
    >```
    > - ID : Language (Indonesian)
    > - (M/F)XX : Male/ female speaker number XX
    > - TypeYY : Type of structural ambiguity (Type04, Type05, Type06, or Type10)
    > - ZZZZV : Syntactically ambiguous sentence no ZZZZ with interpretation no V. Please refer to our paper below to see what each of the interpretation V stands for.
> Download the audio files here: [link](https://drive.google.com/drive/folders/1Z9Vnyytzd2378As8eL7fLRs7Hajya_8g?usp=sharing)

2. `text`  
This directory contains 2 files:
    - `ID_amb_disam_sent.txt`
    Contains pairs of ambiguous sentences and disambiguation text for each syntactically ambiguous sentences in Indonesian. There are 800 rows (400 syntactically ambiguous sentences, each with 2 interpretations):
        ```
        <AMB_SENT_CODE>|<AMB_TRANSCRIPT>|<DISAM_TEXT>
        ID_Type06_00011|saya melihat seseorang di gunung|saya melihat seseorang. saya melihat di gunung
        ```
        - \<AMB_SENT_CODE>: Id for structurally ambiguous sentence and one of its interpretations. Same format with .WAV file, but no speaker ID
        - \<AMB_TRANSCRIPT>: structurally ambiguous sentence
        - \<DISAM_TEXT>: one of <AMB_TRANSCRIPT> interpretation 

    - `EN_amb_disam_sent.txt`
    Contains the translation of `ID_amb_disam_sent.txt` (in other word, contains pairs of ambiguous translation and disambiguation translation for each syntactically ambiguous sentences in English.):
        ```
        <AMB_SENT_CODE>|<AMB_TRANSCRIPT>|<DISAM_TEXT>
        EN_Type06_00011|saya melihat seseorang di gunung|saya melihat seseorang. saya melihat di gunung
        ```
        - \<AMB_SENT_CODE>: Id for structurally ambiguous translation and one of its unambiguous translation. Each row with Id `EN_TypeYY_ZZZZV` is a translation of row with Id `ID_TypeYY_ZZZZV` in `ID_amb_disam_sent.txt`.
        - \<AMB_TRANSLATION>: structurally ambiguous translation (translation as is)
        - \<DISAM_TRANSLATION>: one of <AMB_TRANSCLATION> interpretation 
    
3. `keys`
This directory contains 2 directories:
    -  `spk_to_sent_keys`: contains list of <AMB_SENT_CODE> keys for each speaker
    -  `split_to_spk_keys`: contains list of speakers for each split (train/valid/test)

4. `lvcsr`  
Our study in the paper also used additional training data for ASR and SD: a subset of `Indonesian LVCSR news corpus` (https://github.com/s-sakti/data_indsp_news_lvcsr). Therefore, here we also include the corpus's keys we used as train, dev, and test as well as their translations. If you also use the `Indonesian LVCSR news corpus`, don't forget to also cite the papers mentioned on its github!

4. `src`
Contains simple code to generate data for each task ASR / ASR with additional meaning tag / Text Disambiguation (TD) / Speech Disambiguation (SD) / MT / Disambiguation MT (DMT) / Disambiguation Speech-to-text Translation (DST) (from the structural ambiguity corpus only / the Indonesian LVCSR is not included). To generate the corpus, run:
```
bash src/prepare_data.sh
```

## Citation
This corpus is part of our studies regarding the disambiguation of structurally ambiguous utterances in Indonesian and structural ambiguity-free speech translation for Indonesian→English. 

1. If you are not using the translation, please cite the following paper:
```
@inproceedings{widiaputri-etal-2023-speech,
    title = "Speech Recognition and Meaning Interpretation: Towards Disambiguation of Structurally Ambiguous Spoken Utterances in {I}ndonesian",
    author = "Widiaputri, Ruhiyah  and
      Purwarianti, Ayu  and
      Lestari, Dessi  and
      Azizah, Kurniawati  and
      Tanaya, Dipta  and
      Sakti, Sakriani",
    booktitle = "Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing",
    month = dec,
    year = "2023",
    address = "Singapore",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.emnlp-main.1045",
    doi = "10.18653/v1/2023.emnlp-main.1045",
}
```

2. If you are using the translation as well, please cite the following paper:
```
coming soon!
```
