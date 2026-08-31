# Detecção Forense de Adulterações em Fotografias Realizadas por Ferramentas de IA Generativa

## 1. Problema

O avanço recente de ferramentas de Inteligência Artificial generativa tornou possível modificar fotografias de maneira cada vez mais realista. Técnicas como *generative fill* e *text-guided inpainting* permitem adicionar, remover ou substituir objetos e regiões de uma fotografia preservando grande parte da coerência visual da cena.

Essas alterações podem ser difíceis de identificar por inspeção visual, criando desafios para contextos nos quais é importante avaliar a autenticidade de uma imagem digital.

Este projeto propõe investigar técnicas de Processamento Digital de Imagens e visão computacional capazes de identificar indícios de adulteração em fotografias modificadas por ferramentas de IA generativa.

O problema principal será:

**Dada uma fotografia digital, determinar se ela apresenta indícios de adulteração realizada por uma ferramenta de IA generativa.**

Esse problema pertence ao campo de *digital image forensics*. Trabalhos recentes mostram que técnicas modernas de *inpainting* generativo representam um desafio para métodos tradicionais de localização de falsificações.

---

## 2. Contexto de aplicação

Fotografias digitais são utilizadas como fontes de informação em redes sociais, jornalismo, investigações, documentos, processos judiciais e comunicação institucional.

Ferramentas modernas de IA permitem modificar essas fotografias com poucos comandos. É possível, por exemplo:

* adicionar objetos inexistentes;
* remover pessoas ou objetos;
* substituir elementos da cena;
* reconstruir partes da fotografia;
* alterar semanticamente uma determinada região.

Nesse contexto, técnicas de análise forense podem auxiliar na identificação de imagens potencialmente adulteradas.

O objetivo do projeto não é determinar juridicamente se uma fotografia é verdadeira ou falsa, mas investigar **evidências computacionais que permitam diferenciar fotografias autênticas de fotografias modificadas por processos generativos**.

---

## 3. Objetivo geral

Desenvolver e avaliar um processo computacional para detectar indícios de adulterações realizadas por ferramentas de IA generativa em fotografias digitais.

## 3.1 Objetivos específicos

1. Investigar características visuais e estatísticas que possam diferenciar regiões originais de regiões produzidas por modelos generativos.

2. Selecionar um conjunto de fotografias originais e adulteradas adequado para experimentação.

3. Implementar um pipeline de pré-processamento e análise das imagens.

4. Investigar métodos de classificação capazes de determinar se uma fotografia é autêntica ou adulterada.

5. Comparar diferentes estratégias de processamento e representação das imagens.

6. Avaliar o desempenho do método utilizando métricas quantitativas.

7. Como evolução do projeto, investigar técnicas capazes de localizar a região modificada.

---

## 4. Delimitação do escopo

O projeto não pretende detectar qualquer tipo possível de imagem falsa.

O escopo inicial será limitado a:

**fotografias originalmente reais que tiveram uma ou mais regiões modificadas utilizando técnicas de IA generativa, principalmente inpainting generativo.**

Portanto, não serão o foco inicial:

* imagens inteiramente geradas por IA;
* deepfakes em vídeo;
* manipulação de áudio;
* identificação do modelo exato que realizou a alteração;
* determinação da intenção de quem modificou a imagem.

Essa delimitação permite manter o problema compatível com o tempo disponível durante a disciplina.

---

## 5. Entrada e saída esperadas

### Entrada

Uma fotografia digital, inicialmente nos formatos PNG ou JPEG.

Exemplo:

`fotografia suspeita → sistema`

### Saída principal

Uma classificação indicando a presença ou ausência de indícios de adulteração.

Exemplo:

`Fotografia provavelmente original`

ou

`Fotografia com indícios de adulteração por IA generativa`

Quando possível, o sistema também poderá apresentar um valor de confiança associado à decisão.

### Saída futura

Como evolução do projeto:

`fotografia → máscara/mapa das regiões suspeitas`

Nesse caso, além da classificação da fotografia, o sistema indicaria visualmente quais partes apresentam maior probabilidade de terem sido modificadas.

