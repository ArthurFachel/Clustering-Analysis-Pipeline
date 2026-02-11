# Changelog

Todos os tipos de mudanças notáveis ​​neste projeto será documentado neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-28

### Adicionado
- 🎉 Release inicial do Clustering Analysis Pipeline
- ✨ Implementação de K-Means clustering com suporte a múltiplos k
- ✨ Clustering Hierárquico Agglomerative com variantes Bottom-Top e Top-Down
- ✨ Suporte para HDBSCAN clustering (detector de outliers)
- ✨ Integração com Sentence Transformers para geração de embeddings semânticos
- 📊 Sistema de métricas multidimensionais:
  - Answer Relevancy
  - BERT Similarity
  - Correctness (GEval)
  - Prompt Alignment
- 🔌 Integração AWS para geração automática de descrições de clusters
- 📈 Pipeline de avaliação comparativa entre múltiplos modelos
- 📁 Sistema de agregação de dados (aglomerar)
- 💾 Exportação em CSV e TXT com nomeação automática
- 📚 Documentação completa do projeto
- 🧪 Exemplos de uso e casos de teste

### Ferramentas e Dependências
- pandas >= 1.3.0
- scikit-learn >= 1.0.0
- sentence-transformers >= 2.0.0
- numpy >= 1.19.0
- boto3 >= 1.18.0
- python-dotenv >= 0.19.0

### Documentação
- ✅ README.md completo com 20+ seções
- ✅ Guia de Contribuição (CONTRIBUTING.md)
- ✅ Código de Conduta (CODE_OF_CONDUCT.md)
- ✅ MIT License
- ✅ requirements.txt com todas as dependências
- ✅ .env.example com variáveis de configuração

### Estrutura de Projeto
- utils/run.py - Implementação dos algoritmos de clustering
- utils/evaluation.py - Funções de avaliação
- utils/metrics.py - Cálculo de métricas
- utils/aglomerar.py - Agregação de dados
- utils/assign.py - Atribuição de clusters
- utils/utils_IO.py - Funções de entrada/saída
- utils/AWS.py - Integração com AWS
- Clustering_Analysis_Pipeline.ipynb - Notebook principal

---

## Planejado para Futuras Versões

### v1.1.0 (Planejado)
- [ ] Suporte para UMAP redução de dimensionalidade
- [ ] Visualizações interativas com Plotly
- [ ] Testes unitários abrangentes
- [ ] CI/CD via GitHub Actions
- [ ] API REST para clustering

### v1.2.0 (Planejado)
- [ ] Suporte para mais modelos de embedding
- [ ] Clustering de imagens
- [ ] Dashboard web com Streamlit
- [ ] Comparação visual de dendrogramas
- [ ] Exportação para múltiplos formatos

### v2.0.0 (Planejado)
- [ ] Refatoração para package final
- [ ] Suporte para Deep Learning clustering
- [ ] Benchmarking automático
- [ ] GPU acceleration completa
- [ ] API de plugins customizados

---

## Notas de Versão

### Como Reportar Bugs
Se você encontrar um bug, por favor [abra uma issue](https://github.com/ArthurFachel/Clustering-Analysis-Pipeline/issues) com:
- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs. observado
- Sua configuração de ambiente

### Como Sugerir Melhorias
Para sugerir uma melhoria, por favor [abra uma issue](https://github.com/ArthurFachel/Clustering-Analysis-Pipeline/issues) com:
- Descrição detalhada
- Casos de uso
- Exemplos práticos

---

## Histórico de Versões

| Versão | Data | Status |
|--------|------|--------|
| 1.0.0 | 28/12/2024 | ✅ Lançado |
| 1.1.0 | TBD | 🚧 Em desenvolvimento |
| 1.2.0 | TBD | 📋 Planejado |
| 2.0.0 | TBD | 📋 Planejado |

---

> Para mais informações sobre mudanças futuras, veja a [Roadmap](./docs/ROADMAP.md) do projeto
