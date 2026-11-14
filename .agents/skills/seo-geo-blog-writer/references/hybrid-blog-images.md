# Imagens híbridas para o blog da Unidcom

Use este padrão para transformar imagens geradas por IA em peças editoriais de blog consistentes, informativas e fáceis de revisar.

## Princípio

Separar a produção em duas camadas:

1. **Placa visual:** fotografia, ilustração, objetos, cenário ou metáfora gerados por IA.
2. **Composição editorial:** tipografia, dados, fluxos, destaques, logo, overlays e enquadramento feitos em HTML/CSS.

Não pedir ao modelo de imagem para gerar títulos, números, logos, interfaces ou diagramas finais. Esses elementos devem permanecer editáveis no HTML.

## Formato e arquivos

- Criar todos os artboards em `1200x675px` (16:9).
- Salvar as placas visuais em `Blog/<data>/imagens/`.
- Preservar as placas originais.
- Salvar os PNGs compostos com o sufixo `-editorial.png`.
- Manter o HTML de composição ao lado do artigo, com nome descritivo como `imagens-editoriais.html`.
- Usar caminhos relativos para as placas visuais.
- Manter o marcador `{{UNIDCOM_LOGO_DATA_URI}}` no HTML durante a composição e executar `scripts/inline_brand_assets.py` antes do render. O HTML final deve incorporar a logo oficial em Base64 e não depender de um arquivo externo de logo.

Estrutura recomendada:

```text
Blog/2026-08-01/
├── artigo.md
├── imagens-editoriais.html
└── imagens/
    ├── tema-capa.png
    ├── tema-capa-editorial.png
    ├── tema-processo.png
    └── tema-processo-editorial.png
```

## Planejamento editorial

Definir uma função diferente para cada imagem. Evitar repetir a mesma composição ou a mesma mensagem.

- **Capa:** apresentar a tensão central do artigo em até 10 palavras.
- **Metáfora de seção:** tornar uma mudança ou problema compreensível de imediato.
- **Processo:** mostrar uma sequência clara com 3 a 5 etapas.
- **Comparação:** contrapor atividade e resultado, antes e depois, risco e ação.
- **Evidência:** destacar um dado, consequência ou critério de decisão.
- **Aplicação:** traduzir o conteúdo em painel, checklist ou fluxo operacional.

## Direção da placa gerada por IA

Gerar em paisagem e informar a posição desejada do assunto. Reservar espaço negativo onde a copy será inserida.

Exigir sempre:

- nenhum texto ou número legível;
- nenhum logo ou marca de terceiros;
- nenhuma interface reconhecível;
- nenhuma marca d'água;
- assunto principal bem enquadrado;
- metáfora diretamente ligada ao conteúdo;
- área de respiro suficiente para a composição.

Evitar:

- pessoa de costas olhando para dashboard;
- telas genéricas com gráficos aleatórios;
- excesso de partículas, hologramas e elementos futuristas;
- cenas que dependem de texto gerado dentro da imagem;
- pessoas ou objetos cortados pela área reservada à copy.

## Alt text obrigatório

Definir o alt text antes de gerar a placa visual. Registrar para cada imagem:

| Arquivo final | Seção | Função editorial | Alt text |
|---|---|---|---|
| `tema-capa-editorial.png` | Introdução | Resumir a tese | Frase descritiva única |

Aplicar estas regras:

- Escrever uma frase curta que comunique a informação ou relação transmitida pela imagem.
- Descrever o significado editorial, não cores, decoração ou estilo fotográfico.
- Incluir a palavra-chave apenas quando ela surgir de forma natural.
- Diferenciar o alt text de todas as outras imagens do artigo.
- Quando houver processo, comparação ou fluxo, mencionar os elementos e a relação entre eles.
- Quando a imagem contiver copy visível, transmitir a mensagem essencial sem transcrever todo o layout.
- Evitar começar com “imagem de”, “foto de”, “arte de” ou “gráfico de”.
- Evitar repetir literalmente a headline, acumular palavras-chave ou usar nomes de arquivo como descrição.
- Usar uma frase de aproximadamente 80 a 160 caracteres quando isso couber naturalmente; clareza vale mais que contagem.

