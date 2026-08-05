# Capítulo 18 — O Espelho da Entrega

**OCR • Tesseract • Pytesseract • Pillow • OpenCV • regex**

---

## O problema do livro

O Atacado era digital por inteiro — exceto no aceite de entregas.  
Papéis amassados, atrasados, quase ilegíveis. Motoristas e financeiro presos numa fila que não precisava existir.

Dona Fátima: *“O papel ainda precisa voltar (fiscal). Mas isso não quer dizer que a gente precisa esperar o papel pra começar o resto.”*

---

## A lição que mudou o jogo

OCR em 65%, 58%, 71%… travado.  
A professora de OpenCV olhou a foto e disse:

> “Você está tentando ensinar um algoritmo a ler uma foto que nem um ser humano conseguiria ler.  
> Antes de melhorar a inteligência… melhore a visão.”

Seu Bento resumiu: *“Tem gente que troca a máquina inteira quando só precisava limpar a lente.”*

---

## Pipeline

1. Motorista tira foto no app  
2. Upload para o servidor  
3. **Pré-processamento**: corte, contraste, perspectiva, alinhamento  
4. OCR extrai texto  
5. Visão computacional verifica assinatura **na linha certa**  
6. OK → sistema | Dúvida → revisão humana  

---

## Como executar

```bash
# Modo simulado (sempre funciona)
python ocr_aceite.py

# Modo real (opcional)
pip install opencv-python-headless pytesseract Pillow numpy
# + instalar Tesseract no sistema (apt/brew/windows installer)
```

---

## Conceitos-chave

| Conceito                | Tradução                                | Por que importa                          |
| ----------------------- | --------------------------------------- | ---------------------------------------- |
| **OCR**                 | Leitura automática de texto em imagem   | Elimina digitação manual do aceite       |
| **Região de interesse** | Recorte onde a assinatura deveria estar | Não procura assinatura em qualquer lugar |
| **Pré-processamento**   | Limpar a imagem antes do OCR            | Qualidade da entrada > modelo fancy      |
| **Revisão humana**      | Só os casos duvidosos                   | Reduz erro sem travar a operação         |

---

## PLUS deste capítulo

- Roda em modo simulado sem Tesseract
- Critérios explícitos de “OK” vs “revisão humana”
- Comentários alinhados à lição da professora

---

## Frase de ouro

> “O papel continua existindo. Mas ele para de mandar em tudo.”

---

## Link no GitHub

https://github.com/LuizFBarbosa/ondeocafeacaba/blob/main/capitulo_18/README.md
