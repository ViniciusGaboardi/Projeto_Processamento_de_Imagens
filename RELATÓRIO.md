# Relatório M2 — Detecção Forense de Adulterações em Fotografias Realizadas por Ferramentas de IA Generativa

## 1. Objetivo

Esta etapa do projeto tem como objetivo implementar e avaliar um pipeline inicial de processamento de imagens para localizar regiões alteradas em fotografias modificadas por ferramentas de inteligência artificial generativa. A investigação compara duas abordagens de análise de diferenças entre uma imagem original e sua versão adulterada, considerando diferentes limiares de segmentação.

O trabalho busca verificar como a suavização Gaussiana influencia a qualidade da localização das regiões alteradas, utilizando métricas quantitativas e inspeção visual.

## 2. Conjunto de dados

Foram utilizadas imagens de um conjunto de dados público que contém fotografias originais, máscaras de referência e versões manipuladas. Os arquivos foram organizados em três diretórios:

- `images/orig_testing/testing/`: fotografias originais;
- `images/masks_testing/testing/`: máscaras de referência das regiões manipuladas;
- `images/sd2-sp_testing/testing/`: fotografias modificadas.

A inspeção inicial identificou 1.029 arquivos PNG de imagens originais, 3.428 máscaras e 2.058 imagens manipuladas. Na validação dos pares, foram encontradas 2.052 imagens manipuladas com correspondência exata de nome para a máscara e dimensões compatíveis. Seis arquivos manipulados não apresentaram uma máscara correspondente pelo critério de identificação utilizado.

Para a avaliação experimental, foram selecionadas 50 fotografias originais distintas. O procedimento utilizou uma semente fixa (`42`) para embaralhar os candidatos e selecionar no máximo uma versão manipulada por identificador de fotografia. Dessa forma, os métodos foram comparados sobre o mesmo conjunto de imagens.

## 3. Metodologia

### 3.1. Diferença absoluta entre imagens

A primeira abordagem calcula a diferença absoluta entre os valores dos pixels da imagem original e da imagem manipulada. Essa diferença é utilizada como indicador de alteração: valores maiores sugerem que o pixel sofreu uma mudança mais intensa entre as duas imagens.

Em seguida, aplica-se um limiar à diferença para gerar uma máscara binária prevista. Foram avaliados os limiares 15 e 30. Um limiar menor tende a identificar alterações mais sutis, mas também pode incluir diferenças que não correspondem à região manipulada.

### 3.2. Diferença com suavização Gaussiana

A segunda abordagem aplica um filtro Gaussiano à representação da diferença antes da limiarização. O filtro utilizado possui um núcleo de tamanho 5 × 5 e parâmetro sigma igual a 1,0.

A suavização busca reduzir variações locais e favorecer regiões de detecção mais contínuas. Entretanto, ela também pode modificar os contornos da região detectada e afetar a localização de estruturas estreitas.

Foram utilizados os mesmos limiares, 15 e 30, permitindo comparar as duas abordagens sob condições equivalentes.

### 3.3. Máscara de referência

As máscaras disponibilizadas pelo conjunto de dados foram convertidas em representações binárias utilizando limiar de intensidade 127. Os pixels classificados como pertencentes à região de interesse constituem a referência para a avaliação das máscaras previstas.

### 3.4. Métricas de avaliação

Foram utilizadas três métricas para avaliar a qualidade da segmentação:

- **Precisão (Precision):** proporção de pixels previstos como alterados que também pertencem à região indicada pela máscara de referência. Uma precisão elevada indica menor proporção de falsos positivos.
- **Revocação (Recall):** proporção dos pixels da região de referência que foram identificados pelo método. Uma revocação elevada indica menor proporção de falsos negativos.
- **Interseção sobre União (IoU):** razão entre a interseção das regiões previstas e de referência e a união dessas regiões. Essa métrica considera simultaneamente os acertos e os erros de localização.

As métricas foram calculadas individualmente para cada imagem e, depois, resumidas pela média e pelo desvio-padrão entre as 50 fotografias. Para a comparação entre métodos, também foi analisada a variação das métricas em cada imagem, permitindo identificar em quantos casos uma abordagem apresentou melhora.