---

## 6. Conjunto inicial de imagens

O conjunto de dados inicialmente considerado será o **TGIF — Text-Guided Inpainting Forgery Dataset**.

O TGIF foi criado especificamente para pesquisas relacionadas à detecção e localização de adulterações realizadas por *text-guided inpainting*.

O conjunto original possui aproximadamente **75 mil imagens adulteradas**, produzidas utilizando:

* Stable Diffusion 2;
* Stable Diffusion XL;
* Adobe Photoshop/Firefly.

As fotografias originais utilizadas no dataset são provenientes do MS-COCO. O conjunto também possui máscaras correspondentes às regiões modificadas.

Uma extensão publicada em 2026, denominada **TGIF2**, acrescenta imagens produzidas por modelos FLUX.1. TGIF + TGIF2 totalizam aproximadamente 271 mil imagens manipuladas.

Para o projeto não será necessário utilizar inicialmente todo esse conjunto.

Na M1 poderá ser selecionada apenas uma pequena amostra representativa contendo:

* fotografias originais;
* fotografias adulteradas;
* máscaras correspondentes às regiões alteradas;
* exemplos produzidos por diferentes métodos generativos.

O enunciado permite utilizar na M1 apenas um conjunto inicial representativo, desde que seja possível demonstrar a plausibilidade da proposta.

### Licença

O repositório oficial do TGIF informa distribuição sob licença **CC BY-SA 4.0**. As condições de redistribuição e atribuição deverão ser respeitadas no repositório do projeto.

---

## 7. Pipeline preliminar

O pipeline inicial proposto é:

```text
Fotografia
    ↓
Carregamento e padronização
    ↓
Pré-processamento
    ↓
Extração/representação de características
    ↓
Análise ou classificação
    ↓
Original × Adulterada
    ↓
[Etapa futura]
Localização da região suspeita
```

### 7.1 Carregamento e padronização

Finalidade:

Garantir que as imagens tenham representação adequada para os métodos utilizados posteriormente.

Possíveis operações:

* leitura da imagem;
* conversão de espaços de cor;
* normalização;
* redimensionamento;
* separação dos canais de cor.

Entrada:

Fotografia original.

Saída:

Imagem padronizada para análise.

---

### 7.2 Pré-processamento

Finalidade:

Preparar a imagem e investigar quais representações evidenciam possíveis diferenças entre regiões naturais e regiões sintetizadas.

Técnicas inicialmente consideradas:

* análise RGB;
* conversão para outros espaços de cor;
* filtros;
* análise de ruído;
* análise de bordas;
* transformadas para análise no domínio da frequência.

Na M1 serão investigadas alternativas, sem necessidade de definir imediatamente uma única técnica.

---

### 7.3 Extração ou representação de características

Nesta etapa serão investigadas informações que possam evidenciar inconsistências introduzidas pelo processo generativo.

Exemplos de características a investigar:

* padrões de textura;
* distribuição de frequências;
* inconsistências de ruído;
* diferenças locais de intensidade;
* características obtidas a partir de regiões ou *patches* da imagem.

Também poderá ser investigado o uso de modelos de aprendizado de máquina para aprender automaticamente representações relevantes.

---

### 7.4 Classificação

A partir das características extraídas, será realizada inicialmente uma classificação binária:

```text
Original
   ou
Adulterada
```

Poderão ser avaliados métodos tradicionais de aprendizado de máquina e, dependendo dos resultados obtidos nas etapas anteriores, arquiteturas de aprendizado profundo.

A escolha definitiva será realizada durante o desenvolvimento experimental.

---

### 7.5 Localização da alteração

Esta etapa será considerada uma evolução do sistema.

O objetivo será produzir uma máscara indicando regiões com maior probabilidade de terem sido produzidas ou modificadas por IA.

O TGIF fornece máscaras das regiões adulteradas, permitindo comparar a localização prevista pelo sistema com a localização real da alteração.

---

## 8. Arquitetura preliminar

