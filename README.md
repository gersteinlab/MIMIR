# MIMIR - one-click agent fine-tuning
<p align="center">
<img width="500px" alt="Project Baize" src="assets/logo.jpg">
</p>
<p align="center"><a href="https://aclanthology.org/2024.emnlp-demo.49/">[📄 Paper]</a> | <a href="http://54.175.116.207:8501/">[🤗 Demo]</a> | <a href="https://www.youtube.com/watch?v=7fVgv_T_xjc&ab_channel=ChunYuanDeng">[🎬 Video]</a> </p>
<hr>

# What is MIMIR?
*In Norse mythology, Mímisbrunnr, the Well of Wisdom, symbolizes the idea that models can draw knowledge from various domains and generate specialized datas for different fields, much like how Odin gained wisdom from the Well of Mímir.*

**MIMIR is a medical domain multi-turn dialogue data generation tool based on ChatGPT. It supports multi-agent dialogues, allowing users to generate data for instruction tuning using publicly available medical domain datasets. Users can also upload their own knowledge documents to generate dialogue datasets based on those documents. MIMIR supports dialogue verification, where each generated data is double-checked to ensure the accuracy of knowledge. Additionally, it supports fine-tuning, enabling users to deploy the platform on their own machines or utilize our provided fine-tuning scripts for training.**

## Deploy

```bash
1. Download the repo
2. pip install -r requirements.txt
4. cd conf/ && cp config_template.py config.py
5. fill the openai key in the config.py
3. streamlit run MIMIR/app.py
```

## How to generate data?

<p align="center">
  <img src="assets/datadownload.png" width="800"/>
</p>

## How to generate data based on own data file?

<p align="center">
  <img src="assets/agent.png" width="800"/>
</p>

## How to fineturn using our data?

<p align="center">
  <img src="assets/train.png" width="800"/>
</p>

## Citation
If you find MIMIR useful, please cite the following reference:
```
@inproceedings{tang-etal-2024-mimir,
    title = "{MIMIR}: A Customizable Agent Tuning Platform for Enhanced Scientific Applications",
    author = "Tang, Xiangru  and
      Deng, Chunyuan  and
      Wang, Hanmin  and
      Wang, Haoran  and
      Zhao, Yilun  and
      Shi, Wenqi  and
      Fung, Yi  and
      Zhou, Wangchunshu  and
      Cao, Jiannan  and
      Ji, Heng  and
      Cohan, Arman  and
      Gerstein, Mark",
    editor = "Hernandez Farias, Delia Irazu  and
      Hope, Tom  and
      Li, Manling",
    booktitle = "Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing: System Demonstrations",
    month = nov,
    year = "2024",
    address = "Miami, Florida, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.emnlp-demo.49",
    pages = "486--496",
    abstract = "Recently, large language models (LLMs) have evolved into interactive agents, proficient in planning, tool use, and task execution across various tasks. However, without agent-tuning, open-source models like LLaMA2 currently struggle to match the efficiency of larger models such as GPT-4 in scientific applications due to a lack of agent tuning datasets. In response, we introduce MIMIR, a streamlined platform that leverages large LLMs to generate agent-tuning data for fine-tuning smaller, specialized models. By employing a role-playing methodology, MIMIR enables larger models to simulate various roles and create interaction data, which can then be used to fine-tune open-source models like LLaMA2. This approach ensures that even smaller models can effectively serve as agents in scientific tasks. Integrating these features into an end-to-end platform, MIMIR facilitates everything from the uploading of scientific data to one-click agent fine-tuning. MIMIR is publicly released and actively maintained at https://github. com/gersteinlab/MIMIR, along with a demo video for quick-start, calling for broader development.",
}

```
