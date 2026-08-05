# QR Codes dos Capítulos

Cada imagem aponta para o `README.md` do capítulo correspondente no GitHub:

**Base:** https://github.com/LuizFBarbosa/ondeocafeacaba

| Arquivo                               | Destino                         |
| ------------------------------------- | ------------------------------- |
| `00_readme_principal.png`             | README principal do repositório |
| `capitulo_01.png` … `capitulo_21.png` | README de cada capítulo         |

## Como usar no livro

1. Insira o QR Code no final de cada capítulo (ou na margem).
2. O leitor aponta a câmera do celular.
3. Vai direto para a página com código, dados e explicação passo a passo.

## Regenerar

```bash
pip install qrcode[pil]
python -c "
import qrcode
from pathlib import Path
base = 'https://github.com/LuizFBarbosa/ondeocafeacaba/blob/main'
for i in range(1, 22):
    img = qrcode.make(f'{base}/capitulo_{i:02d}/README.md')
    img.save(f'capitulo_{i:02d}.png')
"
```
