# Quick Start Guide

Comece a usar o Clustering Analysis Pipeline em 5 minutos!

## ⚡ Instalação Rápida

### 1. Clone e Setup
```bash
git clone https://github.com/ArthurFachel/Clustering-Analysis-Pipeline.git
cd Clustering-Analysis-Pipeline

# Crie environment Python
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configure Variáveis de Ambiente
```bash
cp .env.example .env
# Edite o arquivo .env com seus caminhos
```

### 3. Execute!
```bash
jupyter notebook Clustering_Analysis_Pipeline.ipynb
```

---

## 🎯 Seus Primeiros Clusters em Minutos

### Opção A: Usando Jupyter Notebook (Recomendado)

```python
from utils.run import kmeans_model
import os
from dotenv import load_dotenv

load_dotenv()

df, model = kmeans_model(chosen_k=5)

# Veja os resultados
print(df.head())
print(f"Total de pontos: {len(df)}")
print(f"Clusters: {df['cluster'].unique()}")
```

### Opção B: Comparar Todos os Métodos

```python
from utils.run import (
    kmeans_model,
    hierarchical_clustering_bottom_top,
    hierarchical_clustering_top_bottom
)

results = {
    "K-Means": kmeans_model(5),
    "Hierarchical (Bottom-Top)": hierarchical_clustering_bottom_top(5),
    "Hierarchical (Top-Down)": hierarchical_clustering_top_bottom(5),
}

# Analise os resultados
for name, (df, model) in results.items():
    print(f"{name}: {len(df)} pontos classificados")
```

### Opção C: Avaliar Modelos

```python
from utils.evaluation import evaluate_kmeans
from utils.aglomerar import aglomerar

# Agregar dados de múltiplos modelos
df_agregado = aglomerar("/path/to/model/results")

# Avaliar com K=5 clusters
results = evaluate_kmeans(models_folder="/path/to/models", i=5)

# Salvar resultados
results.to_csv("evaluation_kmeans_5.csv", index=False)
print("✅ Resultados salvos em evaluation_kmeans_5.csv")
```

---

## 📊 Estrutura dos Dados

### Dados de Entrada (JSON)
```json
{
  "qa": {
    "question": ["O que é ML?", "Como treinar um modelo?"],
    "answer": ["Machine Learning...", "Você precisa de dados..."],
    "task": "qa"
  },
  "tf": {
    "question": ["Python é compilado (T/F)?", "ML requer GPU (T/F)?"],
    "task": "tf"
  }
}
```

### Dados de Saída (CSV)
```
section,question,text,cluster,answer_relevancy,bert_similarity
qa,O que é ML?,O que é ML? Machine Learning...,0,0.95,0.92
tf,Python é compilado (T/F)?,Python é compilado (T/F)?,1,0.88,0.85
```

---

## 🔧 Configurações Comuns

### Alterar Modelo de Embedding
```python
# No seu código
from sentence_transformers import SentenceTransformer

# Modelo rápido (recomendado para começar)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Modelo mais preciso
model = SentenceTransformer("all-mpnet-base-v2")

# Modelo multilíngue
model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
```

### Ajustar Número de Clusters
```python
from utils.run import kmeans_model

# Testar diferentes Ks
for k in [3, 5, 10, 15, 20]:
    df, model = kmeans_model(chosen_k=k)
    print(f"K={k}: {len(df)} pontos")
```

### Salvar Resultados
```python
# CSV
df.to_csv("meus_clusters.csv", index=False)

# TXT (um arquivo por cluster)
from utils.utils_IO import save_txt_per_cluster
save_txt_per_cluster(df, "./output/clusters", "text")
```

---

## 🐛 Problemas Comuns

### ❌ "ModuleNotFoundError: No module named 'utils'"
**✅ Solução**: Certifique-se de executar do diretório raiz
```bash
cd Clustering-Analysis-Pipeline
python seu_script.py  # ✓ Correto
```

### ❌ "No such file or directory"
**✅ Solução**: Configure `.env` com caminhos corretos
```bash
cat .env  # Verify paths
```

### ❌ "CUDA out of memory"
**✅ Solução**: Use modelo menor de embedding
```python
model = SentenceTransformer("all-MiniLM-L6-v2")  # Mais leve
```

### ❌ "AWS credentials not configured"
**✅ Solução**: Configure variáveis AWS em `.env`
```bash
export AWS_KEY_ID="sua_chave"
export AWS_SECRET_KEY="sua_senha"
```

---

## 📚 Próximos Passos

### 1. Explore os Exemplos
```bash
# Abrir notebook principal
jupyter notebook Clustering_Analysis_Pipeline.ipynb
```

### 2. Leia a Documentação Completa
- [README.md](README.md) - Documentação detalhada
- [CONTRIBUTING.md](CONTRIBUTING.md) - Como contribuir
- [API Reference](docs/API.md) - Referência de funções

### 3. Experimente com Seus Dados
```python
from utils.utils_IO import json_to_df
from utils.run import kmeans_model

# Carregar seus dados
df_input = json_to_df("seu_arquivo.json")

# Executar clustering
df_result, model = kmeans_model(chosen_k=10)

# Explorar resultados
print(df_result.groupby('cluster').size())
```

---

## 🚀 Dicas Pro

### 1. Analise a Qualidade dos Clusters
```python
# Ver distribuição
print(df['cluster'].value_counts().sort_index())

# Ver métricas
print(df.groupby('cluster')['score'].agg(['mean', 'std']))
```

### 2. Customize a Avaliação
```python
# Criar métrica customizada
df['custom_metric'] = df['answer_relevancy'] * 0.7 + df['bert_similarity'] * 0.3
```

### 3. Combine Métodos
```python
# K-Means para segmentação inicial
df_kmeans, _ = kmeans_model(5)

# Hierarchical para análise profunda
df_hier, _ = hierarchical_clustering_bottom_top(5)

# Comparar
print(f"K-Means: {df_kmeans['cluster'].nunique()} clusters")
print(f"Hierarchical: {df_hier['cluster'].nunique()} clusters")
```

---

## 📧 Precisa de Ajuda?

- 🔍 [Issues no GitHub](https://github.com/ArthurFachel/Clustering-Analysis-Pipeline/issues)
- 📖 [Documentação Completa](README.md)
- 💬 [Discussões](https://github.com/ArthurFachel/Clustering-Analysis-Pipeline/discussions)

---

## ✨ O Que Testar A Seguir?

- [ ] Rodar com seus próprios dados JSON
- [ ] Comparar os 3 métodos de clustering
- [ ] Ajustar número de clusters
- [ ] Exportar resultados em CSV
- [ ] Usar diferentes modelos de embedding
- [ ] Avaliar com suas métricas custom
- [ ] Gerar resumos de clusters via AWS

Feliz clustering! 🎉
