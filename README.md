# ☕ Onde o Café Acaba, o Código Começa
## Debugando o Atacado

**Autor:** Luiz Fernando Barbosa  
**Site:** [www.ondeocafeacaba.com.br](https://www.ondeocafeacaba.com.br)  (em breve)
**E-mail:** luizfbarbosa@gmail.com  
**Repositório:** [https://github.com/LuizFBarbosa/ondeocafeacaba](https://github.com/LuizFBarbosa/ondeocafeacaba)

[![Validar código do livro](https://github.com/LuizFBarbosa/ondeocafeacaba/actions/workflows/validar-codigo.yml/badge.svg)](https://github.com/LuizFBarbosa/ondeocafeacaba/actions/workflows/validar-codigo.yml)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)
![Capítulos](https://img.shields.io/badge/capítulos-21%2F21%20validados-brightgreen)
![Licença](https://img.shields.io/badge/uso-educacional-orange)

---

## Sobre o livro

Este repositório contém **todo o código** do livro *Onde o Café Acaba, o Código Começa — Debugando o Atacado*.  

Cada capítulo possui:

- Código Python corrigido e executável
- Gerador de dados realistas (quando necessário)
- `README.md` completo com explicação passo a passo
- Instruções de uso e dependências

---

## Estrutura do repositório

```
ondeocafeacaba/
├── README.md                     ← você está aqui
├── LICENSE
├── CONTRIBUTING.md
├── requirements.txt
├── .github/workflows/
│   └── validar-codigo.yml        ← CI: valida todo capítulo a cada push
├── scripts/
│   ├── validar_capitulos.py      ← roda o mesmo teste do CI, localmente
│   └── checar_qrcodes.py         ← confere se os QR Codes apontam certo
├── qrcodes/                       ← QR Code de cada capítulo (para o livro impresso)
├── capitulo_01/ ... capitulo_21/  ← código + dados + README de cada capítulo
├── laboratorio/                   ← ferramenta bônus (limpador de planilhas)
└── apendice/                      ← fontes e referências reais citadas no livro
```

---

## Capítulos e códigos

Todos os códigos abaixo foram **executados e validados** (veja [status de validação](#status-de-validação)) antes desta publicação.

| Cap. | Título                               | Tecnologias principais                 |       Pasta        |              QR               |
| :--: | ------------------------------------ | -------------------------------------- | :----------------: | :---------------------------: |
|  01  | O Dia em que o Café Acabou           | pandas, openpyxl, smtplib              | [📂](capitulo_01/) | [📱](qrcodes/capitulo_01.png) |
|  02  | O Império das Planilhas              | pandas merge, limpeza de dados         | [📂](capitulo_02/) | [📱](qrcodes/capitulo_02.png) |
|  03  | O Mensageiro Digital                 | FastAPI, Pydantic, Requests            | [📂](capitulo_03/) | [📱](qrcodes/capitulo_03.png) |
|  04  | Uma Casa Decimal de Distância        | Circuit breaker, validação             | [📂](capitulo_04/) | [📱](qrcodes/capitulo_04.png) |
|  05  | Quando o Tempo Corre Demais          | concurrent.futures, ThreadPoolExecutor | [📂](capitulo_05/) | [📱](qrcodes/capitulo_05.png) |
|  06  | O Caçador de Erros                   | logging, throttle de alertas           | [📂](capitulo_06/) | [📱](qrcodes/capitulo_06.png) |
|  07  | O Radar de Oportunidades             | scikit-learn, SMOTE, Random Forest     | [📂](capitulo_07/) | [📱](qrcodes/capitulo_07.png) |
|  08  | O Cérebro Digital                    | FastAPI + ML, Redis, joblib            | [📂](capitulo_08/) | [📱](qrcodes/capitulo_08.png) |
|  09  | O Painel do Futuro                   | Streamlit, Plotly Express              | [📂](capitulo_09/) | [📱](qrcodes/capitulo_09.png) |
|  10  | A Máquina que Aprende Sozinha        | LSTM, TensorFlow/Keras                 | [📂](capitulo_10/) | [📱](qrcodes/capitulo_10.png) |
|  11  | A Tabela que Não Tinha Trinta Linhas | Governança, menor privilégio           | [📂](capitulo_11/) | [📱](qrcodes/capitulo_11.png) |
|  12  | O Jogo das Ideias                    | Gamificação, Streamlit, SQLite         | [📂](capitulo_12/) | [📱](qrcodes/capitulo_12.png) |
|  13  | A Máquina de Sentir                  | BERTimbau, regressão, anonimização     | [📂](capitulo_13/) | [📱](qrcodes/capitulo_13.png) |
|  14  | O Código e o Propósito               | Viés algorítmico, A/B Testing          | [📂](capitulo_14/) | [📱](qrcodes/capitulo_14.png) |
|  15  | O Mentor Digital                     | RAG, LLMs, ZiulBot                     | [📂](capitulo_15/) | [📱](qrcodes/capitulo_15.png) |
|  16  | O DNA do Conhecimento                | Recomendação, personalização           | [📂](capitulo_16/) | [📱](qrcodes/capitulo_16.png) |
|  17  | O Condutor Invisível                 | Celery, Celery Beat, Redis             | [📂](capitulo_17/) | [📱](qrcodes/capitulo_17.png) |
|  18  | O Espelho da Entrega                 | OCR, Tesseract, OpenCV                 | [📂](capitulo_18/) | [📱](qrcodes/capitulo_18.png) |
|  19  | O Guardião da Informação             | LGPD, hashing, auditoria               | [📂](capitulo_19/) | [📱](qrcodes/capitulo_19.png) |
|  20  | O Universo Paralelo                  | Monte Carlo, simulação de agentes      | [📂](capitulo_20/) | [📱](qrcodes/capitulo_20.png) |
|  21  | O Legado do Ziul                     | Documentação, cultura de dados         | [📂](capitulo_21/) | [📱](qrcodes/capitulo_21.png) |

---

## Status de validação

Este repositório **não é só código de exemplo — é testado**. Antes de cada publicação, os 21 capítulos passam por um pipeline automático:

| Verificação                                                            | Resultado |
| ---------------------------------------------------------------------- | :-------: |
| Sintaxe válida (`py_compile`) em 100% dos `.py`                        |    ✅     |
| Capítulos executados ponta a ponta (1, 2, 4–7, 10, 12–20, laboratório) |    ✅     |
| APIs testadas com `TestClient` (cap. 3 e 8)                            |    ✅     |
| Dashboard Streamlit sobe e responde (cap. 9)                           |    ✅     |
| SQL do cap. 11 validado contra cenário simulado                        |    ✅     |
| Os 22 QR Codes decodificados e conferidos                              |    ✅     |
| CI automático a cada `push` (GitHub Actions)                           |    ✅     |

Quer rodar a validação você mesmo?

```bash
pip install -r requirements.txt
python scripts/validar_capitulos.py
```

Capítulos que dependem de infraestrutura externa (Redis, Tesseract, TensorFlow, um servidor no ar) têm **modo de fallback didático** — o código roda mesmo sem a dependência pesada instalada, avisando no console que está em modo simulado. Isso está documentado no README de cada um desses capítulos.

---

## Como começar

```bash
# Clone o repositório
git clone https://github.com/LuizFBarbosa/ondeocafeacaba.git
cd ondeocafeacaba

# Crie um ambiente virtual (recomendado)
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# .venv\Scripts\activate    # Windows

# Instale as dependências
pip install -r requirements.txt
```

Depois entre na pasta do capítulo desejado e siga o `README.md` local.

---

## QR Codes — do papel para o código

Na pasta [`qrcodes/`](qrcodes/) você encontra um QR Code por capítulo (mais um para este README principal).

**Como funciona para o leitor:**
1. Encontra o QR Code impresso no final do capítulo (ou na margem da página).
2. Aponta a câmera do celular.
3. Cai direto no `README.md` daquele capítulo no GitHub — com o código, os dados de exemplo e a explicação passo a passo.

Todos os 22 QR Codes já foram gerados e **conferidos automaticamente** (decodificados um a um para garantir que apontam para a URL certa — veja `scripts/checar_qrcodes.py`). Se algum dia você mudar o nome do repositório ou o branch padrão, regenere-os com o script descrito em [`qrcodes/README.md`](qrcodes/README.md) e rode a checagem de novo antes de mandar pra gráfica.

---

## Como contribuir

Encontrou um bug, uma explicação confusa ou quer sugerir uma melhoria em algum capítulo? Veja o [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## Licença e uso

Este repositório é distribuído sob licença **MIT** (veja [`LICENSE`](LICENSE)), liberado para fins educacionais, alinhado ao espírito do livro.  
Mantenha os créditos ao autor ao reutilizar ou adaptar o material.

---

*"Toda porta existe por um motivo. Algumas apenas esperam a pessoa certa."*  
— Luiz Fernando Barbosa, 2026
