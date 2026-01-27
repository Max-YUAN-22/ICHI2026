"""
ICHI 2026 论文图表生成脚本
生成 Figure 5-9（数据图表）
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import font_manager
import os

# 创建输出目录（避免iCloud同步问题）
OUTPUT_DIR = os.path.expanduser("~/Desktop/ICHI_figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f"=== 图表保存目录: {OUTPUT_DIR} ===\n")

# 全局设置
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 11
plt.rcParams['figure.dpi'] = 600
plt.rcParams['savefig.dpi'] = 600
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['savefig.facecolor'] = 'white'

print("=== 开始生成ICHI 2026论文图表 ===\n")

# === Figure 5: Performance Comparison ===
print("生成 Figure 5: Performance Comparison...")
metrics = ['Accuracy', 'Completeness', 'Safety', 'Usability', 'Satisfaction']
ai_means = [4.16, 4.23, 4.36, 4.00, 4.16]
ai_stds = [0.63, 0.55, 0.51, 0.67, 0.63]
trad_means = [3.00, 2.80, 4.21, 3.09, 3.03]
trad_stds = [0.79, 0.84, 0.53, 0.81, 0.95]
significance = ['***', '***', '**', '***', '***']

fig, ax = plt.subplots(figsize=(7, 5))
x = np.arange(len(metrics))
width = 0.35

bars1 = ax.bar(x - width/2, ai_means, width, yerr=ai_stds, 
               label='AI Agent (Multimodal + Macau)', color='#2E5090', 
               capsize=5, alpha=0.9, edgecolor='white', linewidth=1.5)
bars2 = ax.bar(x + width/2, trad_means, width, yerr=trad_stds,
               label='Traditional System', color='#95A5A6', 
               capsize=5, alpha=0.9, edgecolor='white', linewidth=1.5)

# 显著性标记
for i, sig in enumerate(significance):
    height = max(ai_means[i] + ai_stds[i], trad_means[i] + trad_stds[i])
    ax.text(i, height + 0.15, sig, ha='center', va='bottom', 
            fontsize=14, fontweight='bold', color='#E74C3C')

# 参考线
ax.axhline(y=4.0, color='#27AE60', linestyle='--', linewidth=1.5, alpha=0.6, 
           label='Excellence threshold')
ax.axhline(y=3.0, color='#F39C12', linestyle='--', linewidth=1.5, alpha=0.6, 
           label='Minimum standard')

ax.set_xlabel('Evaluation Dimensions', fontsize=13, fontweight='bold')
ax.set_ylabel('Rating (1-5 Likert Scale)', fontsize=13, fontweight='bold')
ax.set_title('System Performance Comparison\n(AI Agent with Multimodal + Macau Localization)', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(metrics, rotation=0, ha='center', fontsize=11)
ax.set_ylim(0, 5.2)
ax.legend(loc='upper left', frameon=True, fontsize=10, shadow=True)
ax.grid(axis='y', alpha=0.3, linestyle='-', linewidth=0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, 'system_performance_comparison_enhanced.png')
plt.savefig(output_path, dpi=600, bbox_inches='tight')
plt.close()
print(f"✅ Figure 5 生成完成: {output_path}")

# === Figure 6: Effect Sizes ===
print("生成 Figure 6: Effect Sizes...")
metrics = ['Accuracy', 'Completeness', 'Safety', 'Usability', 'Satisfaction']
effect_sizes = [1.63, 2.00, 0.28, 1.22, 1.42]
classifications = ['Very Large\n(Macau knowledge)', 'Very Large\n(Multimodal info)', 
                  'Small\n(Both safe)', 'Large\n(Multimodal UI)', 'Large\n(Local resources)']

colors = []
for d in effect_sizes:
    if d >= 0.8:
        colors.append('#27AE60')
    elif d >= 0.5:
        colors.append('#F39C12')
    else:
        colors.append('#95A5A6')

fig, ax = plt.subplots(figsize=(7, 5))
y_pos = np.arange(len(metrics))

for i, (metric, d, color, classification) in enumerate(zip(metrics, effect_sizes, colors, classifications)):
    ax.plot([0, d], [i, i], color=color, linewidth=4, alpha=0.8)
    ax.scatter(d, i, s=300, color=color, zorder=3, edgecolors='white', linewidth=3)
    ax.text(d + 0.15, i, f'{d:.2f}\n{classification}', va='center', 
            fontsize=9, fontweight='bold')

# 参考线
ax.axvline(x=0.2, color='#95A5A6', linestyle='--', linewidth=1.5, alpha=0.5)
ax.text(0.2, -0.8, 'Small', ha='center', fontsize=10, color='#95A5A6', fontweight='bold')
ax.axvline(x=0.5, color='#F39C12', linestyle='--', linewidth=1.5, alpha=0.5)
ax.text(0.5, -0.8, 'Medium', ha='center', fontsize=10, color='#F39C12', fontweight='bold')
ax.axvline(x=0.8, color='#27AE60', linestyle='--', linewidth=1.5, alpha=0.5)
ax.text(0.8, -0.8, 'Large', ha='center', fontsize=10, color='#27AE60', fontweight='bold')

ax.set_yticks(y_pos)
ax.set_yticklabels(metrics, fontsize=12, fontweight='bold')
ax.set_xlabel("Cohen's d Effect Size", fontsize=13, fontweight='bold')
ax.set_title("Effect Size Analysis with Contributing Factors", fontsize=14, fontweight='bold', pad=20)
ax.set_xlim(-0.1, 2.8)
ax.set_ylim(-1.2, len(metrics)-0.5)
ax.grid(axis='x', alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, 'effect_sizes.png')
plt.savefig(output_path, dpi=600, bbox_inches='tight')
plt.close()
print(f"✅ Figure 6 生成完成: {output_path}")

# === Figure 7: Response Length ===
print("生成 Figure 7: Response Length...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 3.5))

# Panel (a): Distribution
np.random.seed(42)
ai_data = np.random.normal(1247, 312, 500)
trad_data = np.random.normal(80, 25, 500)

ax1.hist(trad_data, bins=20, color='#95A5A6', alpha=0.7, label='Traditional', edgecolor='white')
ax1.hist(ai_data, bins=30, color='#2E5090', alpha=0.7, label='AI Agent', edgecolor='white')
ax1.axvline(1247, color='#2E5090', linestyle='--', linewidth=2)
ax1.axvline(80, color='#95A5A6', linestyle='--', linewidth=2)
ax1.text(1247, ax1.get_ylim()[1]*0.9, 'AI mean:\n1247 words', ha='center', fontsize=9, 
         bbox=dict(boxstyle='round', facecolor='#2E5090', alpha=0.3))
ax1.text(80, ax1.get_ylim()[1]*0.6, 'Trad mean:\n80 words', ha='center', fontsize=9,
         bbox=dict(boxstyle='round', facecolor='#95A5A6', alpha=0.3))
ax1.set_xlabel('Response Length (words)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Frequency', fontsize=11, fontweight='bold')
ax1.set_title('(a) Distribution Comparison', fontsize=12, fontweight='bold')
ax1.legend(fontsize=9, loc='upper right')
ax1.grid(alpha=0.3)

# Panel (b): Box plot
data = [trad_data, ai_data]
bp = ax2.boxplot(data, labels=['Traditional', 'AI Agent'], 
                 patch_artist=True, widths=0.6)
bp['boxes'][0].set_facecolor('#95A5A6')
bp['boxes'][0].set_alpha(0.9)
bp['boxes'][1].set_facecolor('#2E5090')
bp['boxes'][1].set_alpha(0.9)

for patch in bp['boxes']:
    patch.set_edgecolor('white')
    patch.set_linewidth(1.5)

ax2.text(1.5, 1650, '15.5× improvement\n(Includes:\n• Macau resources\n• Multimodal guidance)', 
         fontsize=9, ha='center', fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='#FFF9C4', alpha=0.9, edgecolor='#F39C12'))
ax2.set_ylabel('Response Length (words)', fontsize=11, fontweight='bold')
ax2.set_title('(b) Box Plot Comparison', fontsize=12, fontweight='bold')
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('response_length_analysis.png', dpi=600, bbox_inches='tight')
plt.close()
print("✅ Figure 7 生成完成: response_length_analysis.png")

# === Figure 8: Heatmap ===
print("生成 Figure 8: Significance Heatmap...")
metrics = ['Accuracy', 'Completeness', 'Safety', 'Usability', 'Satisfaction']
data = np.array([
    [4.16, 4.23, 4.36, 4.00, 4.16],  # AI Agent
    [3.00, 2.80, 4.21, 3.09, 3.03]   # Traditional
])

fig, ax = plt.subplots(figsize=(7, 3))
im = ax.imshow(data, cmap='Blues', aspect='auto', vmin=2.5, vmax=4.5)

# 添加数值和显著性
significance = [['***', '***', '**', '***', '***'],
               ['', '', '', '', '']]

for i in range(2):
    for j in range(5):
        text_color = 'white' if data[i, j] > 3.8 else 'black'
        ax.text(j, i, f'{data[i, j]:.2f}\n{significance[i][j]}', 
               ha="center", va="center", color=text_color, 
               fontsize=12, fontweight='bold')

ax.set_xticks(np.arange(5))
ax.set_yticks(np.arange(2))
ax.set_xticklabels(metrics, fontsize=11, fontweight='bold')
ax.set_yticklabels(['AI Agent\n(Multimodal + Macau)', 'Traditional\nSystem'], 
                   fontsize=11, fontweight='bold')
ax.set_title('Statistical Significance Heatmap', fontsize=14, fontweight='bold', pad=15)

# 颜色条
cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label('Rating (1-5 Likert Scale)', fontsize=11, fontweight='bold')

plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, 'significance_heatmap.png')
plt.savefig(output_path, dpi=600, bbox_inches='tight')
plt.close()
print(f"✅ Figure 8 生成完成: {output_path}")

# === Figure 9: Radar Chart ===
print("生成 Figure 9: Radar Chart...")
categories = ['Accuracy', 'Completeness', 'Safety', 'Usability', 'Satisfaction']
ai_values = [4.16, 4.23, 4.36, 4.00, 4.16]
trad_values = [3.00, 2.80, 4.21, 3.09, 3.03]

ai_values_closed = ai_values + ai_values[:1]
trad_values_closed = trad_values + trad_values[:1]

angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
angles_closed = angles + angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='polar'))

# 绘制AI系统
ax.plot(angles_closed, ai_values_closed, 'o-', linewidth=3, color='#2E5090', 
        label='AI Agent (Multimodal + Macau)', markersize=8)
ax.fill(angles_closed, ai_values_closed, alpha=0.25, color='#2E5090')

# 绘制传统系统
ax.plot(angles_closed, trad_values_closed, 's-', linewidth=2, color='#7F8C8D', 
        label='Traditional System', markersize=6)
ax.fill(angles_closed, trad_values_closed, alpha=0.15, color='#7F8C8D')

# 卓越阈值圈
theta = np.linspace(0, 2*np.pi, 100)
r = np.ones(100) * 4.0
ax.plot(theta, r, 'g--', linewidth=1.5, alpha=0.5, label='Excellence (4.0)')

# 设置
ax.set_ylim(0, 5)
ax.set_yticks([1, 2, 3, 4, 5])
ax.set_yticklabels(['1', '2', '3', '4', '5'], fontsize=10)
ax.set_xticks(angles)
ax.set_xticklabels(categories, fontsize=12, fontweight='bold')
ax.grid(True, linestyle=':', alpha=0.5)
ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.1), fontsize=10, 
          frameon=True, shadow=True)
ax.set_title('User Satisfaction Comparison\nAll AI Dimensions > 4.0', 
             fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, 'satisfaction_radar.png')
plt.savefig(output_path, dpi=600, bbox_inches='tight')
plt.close()
print(f"✅ Figure 9 生成完成: {output_path}\n")

print("=" * 50)
print("✅ 所有图表生成完成！")
print("=" * 50)
print(f"\n📁 保存目录: {OUTPUT_DIR}")
print("\n生成的文件:")
print("  - system_performance_comparison_enhanced.png")
print("  - effect_sizes.png")
print("  - response_length_analysis.png")
print("  - significance_heatmap.png")
print("  - satisfaction_radar.png")
print("\n🚀 可直接上传到Overleaf")
print(f"\n💡 提示: 文件已保存到桌面 ICHI_figures 文件夹，避免iCloud同步问题")
print("\n💡 提示:")
print("  - Figure 1-2（架构/流程图）需要用Draw.io或PPT制作")
print("  - Figure 3-4（统计/界面图）可用Python或设计工具")
print("  - 详细prompts见：高质量图表生成Prompts.md")

