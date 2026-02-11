
import time
import os
import requests
from pydantic import BaseModel
from typing import Union, Optional


def generate(
    input_text: str, 
    schema: Optional[BaseModel] = None,
    max_retries: int = 5,
    retry_delay: int = 10,
    request_delay: int = 3
) -> Union[str, BaseModel]:
    """
    Gera termos geológicos específicos a partir de um texto usando LLM da AWS.
    
    Esta função envia requisições para um endpoint AWS que hospeda um modelo
    de linguagem (LLM) para extrair até 3 termos geológicos ultra-específicos
    que resumem o texto fornecido. A função implementa retry automático em
    caso de falhas.
    
    Parameters
    ----------
    input_text : str
        Texto de entrada contendo informações geológicas a serem resumidas.
        Pode ser de qualquer comprimento, mas textos muito longos podem
        ser truncados pelo modelo dependendo do limite de tokens.
    schema : BaseModel, optional (default=None)
        Schema Pydantic para validação/estruturação da resposta.
        Atualmente não implementado, mas preparado para uso futuro.
    max_retries : int, optional (default=5)
        Número máximo de tentativas em caso de erro antes de desistir.
        Se None, tentará indefinidamente.
    retry_delay : int, optional (default=10)
        Tempo em segundos entre tentativas após falha.
    request_delay : int, optional (default=3)
        Tempo em segundos de espera antes de cada requisição
        (rate limiting preventivo).
        
    Returns
    -------
    str or BaseModel
        String contendo até 3 termos geológicos separados por underscores.
        Exemplo: "granito_metamorfico_gnaisse"
        
        Se schema for fornecido (funcionalidade futura), retorna instância
        do BaseModel validado.
        
    Environment Variables
    ---------------------
    AWS_ENDPOINT_URL : str
        URL do endpoint AWS onde o modelo LLM está hospedado.
        Exemplo: "https://xxxxx.execute-api.us-east-1.amazonaws.com/prod/generate"
    AWS_MODEL : str
        Identificador do modelo a ser usado.
        Exemplo: "anthropic.claude-v2", "meta.llama2-70b-chat-v1"
        
    Examples
    --------
    >>> texto = "Amostra de rocha ígnea com cristais de feldspato e quartzo"
    >>> termos = generate(texto)
    >>> print(termos)
    "granito_plutonica_fanerítica"
    
    >>> # Com tratamento de erro
    >>> try:
    ...     termos = generate(texto_longo, max_retries=3)
    ... except Exception as e:
    ...     print(f"Falha após 3 tentativas: {e}")
    
    Raises
    ------
    EnvironmentError
        Se as variáveis de ambiente AWS_ENDPOINT_URL ou AWS_MODEL não estiverem definidas.
    requests.exceptions.RequestException
        Se todas as tentativas de requisição falharem após max_retries.
    ValueError
        Se a resposta da API estiver em formato inesperado.
        
    Notes
    -----
    - A função implementa rate limiting automático (3s entre requisições)
    - Em caso de erro, aguarda 10s antes de tentar novamente
    - A temperatura baixa (0.1) garante respostas mais determinísticas
    - O prompt é otimizado para extrair termos técnicos de geologia
    - A função tenta indefinidamente por padrão (pode ser limitado com max_retries)
    
    Warnings
    --------
    - Certifique-se de que as credenciais AWS estão configuradas corretamente
    - Custos da AWS são incorridos a cada chamada da API
    - Textos muito longos podem exceder o limite de tokens do modelo
    - O delay de 3s pode tornar processamento em lote lento
    
    See Also
    --------
    requests.post : Documentação da biblioteca requests
    pydantic.BaseModel : Sistema de validação de dados
    """
    endpoint_url = os.getenv("AWS_ENDPOINT_URL")
    model_name = os.getenv("AWS_MODEL")
    
    if not endpoint_url:
        raise EnvironmentError(
            "AWS_ENDPOINT_URL não está definida. "
            "Configure a variável de ambiente antes de usar esta função."
        )
    
    if not model_name:
        raise EnvironmentError(
            "AWS_MODEL não está definida. "
            "Configure a variável de ambiente antes de usar esta função."
        )
    
    headers = {"Content-Type": "application/json"}
    
    prompt = (
        "Responda apenas com no máximo 3 termos ultra específicos de geologia "
        "que resuma todo o texto fornecido. Os termos devem estar espaçados "
        "por underscores. "
    )
    
    # Corpo da requisição
    body = {
        "prompt": prompt + input_text,
        "temperature": 0.1,  
        "top_p": 0.9,       
        "model": model_name,
        "max_tokens": 4096  
    }
    
    attempt = 0
    
    while max_retries is None or attempt < max_retries:
        attempt += 1
        
        # Rate limiting preventivo
        time.sleep(request_delay)
        
        try:
            response = requests.post(
                endpoint_url,
                json=body,
                headers=headers,
                timeout=60  # Timeout de 60 segundos
            )
            
            response.raise_for_status()
            
            # Parse da resposta JSON
            data_raw = response.json()
            output = data_raw.get("body", data_raw)

            # Retorna diretamente se já for string
            if isinstance(output, str):
                return output

            # Navega pela estrutura: response > output > message > content > text
            extracted_text = output["response"]["output"]["message"]["content"][0]["text"]
            return extracted_text
            
        except requests.exceptions.Timeout:
            print(f"Timeout na requisição (tentativa {attempt}/{max_retries}). Tentando novamente em {retry_delay}s...")
            
        except requests.exceptions.HTTPError as e:
            print(f"Erro HTTP {e.response.status_code}: {e}. Tentando novamente em {retry_delay}s...")
            
        except KeyError as e:
            print(f"Estrutura de resposta inesperada. Chave ausente: {e}. Tentando novamente em {retry_delay}s...")
            
        except Exception as e:
            print(f"Erro inesperado na geração: {e}. Tentando novamente em {retry_delay}s...")
        

        if max_retries is None or attempt < max_retries:
            time.sleep(retry_delay)
    
   
    raise RuntimeError(
        f"Falha ao gerar termos após {max_retries} tentativas. "
        "Verifique a conexão, credenciais AWS e logs acima."
    )