A placa usada como fundo dentro do HTML deve ter `alt=""`, pois é decorativa na composição. O PNG editorial final inserido no Markdown deve receber o alt text completo.

## Sistema visual

- Usar Montserrat, com fallback para Arial.
- Escolher uma única cor principal por artigo: laranja `#FF7C1A`, azul `#0A6DBF` ou verde `#13A24B`.
- Manter fundo escuro ou claro conforme contraste da placa, sem misturar várias cores principais.
- Usar exclusivamente uma logo oficial dos assets Base64 da skill; nunca reconstruir o logo por texto, iniciais, badge CSS, SVG improvisado ou geração por IA.
- Aplicar overlay para garantir contraste sem esconder o assunto.
- Limitar a copy a headline, apoio curto e, quando útil, um pequeno fluxo ou conjunto de indicadores.
- Usar números, setas, ícones e gráficos em HTML/CSS ou SVG inline.
- Não usar texto miúdo como decoração.

## Arquitetura de composição

Cada artboard deve conter apenas os elementos necessários:

```html
<section class="art" id="cover" data-output="tema-capa-editorial.png">
  <img class="photo" src="imagens/tema-capa.png" alt="">
  <div class="overlay"></div>
  <img class="brand" src="{{UNIDCOM_LOGO_DATA_URI}}" alt="Unidcom">
  <div class="copy">...</div>
</section>
```

Usar `assets/hybrid-blog-images-template.html` como base. Ele contém um conjunto aprovado de composições que deve ser adaptado ao novo tema. Copiar para a pasta do artigo antes de editar; não alterar o template durante uma produção comum.

Antes de renderizar, substituir o marcador pela variante oficial apropriada:

```bash
# Fundo escuro: wordmark totalmente branco
python scripts/inline_brand_assets.py Blog/<data>/imagens-editoriais.html --variant allwhite

# Fundo claro: wordmark totalmente preto
python scripts/inline_brand_assets.py Blog/<data>/imagens-editoriais.html --variant allblack
```

As variantes `color` e `white` também estão disponíveis para composições que exijam essas aplicações aprovadas. O script valida o Base64 e a assinatura PNG antes de alterar o HTML.

## Exportação

Executar:

```bash
node scripts/render_hybrid_images.js Blog/<data>/imagens-editoriais.html Blog/<data>/imagens
```

O renderizador procura elementos `.art`, usa `data-output` como nome do arquivo e, na ausência desse atributo, usa o `id`. Playwright deve estar disponível no ambiente.

## Validação visual obrigatória

Abrir todas as imagens exportadas e revisar:

- dimensão exata de 1200x675px;
- copy sem cortes ou sobreposição;
- título legível em miniatura;
- contraste suficiente;
- foto bem enquadrada;
- rosto, produto ou objeto principal visível;
- uma função editorial clara por imagem;
- consistência de cor e tipografia no conjunto;
- ausência de mojibake, texto instável ou ícones tipográficos frágeis;
- logo oficial completa e legível, sem substitutos textuais como `UNID`, `U` ou `Unidcom`.

Corrigir o HTML e exportar novamente quando qualquer item falhar.

## Inserção no artigo

- Referenciar somente os arquivos `-editorial.png` no Markdown.
- Inserir o alt text planejado de cada imagem, sem deixar campos vazios.
- Posicionar cada imagem logo após o título ou parágrafo que introduz sua função.
- Preservar as placas visuais como fonte para futuras revisões.
- Adicionar a URL pública da capa ao campo `image` do schema quando a URL final estiver disponível.
- Executar `python scripts/validate_image_alt_text.py <article.md>` e corrigir erros ou avisos relevantes antes da entrega.
