# Detecção Forense de Adulterações em Fotografias Realizadas por Ferramentas de IA Generativa

## Integrantes

* João Eduardo Cardoso
* Victor Hugo Chrisosthemos Teixeira
* Vinícius Gaboardi Silva

### Link do Vídeo no Youtube
https://youtu.be/lpn4-aHTndk

## Sobre o projeto

Este projeto investiga técnicas de Processamento Digital de Imagens e visão computacional para detectar adulterações realizadas por ferramentas de Inteligência Artificial generativa em fotografias digitais.

O foco inicial está em fotografias originalmente reais que tiveram regiões adicionadas, removidas ou substituídas utilizando técnicas de *generative inpainting*.

## Problema

Dada uma fotografia digital, queremos determinar se ela apresenta indícios de adulteração realizada por IA generativa.

## Entrada e saída

Entrada:

`Fotografia digital`

Saída inicial:

`Original / Adulterada`

Saída futura:

`Máscara ou mapa indicando regiões suspeitas`

## Dataset

Será utilizado inicialmente o **TGIF — Text-Guided Inpainting Forgery Dataset**, que contém fotografias modificadas utilizando Stable Diffusion 2, Stable Diffusion XL e Adobe Firefly, além das respectivas máscaras das regiões adulteradas.

## Pipeline preliminar

```text
Imagem
  ↓
Pré-processamento
  ↓
Extração de características
  ↓
Detecção/classificação
  ↓
Original × Adulterada
  ↓
Localização da região suspeita
```

## Tecnologias previstas

* Python
* OpenCV
* NumPy
* scikit-image
* scikit-learn
* Matplotlib
* PyTorch, caso necessário

## Estado atual

**M1 — definição e investigação da proposta.**

Atividades atuais:

* levantamento bibliográfico;
* investigação do dataset;
* seleção de imagens;
* planejamento do pipeline;
* experimentos preliminares.

## Organização

```text
docs/       documentação
images/     imagens utilizadas nos experimentos
src/        código-fonte
notebooks/  experimentos exploratórios
tests/      testes
```

## Documentação

A proposta detalhada está disponível em:

`docs/proposta.md`

## Vídeo da M1

[Adicionar link do vídeo não listado no YouTube]

## Uso de IA generativa

Ferramentas de IA generativa foram utilizadas como apoio à elaboração inicial da proposta e pesquisa de referências. As informações utilizadas são verificadas pelo grupo por meio das fontes técnicas e dos experimentos desenvolvidos.
