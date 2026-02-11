# Guia de Contribuição

Obrigado por estar interessado em contribuir para o Clustering Analysis Pipeline! Este documento fornece orientações e instruções para contribuir ao projeto.

## 🤝 Código de Conduta

Por favor, note que este projeto é lançado com um [Contributor Code of Conduct](CODE_OF_CONDUCT.md). Ao participar neste projeto você concorda em estar ligado pelos seus termos.

## 📋 Como Contribuir

### Relatando Bugs

Antes de criar um relatório de bug, verifique a [lista de issues](https://github.com/ArthurFachel/Clustering-Analysis-Pipeline/issues), pois o problema pode ter sido relatado.

Ao criar um relatório de bug, inclua o máximo de detalhes possível:

* **Use um título descritivo** para identificar o problema
* **Descreva os passos exatos** para reproduzir o problema
* **Forneça exemplos específicos** para demonstrar os passos
* **Descreva o comportamento observado** e **o que você esperava ver**
* **Inclua screenshots** (se aplicável)
* **Mencione sua versão do Python**, SO e outras configurações relevantes

### Sugestões de Melhorias

Se você tem uma sugestão de melhoria, inclua:

* **Um título descritivo**
* **Uma descrição detalhada** da funcionalidade sugerida
* **Exemplos práticos** de como deveria funcionar
* **Por que você acredita que isso seria útil** para a maioria dos usuários

## 🔧 Processo de Desenvolvimento

### Configuração Local

```bash
# 1. Fork o repositório
git clone https://github.com/seu_usuario/Clustering-Analysis-Pipeline.git
cd Clustering-Analysis-Pipeline

# 2. Configure o ambiente
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# 3. Instale dependências
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Ferramentas de desenvolvimento

# 4. Configure pre-commit hooks
pre-commit install

# 5. Crie uma branch para sua feature
git checkout -b feature/nome-da-feature
```

### Padrões de Código

* Siga [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* Use type hints quando possível
* Documente funções com docstrings estilo NumPy
* Mantenha máximo 100 caracteres por linha
* Use nomes descritivos para variáveis e funções

### Exemplo de Docstring

```python
def exemplo_funcao(parametro1, parametro2):
    """
    Descrição breve da função.
    
    Descrição mais longa se necessário, explicando o comportamento
    e casos de uso especiais.
    
    Parameters
    ----------
    parametro1 : str
        Descrição do parametro1
    parametro2 : int, optional
        Descrição do parametro2 (default é None)
        
    Returns
    -------
    dict
        Descrição do valor retornado
        
    Examples
    --------
    >>> resultado = exemplo_funcao("test", 10)
    >>> print(resultado)
    
    Notes
    -----
    Qualquer nota adicional sobre a função.
    
    Raises
    ------
    ValueError
        Quando... descrever o erro
    """
    pass
```

### Testing

```bash
# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=utils

# Executar testes específicos
pytest tests/test_clustering.py::test_kmeans
```

### Fluxo de Git

1. **Sempre comece a partir da branch main atualizada**
   ```bash
   git checkout main
   git pull origin main
   ```

2. **Crie uma branch com nome descritivo**
   ```bash
   git checkout -b fix/issue-123-bug-description
   git checkout -b feature/add-new-clustering-method
   git checkout -b docs/improve-readme
   ```

3. **Commit com mensagens claras**
   ```bash
   git commit -m "docs: Improve README with examples"
   git commit -m "feat: Add DBSCAN clustering method"
   git commit -m "fix: Resolve memory leak in embeddings"
   ```

4. **Push para seu fork**
   ```bash
   git push origin feature/nome-da-feature
   ```

5. **Abra um Pull Request**

## 📝 Convenções de Commit

Use o formato: `<tipo>: <assunto>`

**Tipos:**
- `feat:` Uma nova funcionalidade
- `fix:` Correção de um bug
- `docs:` Mudanças apenas em documentação
- `style:` Mudanças que não afetam código (espaços, vírgulas, etc)
- `refactor:` Mudança no código que não é feature nem fix
- `perf:` Mudança que melhora performance
- `test:` Adição ou atualização de testes
- `chore:` Mudanças em build, dependencies, etc

**Exemplos:**
```
feat: Add support for HDBSCAN clustering
fix: Correct metric calculation in hierarchical clustering
docs: Add clustering algorithm comparison table
refactor: Simplify embedding generation code
test: Add unit tests for metrics module
```

## 📤 Submissão de Pull Request

1. Atualize a documentação quando necessário
2. Adicione testes para novas funcionalidades
3. Garanta que todos os testes passam
4. Garanta que o código segue PEP 8
5. Aumente o número da versão (se aplicável)
6. Escreva uma descrição clara do PR

### Template PR

```markdown
## Descrição
Descrição clara do que foi mudado e por quê.

## Tipo de Mudança
- [ ] Bug fix
- [ ] Nova feature
- [ ] Breaking change
- [ ] Atualização de docs

## Testing
Descreva como testar as mudanças:

1. Passo um...
2. Passo dois...

## Checklist
- [ ] Meu código segue o estilo deste projeto
- [ ] Atualizei a documentação
- [ ] Adicionei testes para minhas mudanças
- [ ] Todos os testes passam
- [ ] Não há conflitos com a branch main
```

## 🧪 Criando Testes

Coloque testes em `tests/` seguindo a estrutura de módulos:

```
tests/
├── test_clustering.py
├── test_evaluation.py
├── test_metrics.py
└── test_utils_io.py
```

**Exemplo de teste:**

```python
import pytest
from utils.metrics import compute_score

def test_compute_score_with_tf_task():
    """Test score computation for T/F tasks."""
    row = {
        "task": "tf",
        "success": True,
        "answer_relevancy": None,
    }
    score = compute_score(row)
    assert score == 1.0
    
def test_compute_score_with_none_metrics():
    """Test score with all None metrics."""
    row = {
        "task": "qa",
        "answer_relevancy": None,
        "bert_similarity": None,
        "correctness_geval": None,
        "prompt_alignment": None,
    }
    score = compute_score(row)
    assert score is None
```

## 📚 Estrutura de Documentação

- Use Markdown para documentação
- Mantenha exemplos atualizados
- Documente dependências e requisitos
- Inclua troubleshooting comum

## 🔍 Revisão de Código

Todos os PRs serão revisados por maintainers. Nós procuramos por:

- ✅ Código bem escrito e testado
- ✅ Documentação clara
- ✅ Sem duplicação desnecessária
- ✅ Performance adequada
- ✅ Segurança

## ✨ Dúvidas?

Sinta-se livre para:
- Abrir uma issue com a tag `question`
- Entrar em contato via GitHub Discussions
- Revisar issues existentes para respostas

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a MIT License.

---

Obrigado por contribuir! 🎉