## 4. Resultados

A tabela apresenta as médias obtidas nas 50 fotografias avaliadas.

| Método | Limiar | Precisão média | Revocação média | IoU média |
|---|---:|---:|---:|---:|
| Diferença absoluta | 15 | 0,9693 | 0,7183 | 0,6990 |
| Diferença absoluta | 30 | 0,9816 | 0,5577 | 0,5504 |
| Diferença + Gaussiano | 15 | 0,9618 | 0,7819 | 0,7519 |
| Diferença + Gaussiano | 30 | 0,9828 | 0,6159 | 0,6065 |

O melhor resultado médio de IoU foi obtido pela combinação de suavização Gaussiana e limiar 15, com valor de 0,7519. A maior precisão média foi observada com suavização Gaussiana e limiar 30, com valor de 0,9828.

Esses resultados mostram que a configuração com maior precisão não é necessariamente aquela que oferece a melhor sobreposição geral entre a segmentação prevista e a máscara de referência.

### 4.1. Influência do limiar

Na abordagem de diferença absoluta, a alteração do limiar de 15 para 30 aumentou a precisão média de 0,9693 para 0,9816. Em contrapartida, a revocação diminuiu de 0,7183 para 0,5577, e a IoU caiu de 0,6990 para 0,5504.

Esse comportamento é compatível com uma segmentação mais restritiva: o limiar maior reduz a quantidade de pixels classificados como alterados, diminuindo os falsos positivos, mas também deixando de identificar parte da região de referência.

A mesma tendência geral aparece na abordagem Gaussiana. Ao aumentar o limiar, a precisão média passou de 0,9618 para 0,9828, enquanto a revocação diminuiu de 0,7819 para 0,6159 e a IoU caiu de 0,7519 para 0,6065.

Portanto, a escolha do limiar envolve um compromisso entre precisão e cobertura da região alterada. Um limiar mais elevado pode tornar a previsão mais seletiva, mas essa seletividade não implica necessariamente uma localização mais próxima da máscara de referência.

### 4.2. Influência da suavização Gaussiana

Comparando os métodos sobre as mesmas imagens, a suavização Gaussiana elevou a IoU média de 0,6990 para 0,7519 no limiar 15, uma diferença de 0,0529. A revocação aumentou de 0,7183 para 0,7819, enquanto a precisão diminuiu de 0,9693 para 0,9618.

No limiar 30, a IoU média aumentou de 0,5504 para 0,6065, uma diferença de 0,0561. A revocação passou de 0,5577 para 0,6159, e a precisão aumentou ligeiramente, de 0,9816 para 0,9828.

A comparação individual também demonstra que a suavização não beneficia todas as fotografias. No limiar 15, a IoU aumentou em 47 das 50 imagens, enquanto a precisão aumentou em 18. No limiar 30, a IoU aumentou em 47 das 50 imagens, e a precisão aumentou em 38.

Os desvios-padrão das métricas de IoU também indicam variação entre as imagens. No limiar 15, por exemplo, o desvio-padrão foi de 0,1559 para a diferença absoluta e de 0,1606 para a abordagem Gaussiana. Assim, embora a média tenha melhorado, a dispersão dos resultados não desapareceu.

Em conjunto, os resultados indicam uma melhoria média de localização com a suavização Gaussiana para esse conjunto experimental, mas não demonstram que o filtro seja superior em todos os casos.

## 5. Análise de um caso de falha

A fotografia de identificador 289960 foi utilizada como exemplo de caso em que a suavização Gaussiana piorou a localização. No limiar 15, a abordagem de diferença absoluta obteve IoU de 0,7456, enquanto a abordagem com suavização Gaussiana obteve 0,7161. A redução foi de 0,0295.

Nesse caso, a revocação aumentou de 0,8663 para 0,9612, mas a precisão caiu de 0,8425 para 0,7374. Assim, o filtro identificou uma parcela maior dos pixels da região de referência, porém classificou também mais pixels fora dessa região como alterados.