```text
             Dataset
                │
                ▼
       Carregamento das imagens
                │
                ▼
         Pré-processamento
                │
                ▼
       Extração de características
                │
                ▼
       Detector / Classificador
                │
        ┌───────┴────────┐
        ▼                ▼
     Original        Adulterada
                         │
                         ▼
                 Localização futura
                         │
                         ▼
                  Máscara/heatmap
```

A solução poderá ser dividida inicialmente nos seguintes módulos:

```text
data/
    gerenciamento das imagens

preprocessing/
    transformação e preparação

features/
    extração de características

detection/
    classificação

localization/
    localização das alterações

evaluation/
    métricas e análise dos resultados
```

Essa organização poderá ser alterada conforme os experimentos indiquem necessidades diferentes.

---

## 9. Tecnologias inicialmente previstas

A implementação deverá utilizar principalmente:

* Python;
* OpenCV;
* NumPy;
* Matplotlib;
* scikit-image;
* scikit-learn.

Caso sejam utilizados modelos de aprendizado profundo, poderão ser consideradas bibliotecas como:

* PyTorch;
* torchvision.

A escolha final dependerá dos experimentos realizados.

O enunciado permite livre escolha das tecnologias, desde que sejam adequadas ao problema e tecnicamente justificadas.

---

## 10. Estudo inicial de viabilidade

A proposta apresenta viabilidade por três razões principais.

### Disponibilidade de dados

Existem datasets públicos especificamente desenvolvidos para investigar adulterações produzidas por IA generativa.

O TGIF disponibiliza fotografias originais, versões adulteradas e máscaras indicando as regiões modificadas.

### Existência de literatura

A detecção e localização desse tipo de manipulação é um problema atualmente estudado na área de computação forense.

Os próprios autores do TGIF demonstram que adulterações modernas realizadas por modelos de difusão representam dificuldades para detectores forenses existentes, particularmente em condições de compressão e regeneração completa da imagem.

O TGIF2 demonstra ainda problemas de generalização quando detectores são expostos a adulterações produzidas por modelos generativos diferentes daqueles utilizados em seu desenvolvimento.

### Possibilidade de evolução incremental

O projeto pode começar com tarefas simples, como:

```text
Original × Adulterada
```

e posteriormente evoluir para:

```text
Detecção
+
Localização da adulteração
+
Análise de robustez
```

Assim, não é necessário resolver todo o problema desde a M1.

---

## 11. Experimentos preliminares propostos para M1

Para demonstrar viabilidade, serão selecionadas algumas fotografias do dataset TGIF.

Para cada exemplo deverão ser analisados:

1. fotografia original;
2. fotografia adulterada;
3. máscara da região modificada;
4. diferenças visuais entre original e adulterada.

Também poderão ser realizados experimentos simples:

* comparação de histogramas;
* análise dos canais RGB;
* análise de bordas;
* aplicação de filtros;
* análise de regiões modificadas;
* análise no domínio da frequência;
* comparação entre regiões autênticas e regiões geradas.

Cada experimento deverá registrar:

```text
Imagem de entrada
Método utilizado
Parâmetros
Resultado
Interpretação
```

Esse tipo de experimento está explicitamente dentro do que o enunciado considera adequado para a M1.

---

## 12. Avaliação

Para a etapa de detecção, poderão ser utilizadas métricas como:

* acurácia;
* precisão;
* recall;
* F1-score;
* matriz de confusão;
* ROC-AUC.

Para a futura etapa de localização poderão ser utilizadas métricas que comparem a máscara prevista com a máscara verdadeira disponibilizada pelo dataset.

A escolha definitiva das métricas será realizada de acordo com o método implementado.

O NIST também utiliza métricas como ROC-AUC, EER e taxas de verdadeiro positivo para avaliar sistemas de detecção de imagens relacionadas a IA generativa, fornecendo uma referência externa para avaliação desse tipo de sistema.

---

## 13. Principais dificuldades e riscos

Alguns desafios já identificados são:

### Generalização

Um detector pode funcionar bem para imagens produzidas por um modelo e falhar quando encontra adulterações produzidas por outro.

