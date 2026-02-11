import pandas as pd
import numpy as np
from typing import Any


def assign_clusters(model_df, embed_model, kmeans):
    """
    Atribui clusters a textos usando embeddings e modelo K-means.
    
    Esta função realiza três operações principais:
    1. Gera embeddings normalizados para os textos de entrada
    2. Prevê os clusters usando o modelo K-means treinado
    3. Adiciona a coluna 'cluster' ao DataFrame original
    
    Parameters
    ----------
    model_df : pandas.DataFrame
        DataFrame contendo os dados a serem clusterizados.
        Deve conter uma coluna 'input' com os textos para análise.
    embed_model : SentenceTransformer ou similar
        Modelo de embeddings pré-treinado que implementa o método encode().
        Exemplos: SentenceTransformer, OpenAI embeddings, etc.
    kmeans : sklearn.cluster.KMeans ou similar
        Modelo K-means já treinado que implementa o método predict().
        Deve ter sido previamente ajustado com fit() em dados similares.
        
    Returns
    -------
    pandas.DataFrame
        DataFrame original com uma nova coluna 'cluster' contendo
        os índices dos clusters atribuídos (0 a k-1, onde k é o
        número de clusters do modelo K-means).
        
    Examples
    --------
    >>> from sentence_transformers import SentenceTransformer
    >>> from sklearn.cluster import KMeans
    >>> 
    >>> # Preparar dados
    >>> df = pd.DataFrame({
    ...     'input': ['texto 1', 'texto 2', 'texto 3'],
    ...     'label': ['A', 'B', 'A']
    ... })
    >>> 
    >>> # Inicializar modelos
    >>> embed_model = SentenceTransformer('all-MiniLM-L6-v2')
    >>> kmeans = KMeans(n_clusters=2, random_state=42)
    >>> 
    >>> # Treinar K-means (em um dataset de treino)
    >>> train_embeddings = embed_model.encode(train_texts)
    >>> kmeans.fit(train_embeddings)
    >>> 
    >>> # Atribuir clusters
    >>> df_with_clusters = assign_clusters(df, embed_model, kmeans)
    >>> print(df_with_clusters['cluster'].value_counts())
    0    2
    1    1
    Name: cluster, dtype: int64
    
    Notes
    -----
    - A coluna 'input' é convertida para string antes da geração de embeddings
    - Os embeddings são normalizados (normalize_embeddings=True) para garantir
      que todos os vetores tenham magnitude unitária
    - Uma barra de progresso é exibida durante a geração dos embeddings
    - A função modifica o DataFrame original adicionando a coluna 'cluster'
    - Valores NaN ou None na coluna 'input' são convertidos para string "nan"
    
    Warnings
    --------
    - Certifique-se de que o modelo K-means foi treinado com embeddings
      do mesmo modelo de embedding usado aqui
    - A dimensionalidade dos embeddings deve corresponder à esperada pelo K-means
    - DataFrame grandes podem consumir muita memória durante a geração de embeddings
    
    See Also
    --------
    sklearn.cluster.KMeans : Algoritmo de clustering K-means
    sentence_transformers.SentenceTransformer : Modelo de embeddings de texto
    """
    # Gera embeddings normalizados para todos os textos
    # - astype(str): converte todos os valores para string (trata NaN, números, etc.)
    # - tolist(): converte Series do pandas para lista Python
    # - normalize_embeddings=True: normaliza vetores para magnitude unitária
    # - show_progress_bar=True: mostra barra de progresso durante processamento
    embeddings = embed_model.encode(
        model_df["input"].astype(str).tolist(),
        normalize_embeddings=True,
        show_progress_bar=True
    )

    # Prevê o cluster mais próximo para cada embedding
    model_df["cluster"] = kmeans.predict(embeddings)
    
    return model_df