#!/usr/bin/env python3
"""
澳门癌症数据下载脚本
从澳门政府数据开放平台下载癌症相关数据集
"""

import requests
import os
import json
from pathlib import Path

# 创建数据目录
DATA_DIR = Path("macau_cancer_data")
DATA_DIR.mkdir(exist_ok=True)

# 18个癌症数据集的信息
DATASETS = [
    {
        "name": "十大死亡癌症個案",
        "id": "420d8915-1599-4fee-9cba-50df76c482ee",
        "filename": "topTenDeathCancerCases.xlsx",
        "description": "疾病預防控制範疇十大死亡癌症個案"
    },
    {
        "name": "十大癌症新增個案",
        "id": "3be8ebf8-4a12-4acf-b5bc-2877bd7d68ca",
        "filename": "topTenNewCancerCases.xlsx",
        "description": "疾病預防控制範疇十大癌症新增個案"
    },
    {
        "name": "按歲組劃分的2020年主要新增癌症個案",
        "id": "edde9246-5ac7-449b-9f71-ab39b49ec4c3",
        "filename": "cancerCasesByAgeGroup2020.xlsx",
        "description": "疾病預防控制範疇按歲組劃分的二ｏ二ｏ年主要新增癌症個案"
    },
    {
        "name": "癌症登記年報新個案數",
        "id": "26a9e6d1-309b-43cc-8e5e-1ebe01999e1e",
        "filename": "cancerRegistryNewCases.xlsx",
        "description": "澳門癌症登記年報癌症新個案數"
    },
    {
        "name": "癌症登記年報死亡個案數",
        "id": "fb690057-3e6d-4b3d-b8e4-3add6de0c60a",
        "filename": "cancerRegistryDeathCases.xlsx",
        "description": "澳門癌症登記年報癌症死亡個案數"
    },
    {
        "name": "癌症登記年報發生率",
        "id": "6d0e91a7-5478-4b96-924c-c66de1895225",
        "filename": "cancerRegistryIncidenceRate.xlsx",
        "description": "澳門癌症登記年報每十萬人口之癌症發生率"
    },
    {
        "name": "女性癌症新個案數",
        "id": "9d745557-d9e1-4e4f-9c19-422d72cd7091",
        "filename": "femaleCancerNewCases.xlsx",
        "description": "澳門癌症登記年報的女性癌症新個案數"
    },
    {
        "name": "女性癌症死亡率",
        "id": "4d781976-f108-453d-8634-2190ff8ce514",
        "filename": "femaleCancerMortalityRate.xlsx",
        "description": "澳門癌症登記年報每十萬女性之癌症死亡率"
    },
    {
        "name": "男性癌症新個案數",
        "id": "a7525a1a-46ce-4c64-ad8b-2aea86179a6f",
        "filename": "maleCancerNewCases.xlsx",
        "description": "澳門癌症登記年報男性癌症新個案數"
    },
    {
        "name": "癌症死亡率",
        "id": "f7f6b2ab-09cb-4370-9071-dcb62518d8a7",
        "filename": "cancerMortalityRate.xlsx",
        "description": "澳門癌症登記年報每十萬人口之癌症死亡率"
    }
]

def download_dataset(dataset_info):
    """下载单个数据集"""
    dataset_id = dataset_info["id"]
    filename = dataset_info["filename"]
    name = dataset_info["name"]
    
    # API下载URL（需要获取token，这里使用通用格式）
    # 注意：实际token需要从网页获取，这里提供基础URL
    base_url = f"https://api.data.gov.mo/document/download/{dataset_id}"
    
    # 方法1：尝试通过API下载（需要token）
    # 方法2：直接访问详情页获取下载链接
    
    detail_url = f"https://data.gov.mo/Detail?id={dataset_id}"
    
    print(f"\n正在下载: {name}")
    print(f"详情页: {detail_url}")
    print(f"目标文件: {filename}")
    
    # 由于需要token，建议手动下载或使用浏览器自动化
    # 这里提供下载说明
    filepath = DATA_DIR / filename
    
    return {
        "name": name,
        "detail_url": detail_url,
        "filename": filename,
        "filepath": str(filepath),
        "status": "需要手动下载或使用浏览器自动化"
    }

def create_download_guide():
    """创建下载指南"""
    guide = {
        "title": "澳门癌症数据下载指南",
        "source": "澳门特别行政区政府数据开放平台",
        "url": "https://data.gov.mo/Datasets",
        "datasets": []
    }
    
    for dataset in DATASETS:
        info = download_dataset(dataset)
        guide["datasets"].append({
            "name": info["name"],
            "description": dataset["description"],
            "detail_url": info["detail_url"],
            "filename": info["filename"],
            "download_method": "访问详情页，点击下载按钮"
        })
    
    # 保存指南
    guide_path = DATA_DIR / "download_guide.json"
    with open(guide_path, "w", encoding="utf-8") as f:
        json.dump(guide, f, ensure_ascii=False, indent=2)
    
    # 创建Markdown格式的指南
    md_guide = "# 澳门癌症数据下载指南\n\n"
    md_guide += "数据来源: [澳门特别行政区政府数据开放平台](https://data.gov.mo/Datasets)\n\n"
    md_guide += "## 数据集列表\n\n"
    
    for i, dataset in enumerate(DATASETS, 1):
        md_guide += f"### {i}. {dataset['name']}\n\n"
        md_guide += f"- **描述**: {dataset['description']}\n"
        md_guide += f"- **详情页**: [点击访问](https://data.gov.mo/Detail?id={dataset['id']})\n"
        md_guide += f"- **文件名**: {dataset['filename']}\n\n"
    
    md_guide += "## 下载方法\n\n"
    md_guide += "1. 访问每个数据集的详情页\n"
    md_guide += "2. 在\"檔案下載\"部分点击下载按钮\n"
    md_guide += "3. 或使用浏览器自动化工具（如Selenium）批量下载\n\n"
    md_guide += "## 数据用途\n\n"
    md_guide += "这些数据将用于论文中的以下分析：\n\n"
    md_guide += "1. **本地化适配性验证**: 计算研究覆盖的5大癌种与澳门高发癌种的重合率\n"
    md_guide += "2. **年龄分布匹配**: 验证研究样本年龄分布与澳门癌症患者年龄分布的匹配度\n"
    md_guide += "3. **性别特异性适配**: 分析AI系统对不同性别高发癌种的响应适配度\n"
    md_guide += "4. **风险预警模块**: 基于澳门癌症登记数据生成个性化风险提示\n\n"
    
    md_path = DATA_DIR / "download_guide.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_guide)
    
    print(f"\n下载指南已创建:")
    print(f"  - JSON格式: {guide_path}")
    print(f"  - Markdown格式: {md_path}")
    
    return md_path

if __name__ == "__main__":
    print("=" * 60)
    print("澳门癌症数据下载脚本")
    print("=" * 60)
    
    # 创建下载指南
    guide_path = create_download_guide()
    
    print("\n" + "=" * 60)
    print("说明:")
    print("由于数据平台需要token认证，建议使用以下方法:")
    print("1. 手动访问每个数据集详情页下载")
    print("2. 使用浏览器自动化工具（Selenium/Playwright）")
    print("3. 查看生成的下载指南获取所有链接")
    print("=" * 60)
    print(f"\n下载指南已保存至: {guide_path}")

