"""
Data Aggregation Module
=======================

Este módulo contém funções para agregar dados de métricas de modelos
armazenados em arquivos JSON.
"""

import os
import pandas as pd
import json
from utils.metrics import split_metrics


def aglomerar(folder):
    """
    Agrega dados de métricas de múltiplos arquivos JSON em um único DataFrame.
    
    Esta função processa todos os arquivos JSON em uma pasta, extrai informações
    sobre modelos e tarefas a partir dos nomes dos arquivos, e combina os dados
    de métricas em um DataFrame consolidado.
    
    Convenção de Nomenclatura dos Arquivos
    ---------------------------------------
    Os arquivos devem seguir o padrão: `prefix_modelname_task.json`
    ou `prefix_modelname_suffix_task.json`
    
    Exemplos de nomes válidos:
    - `results_bert_classification.json`
    - `results_gpt2_large_summarization.json`
    
    Parameters
    ----------
    folder : str
        Caminho para a pasta contendo os arquivos JSON com dados de métricas
        
    Returns
    -------
    pandas.DataFrame
        DataFrame consolidado contendo todas as métricas de todos os modelos,
        com as seguintes colunas principais:
        - model: Nome do modelo extraído do nome do arquivo
        - task: Nome da tarefa extraída do nome do arquivo
        - Colunas adicionais de metricsData (expandidas via split_metrics)
        - Outras colunas presentes em testCases
        
    Structure do JSON Esperado
    --------------------------
```json
    {
        "testCases": [
            {
                "metricsData": {...},
                "otherField1": "value1",
                "otherField2": "value2"
            }
        ]
    }
```
    
    Examples
    --------
    >>> df = aglomerar("/path/to/metrics/folder")
    >>> print(df.columns)
    Index(['model', 'task', 'accuracy', 'f1_score', ...])
    
    >>> print(df['model'].unique())
    ['bert', 'gpt2_large', 'roberta']
    
    Notes
    -----
    - Apenas arquivos com extensão .json são processados
    - A função split_metrics deve estar disponível em utils.metrics
    - Os dados de metricsData são expandidos em colunas separadas
    - Todos os DataFrames são concatenados ignorando o índice original
    
    Raises
    ------
    FileNotFoundError
        Se a pasta especificada não existir
    json.JSONDecodeError
        Se algum arquivo JSON estiver malformado
    KeyError
        Se a estrutura JSON não contiver a chave "testCases"
    """
    dfs = []

    for fname in os.listdir(folder):
        # Processa apenas arquivos JSON
        if not fname.endswith(".json"):
            continue
        # Extrai informações do nome do arquivo
        parts = fname.replace(".json", "").split("_")
        task = parts[-1]  
        # Determina o nome do modelo baseado na estrutura do nome
        if parts[2] == task: 
            model_name = parts[1]
        else: 
            # Formato: prefix_modelname_suffix_task
            model_name = parts[1] + "_" + parts[2]
        
        with open(os.path.join(folder, fname), 'r', encoding='utf-8') as f:
            data = json.load(f)["testCases"]

        df = pd.DataFrame(data)
        df["model"] = model_name
        df["task"] = task
        
        metrics_df = df["metricsData"].apply(split_metrics).apply(pd.Series)
        df = pd.concat([df.drop(columns=["metricsData"]), metrics_df], axis=1)

        dfs.append(df)

    # Combina todos os DataFrames em um único
    return pd.concat(dfs, ignore_index=True)

