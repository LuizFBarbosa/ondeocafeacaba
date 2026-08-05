# Como contribuir

Obrigado por querer melhorar o código do livro *Onde o Café Acaba, o Código Começa*! 🎉

Este repositório acompanha um livro físico — então algumas regras existem para manter tudo consistente com o que está impresso.

## O que é bem-vindo

- 🐛 **Correção de bugs** em qualquer script de qualquer capítulo
- 📝 **Melhorias no README** de um capítulo (mais clareza, mais exemplos, correção de erro de digitação)
- 🧪 **Testes adicionais** no `scripts/validar_capitulos.py`
- 💡 **Extensões didáticas** (ex.: uma versão do capítulo 10 com Prophet além da LSTM) — desde que fique claro que é uma *extensão* e não substitua o código original citado no livro

## O que evitar

- Trocar a lógica central de um capítulo de um jeito que não bata mais com a explicação do livro impresso (o leitor vai comparar os dois)
- Renomear pastas ou arquivos citados nos QR Codes sem atualizar `qrcodes/` e rodar `scripts/checar_qrcodes.py`
- Adicionar dependências pesadas (ex. um novo framework de ML) sem justificar no PR

## Passo a passo

1. Faça um fork do repositório
2. Crie uma branch: `git checkout -b fix/nome-da-correcao`
3. Se você editou alguma tabela Markdown, realinhe antes de commitar:
   ```bash
   pip install wcwidth
   python scripts/formatar_tabelas.py .
   ```
   Isso deixa as colunas com a mesma largura visual (estilo planilha), tanto
   no arquivo aberto em texto puro quanto renderizado no GitHub.
4. Rode a validação local antes de commitar:
   ```bash
   pip install -r requirements.txt
   python scripts/validar_capitulos.py
   ```
5. Se você mexeu em algum QR Code ou em URLs de capítulo:
   ```bash
   pip install pyzbar pillow
   python scripts/checar_qrcodes.py
   ```
6. Abra um Pull Request descrevendo:
   - Qual capítulo foi alterado
   - O que mudou e por quê
   - Se rodou a validação localmente (o CI do GitHub Actions também roda automaticamente)

## Dúvidas

Abra uma [Issue](https://github.com/LuizFBarbosa/ondeocafeacaba/issues) ou escreva para luizfbarbosa@gmail.com.
