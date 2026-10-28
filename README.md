# Detecção Forense de Adulterações em Fotografias Realizadas por Ferramentas de IA Generativa

Projeto acadêmico da disciplina de Processamento de Imagens — 2026/2.

## Objetivo

Este projeto investiga técnicas de processamento de imagens para localizar regiões alteradas em fotografias manipuladas por ferramentas de inteligência artificial generativa.

Nesta etapa, foi desenvolvido um pipeline experimental baseado na diferença entre uma fotografia original e sua versão manipulada. São comparadas a diferença absoluta entre imagens e uma variante que aplica suavização Gaussiana antes da segmentação.

**Limitação importante:** a implementação atual depende da imagem original correspondente. Portanto, o pipeline realiza a localização de diferenças entre duas imagens conhecidas; ele ainda não é um detector forense capaz de analisar uma fotografia isolada e determinar se ela foi adulterada por IA.

## Estrutura do projeto

```text
Projeto_Processamento_de_Imagens/
├── images/
│   ├── orig_testing/
│   ├── masks_testing/
│   └── sd2-sp_testing/
├── src/
│   ├── __init__.py 
│   ├── metrics.py
│   ├── inspect_dataset.py
│   ├── validate_dataset.py
│   ├── visualize_sample.py
│   ├── compare_thresholds.py
│   ├── analyze_results.py
│   ├── compare_gaussian.py
│   ├── visualize_thresholds.py
│   ├── visualize_methods.py
│   └── visualize_failure_case.py
├── results/
├── tests/
│   └── test_metrics.py
├── notebooks/
├── requirements.txt
└── README.md
```

A pasta `images/` contém as fotografias originais, as máscaras de referência e as versões manipuladas. A pasta `src/` contém os scripts de inspeção, validação, comparação e visualização, além da implementação compartilhada das métricas. A pasta `tests/` contém testes automatizados. Os resultados quantitativos são exportados para arquivos CSV em `results/`.

## Requisitos

- Python 3.12.5.
- Pip para instalação das dependências.
- Conjunto de dados extraído e organizado conforme a estrutura descrita acima.

As dependências e suas versões estão registradas em `requirements.txt`.

## Instalação

No terminal, na raiz do projeto, execute:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Caso o PowerShell impeça a ativação do ambiente virtual, consulte a política de execução do PowerShell ou execute os comandos utilizando diretamente o interpretador localizado em `.venv\Scripts\python.exe`.

## Execução dos experimentos

Execute os comandos a partir da raiz do repositório.

### 1. Inspeção e validação do conjunto de dados

```powershell
python -m src.inspect_dataset
python -m src.validate_dataset
```

O primeiro script contabiliza os arquivos encontrados. O segundo verifica a correspondência entre imagens manipuladas, imagens originais e máscaras de referência.

### 2. Visualização de uma amostra

```powershell
python -m src.visualize_sample
```

Permite inspecionar a imagem original, a versão manipulada, a máscara de referência e a diferença entre as imagens.

### 3. Comparação de limiares

```powershell
python -m src.compare_thresholds
python -m src.analyze_results
```

O experimento compara os limiares 15 e 30 utilizando a diferença absoluta entre as imagens. Os resultados por imagem são armazenados em `results/threshold_results.csv`, e o resumo estatístico é salvo em `results/threshold_summary.csv`.

### 4. Comparação com suavização Gaussiana

```powershell
python -m src.compare_gaussian
```

Compara a diferença absoluta com a diferença suavizada por um filtro Gaussiano de núcleo 5 × 5 e sigma 1,0, utilizando os limiares 15 e 30. Os resultados são armazenados em `results/method_comparison.csv`.

### 5. Visualização dos resultados e do caso de falha

```powershell
python -m src.visualize_thresholds
python -m src.visualize_methods
python -m src.visualize_failure_case
```

Esses scripts permitem examinar as máscaras previstas e comparar os erros de segmentação. Nas visualizações de erro, verde representa verdadeiros positivos, vermelho representa falsos positivos e azul representa falsos negativos.

### 6. Testes automatizados

```powershell
python -m unittest discover -s tests -v
```

Os testes verificam a implementação das métricas em situações controladas, incluindo previsão perfeita, sobreposição parcial, ausência de sobreposição, máscaras vazias e máscaras com dimensões incompatíveis.

## Metodologia e métricas

A diferença absoluta é calculada entre os canais de cor correspondentes das imagens original e manipulada. Em seguida, é obtido um mapa de diferença pela média das diferenças absolutas dos três canais BGR. Um limiar determina quais pixels serão considerados diferentes.

Na segunda abordagem, o mapa de diferença é suavizado por um filtro Gaussiano antes da aplicação do limiar. Essa operação reduz variações locais, mas também pode modificar os contornos e as extremidades das regiões detectadas.

As máscaras de referência são convertidas em máscaras binárias utilizando limiar de intensidade superior a 127.

A avaliação utiliza:

- **Precisão:** proporção de pixels previstos como alterados que correspondem à máscara de referência.
- **Revocação:** proporção de pixels da região de referência que foram identificados.
- **IoU (Intersection over Union):** área de interseção entre a máscara prevista e a máscara de referência dividida pela área de união das duas regiões.

As métricas são calculadas individualmente por imagem e resumidas por médias e desvios-padrão.

## Resultados principais

O experimento utilizou 50 fotografias originais distintas, selecionadas de forma reproduzível com a semente aleatória 42. As mesmas fotografias foram utilizadas na comparação entre os métodos.

| Método | Limiar | Precisão média | Revocação média | IoU média |
|---|---:|---:|---:|---:|
| Diferença absoluta | 15 | 0,9693 | 0,7183 | 0,6990 |
| Diferença absoluta | 30 | 0,9816 | 0,5577 | 0,5504 |
| Diferença + Gaussiano | 15 | 0,9618 | 0,7819 | **0,7519** |
| Diferença + Gaussiano | 30 | 0,9828 | 0,6159 | 0,6065 |

A combinação de suavização Gaussiana e limiar 15 obteve a maior IoU média entre as configurações avaliadas.

Em comparação com a diferença absoluta no limiar 15, a suavização aumentou a revocação média de 0,7183 para 0,7819 e a IoU média de 0,6990 para 0,7519, com redução da precisão média de 0,9693 para 0,9618.

Os resultados indicam que a suavização favoreceu a identificação das regiões de referência na amostra analisada, mas não melhorou todos os casos individuais. Em algumas imagens, alterou os contornos da região detectada e reduziu a precisão.

Os resultados completos e a análise visual de um caso de falha estão disponíveis nos arquivos de resultados e no relatório técnico do projeto.

## Limitações e próximos passos

A abordagem depende da imagem original correspondente e pode detectar diferenças causadas por compressão, redimensionamento ou outras transformações que não estejam relacionadas à adulteração por IA. A avaliação também está limitada a uma amostra de 50 fotografias e às configurações de limiar e suavização selecionadas.

Como continuidade, pretende-se investigar técnicas que permitam detectar ou localizar adulterações sem depender da imagem original, ampliar os testes e avaliar a generalização dos métodos para diferentes imagens e tipos de manipulação.

## Reprodutibilidade

Para reproduzir os experimentos:

1. Utilize Python 3.12.5 e instale as dependências registradas em `requirements.txt`.
2. Disponibilize o conjunto de dados na estrutura de diretórios descrita neste documento.
3. Execute os comandos a partir da raiz do repositório.
4. Preserve os arquivos CSV gerados e a versão do código utilizada nos experimentos.

Consulte o relatório técnico para a descrição detalhada da metodologia, dos resultados, da análise do caso de falha e das limitações do pipeline.