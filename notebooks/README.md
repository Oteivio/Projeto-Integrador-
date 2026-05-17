# 📓 Diretório de Notebooks (notebooks/)

Este diretório armazena todos os **Jupyter Notebooks (`.ipynb`)** gerados durante o ciclo de vida do projeto. O uso de notebooks é ideal para desenvolvimento de caráter científico e acadêmico, permitindo mesclar código vivo, equações, visualizações e textos explicativos.

---

## 🚦 Fluxo Sugerido de Execução

Para manter o projeto organizado e modularizado, os notebooks devem ser numerados sequencialmente na ordem de execução ideal:

1. **`01_limpeza_tratamento.ipynb`**
   * **Objetivo:** Importar o dataset bruto `bmw_global_sales_2018_2025.csv`, analisar tipos de dados, remover linhas nulas ou duplicadas e formatar colunas textuais.
   * **Saída:** Exportação de um arquivo limpo chamado `bmw_global_sales_2018_2025_cleaned.csv` na pasta `/data`.
2. **`02_analise_exploratoria.ipynb`**
   * **Objetivo:** Ingerir o arquivo tratado, rodar estatísticas descritivas (média, mediana, desvio padrão), calcular as taxas de crescimento composto (CAGR) e testar hipóteses analíticas sobre as vendas.
   * **Visualizações:** Gráficos estáticos gerados com `matplotlib` e `seaborn` para validação visual rápida das hipóteses.
3. **`03_modelagem_metricas.ipynb`** (Opcional)
   * **Objetivo:** Geração de tabelas de resumo e rollups agregados por país/modelo para facilitar a importação no Power BI ou Tableau.

---

## 💡 Estrutura Recomendada para um Notebook Acadêmico

Cada arquivo de notebook deve seguir uma estrutura textual clara para facilitar a leitura da banca avaliadora:

```text
├── 🏢 Título Principal (Markdown - H1)
├── 📝 Descrição do Objetivo daquele Notebook
├── 📦 Bloco de Importação de Bibliotecas (Pandas, Numpy, etc.)
├── 📥 Carga dos Dados (Caminhos Relativos: "../data/...")
├── 🛠️ Seção de Processamento (comentários em Markdown explicando cada passo)
├── 📊 Visualizações e Resultados Intermediários
└── 💾 Salvamento dos Resultados (Exportação da base limpa)
```

---

## 🔧 Como Executar os Notebooks

1. Certifique-se de que instalou as dependências listadas no `requirements.txt` na raiz do projeto:
   ```bash
   pip install -r requirements.txt
   ```
2. Abra o terminal (PowerShell ou Bash) na raiz do projeto e execute:
   ```bash
   jupyter notebook
   ```
3. Navegue até a pasta `notebooks/` no navegador que se abrirá automaticamente e selecione o notebook que deseja rodar.