A inspeção visual sugere que a suavização modificou os limites da região detectada, principalmente nas bordas e nas extremidades finas do objeto presente na fotografia. Uma hipótese é que a suavização, combinada com a limiarização, tenha alterado a distribuição dos valores próximos aos contornos, produzindo uma segmentação mais abrangente, mas menos precisa.

Esse caso ilustra que a melhoria da revocação não garante uma melhoria da IoU. A avaliação deve considerar conjuntamente a cobertura da região, a proporção de falsos positivos e a sobreposição espacial total.

## 6. Limitações

O método atual depende da disponibilidade da imagem original correspondente à fotografia manipulada. Ele identifica diferenças entre duas versões conhecidas da mesma imagem, em vez de determinar, a partir de uma única fotografia desconhecida, se ela foi adulterada por inteligência artificial generativa.

Além disso, diferenças entre imagens podem decorrer de alterações que não são necessariamente geradas por IA, como mudanças de compressão, redimensionamento, alinhamento ou processamento. Tais fatores podem influenciar a segmentação e gerar falsos positivos.

A avaliação foi realizada em uma amostra de 50 fotografias selecionadas do conjunto disponível. Embora a comparação seja controlada e utilize as mesmas imagens para ambos os métodos, os resultados não devem ser generalizados automaticamente para todos os tipos de imagem, ferramentas generativas ou técnicas de adulteração.

Por fim, as máscaras de referência são utilizadas como verdade-terreno para a avaliação, mas sua correspondência com os limites perceptuais de uma alteração pode depender de como o conjunto de dados foi construído.

## 7. Conclusão

Foi implementado um pipeline inicial de localização de regiões alteradas por meio da diferença absoluta entre imagens, com comparação entre dois limiares e uma variante com suavização Gaussiana. A avaliação em 50 fotografias demonstrou que o limiar influencia o equilíbrio entre precisão e revocação e que a suavização Gaussiana aumentou a IoU média nos dois limiares testados.

A combinação Gaussiana com limiar 15 apresentou a maior IoU média, de 0,7519. Entretanto, a análise de um caso em que o filtro piorou o resultado mostrou que a suavização pode aumentar a cobertura da região ao custo de uma delimitação menos precisa, sobretudo em estruturas estreitas.

Os resultados são promissores para uma etapa inicial de localização de diferenças, mas não comprovam, por si só, a capacidade de realizar detecção forense cega de imagens geradas ou modificadas por IA. Como continuidade, o projeto poderá investigar métodos que não dependam da imagem original, ampliar a avaliação para diferentes cenários de adulteração e estudar técnicas capazes de distinguir alterações generativas de outras fontes de diferença entre imagens.

## 8. Reprodutibilidade

Os experimentos foram implementados em scripts Python organizados no pacote `src/`. A execução deve ser realizada a partir do diretório raiz do projeto, com o ambiente virtual ativado e as dependências instaladas conforme o arquivo `requirements.txt`.

Os principais comandos utilizados foram:

```powershell
python -m src.inspect_dataset
python -m src.validate_dataset
python -m src.compare_thresholds
python -m src.analyze_results
python -m src.compare_gaussian
python -m unittest discover -s tests -v
```

Para gerar as visualizações utilizadas na inspeção dos resultados, foram executados:

```powershell
python -m src.visualize_sample
python -m src.visualize_thresholds
python -m src.visualize_methods
python -m src.visualize_failure_case
```

A avaliação experimental utiliza uma semente fixa (`42`) para a seleção das 50 fotografias, permitindo reproduzir a amostra quando o conjunto de dados e o procedimento de seleção são mantidos. Os resultados quantitativos são exportados para arquivos CSV no diretório `results/`, incluindo `threshold_results.csv`, `threshold_summary.csv` e `method_comparison.csv`.

Os testes automatizados das métricas são executados por meio do módulo `unittest`. Foram aprovados cinco testes que verificam a previsão perfeita, a sobreposição parcial, a ausência de sobreposição, o caso de máscaras vazias e a incompatibilidade entre dimensões.

A reprodução dos resultados depende da disponibilidade do conjunto de dados, da estrutura de diretórios esperada e das versões das dependências registradas em `requirements.txt`.