Esse comportamento foi observado em pesquisas recentes com o TGIF2.

### Compressão

Operações como compressão JPEG ou WEBP podem modificar os artefatos usados pelo detector.

O trabalho original do TGIF identificou perda de desempenho de métodos forenses após compressões mais intensas.

### Alterações muito pequenas

Quanto menor a área modificada, mais difícil poderá ser detectar a adulteração utilizando características globais da fotografia.

### Dependência do dataset

É necessário evitar que o sistema aprenda características específicas do dataset em vez de características relacionadas às adulterações.

Esses problemas serão considerados durante os experimentos.

---

## 14. Resultados esperados

Ao final do projeto espera-se produzir um processo capaz de receber uma fotografia e avaliar a presença de indícios de adulteração realizada por IA generativa.

O resultado mínimo esperado será:

```text
Fotografia
    ↓
Detector
    ↓
Original / Adulterada
```

Como resultado adicional, pretende-se investigar:

```text
Fotografia
    ↓
Detector
    ↓
Região suspeita
    ↓
Máscara / mapa visual
```

Não se pressupõe que o método consiga detectar perfeitamente todas as ferramentas de IA existentes.

O objetivo experimental será avaliar em quais condições os métodos escolhidos apresentam resultados satisfatórios e quais são suas limitações.

---

## 15. Evolução planejada

### M1 — Investigação e definição

* delimitação do problema;
* levantamento bibliográfico;
* obtenção do dataset;
* seleção das primeiras imagens;
* análise exploratória;
* definição do pipeline;
* primeiros experimentos de PDI;
* organização do repositório.

### M2 — Desenvolvimento

* implementação do pipeline;
* extração e comparação de características;
* desenvolvimento do detector;
* testes com fotografias originais e adulteradas;
* avaliação quantitativa;
* comparação entre alternativas.

### M3 — Refinamento e avaliação

* melhoria do detector;
* investigação da localização das regiões;
* testes com diferentes ferramentas generativas;
* avaliação de robustez;
* análise de generalização;
* documentação dos resultados e limitações.

---

## 16. Organização inicial do repositório

```text
ai-image-forensics/
├── README.md
├── docs/
│   └── proposta.md
├── images/
│   ├── input/
│   └── results/
├── src/
│   ├── preprocessing/
│   ├── features/
│   ├── detection/
│   └── evaluation/
├── notebooks/
│   └── exploracao.ipynb
├── tests/
├── requirements.txt
├── .gitignore
└── LICENSE
```

Na M1, pastas que ainda não tenham conteúdo não precisam necessariamente existir, conforme orientação do enunciado.

---

## 17. Uso de Inteligência Artificial generativa no desenvolvimento

Ferramentas de IA generativa foram utilizadas como apoio na estruturação inicial da proposta e na identificação de literatura, datasets e possíveis estratégias técnicas.

Todo conteúdo utilizado no projeto deverá ser verificado pelo grupo por meio das fontes técnicas citadas e da execução dos experimentos.

Durante o desenvolvimento serão registrados:

* ferramenta utilizada;
* finalidade;
* conteúdo produzido ou modificado;
* procedimento utilizado para verificar as informações.

Essa declaração atende à exigência de transparência sobre uso de IA generativa prevista no projeto.

---

## 18. Referências iniciais

MAREEN, H. et al. **TGIF: Text-Guided Inpainting Forgery Dataset**. IEEE International Workshop on Information Forensics and Security, 2024. DOI: 10.1109/WIFS61860.2024.10810690.

MAREEN, H. et al. **TGIF2: Extended Text-Guided Inpainting Forgery Dataset and Benchmark**. Journal on Information Security, 2026. DOI: 10.1186/s13635-026-00235-9.

IDLab / Ghent University. **TGIF & TGIF2: Text-Guided Inpainting Forgery Dataset**. Repositório oficial contendo dataset, metadados e código associado.

NIST. **GenAI — Image Discriminators / Text-to-Image Challenge**. Referência para avaliação de sistemas de detecção de conteúdo produzido por IA generativa.
