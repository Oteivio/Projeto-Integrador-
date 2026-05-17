# 🖥️ Diretório do Dashboard (dashboard/)

Este diretório é dedicado aos arquivos fontes do painel analítico interativo, tais como os arquivos de projeto do Power BI (`.pbix`), pastas de projetos do Tableau (`.twbx`) ou scripts específicos de painéis Python (Streamlit/Dash).

---

## 🎨 Identidade Visual Corporativa (BMW Style Guide)

Para obter uma nota excelente no Projeto Integrador, é altamente recomendável que a identidade visual do dashboard reflita a sofisticação e sobriedade da marca **BMW**. Sugerimos a utilização da seguinte paleta de cores:

* **Cor Primária (Fundo Escuro ou Destaque):** Azul Marinho Escuro (`#061A40` ou `#002447`)
* **Cor Secundária (Freesh / Contraste):** Azul BMW Clássico (`#1C69D4` ou `#0066B2`)
* **Cor de Apoio (Texto e Detalhes):** Cinza Prateado Metálico (`#D1D5DB` ou `#E5E7EB`)
* **Cor de Fundo da Tela:** Branco contrastante para modo claro (`#F9FAFB`) ou Grafite Escuro para modo escuro (`#111827`).
* **Tipografia Recomendada:** Fontes sem serifa limpas e corporativas (como **Segoe UI**, **Helvetica** ou **Arial**).

---

## 🗺️ Mapa de Navegação das Telas

Recomendamos que o Dashboard seja estruturado em **3 visões centrais** para facilitar a navegação do usuário:

```text
  ┌──────────────────────────────────────────────────────────┐
  │                   MENU PRINCIPAL / FILTROS               │
  │     [Ano: Todos ▾]  [Região: Todas ▾]  [Combustível: ▾]  │
  └───────────────────────────┬──────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
  │   Painel 1   │     │   Painel 2   │     │   Painel 3   │
  │ Visão Macro  │     │ Geográfico   │     │ De Modelos   │
  │ (Faturamento │     │ (Mercados &  │     │ (Desempenho  │
  │   e Vendas)  │     │   Países)    │     │  de Séries)  │
  └──────────────┘     └──────────────┘     └──────────────┘
```

---

## 📝 Instruções de Conexão com os Dados

1. Certifique-se de que a base tratada em Python (`bmw_global_sales_2018_2025_cleaned.csv`) está devidamente exportada para a pasta `/data`.
2. Ao criar a conexão no seu software de BI (Power BI ou Tableau), utilize a importação do tipo **Texto/CSV** e selecione o caminho relativo para a pasta `/data`.
3. Verifique se o separador configurado na importação está de acordo com a exportação do Python (normalmente vírgula `,` ou ponto e vírgula `;`).
4. Garanta que a coluna `Ano` esteja configurada como tipo de dado "Não Resumir" para evitar que o Power BI tente somar os anos (ex: somar 2018 + 2019).
