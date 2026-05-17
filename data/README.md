# 📂 Diretório de Dados (data/)

Este diretório é reservado para armazenar o conjunto de dados (dataset) bruto original e as eventuais bases de dados tratadas que serão geradas nas etapas de limpeza e transformação.

---

## 📍 Localização do Dataset

Para que todo o projeto funcione corretamente, o arquivo do dataset chamado exatamente **`bmw_global_sales_2018_2025.csv`** deve ser colocado nesta pasta.

### Caminho Completo no seu Computador:
📁 `c:\Users\jktgh\Documents\PROJETO INTEGRADOR\Projeto-Integrador--main\data\bmw_global_sales_2018_2025.csv`

---

## 📋 Dicionário de Dados Sugerido

Quando o arquivo `bmw_global_sales_2018_2025.csv` for integrado, espera-se que ele contenha as seguintes colunas ou que as seguintes transformações criem essa estrutura lógica:

1. **`Year`** (Inteiro): O ano em que as vendas foram registradas (2018 a 2025).
2. **`Month`** (Inteiro): O mês numérico de consolidação do registro (1 a 12).
3. **`Region`** (Texto): A macrorregião geográfica / Mercado da transação (`Europe`, `China`, `USA`, `RestOfWorld`).
4. **`Model`** (Texto): A série ou modelo específico do veículo da BMW (`3 Series`, `5 Series`, `X3`, `X5`, `X7`, `i4`, `iX`, `MINI`).
5. **`Units_Sold`** (Inteiro): Quantidade absoluta de veículos vendidos no registro.
6. **`Avg_Price_EUR`** (Decimal): Preço médio unitário de venda na categoria em Euros (€).
7. **`Revenue_EUR`** (Decimal): Faturamento bruto total do registro em Euros (`Units_Sold` * `Avg_Price_EUR`).
8. **`BEV_Share`** (Decimal): Proporção relativa de Veículos Elétricos a Bateria (100% elétricos) em relação ao total de vendas do registro.
9. **`Premium_Share`** (Decimal): Fração de mercado ocupada pela BMW no segmento premium daquele mercado.
10. **`GDP_Growth`** (Decimal): Crescimento percentual do PIB do mercado regional associado.
11. **`Fuel_Price_Index`** (Decimal): Índice de oscilação do preço do combustível no mercado local.

---

## 🛡️ Boas Práticas e Regras de Segurança

* **Nunca modifique o arquivo original diretamente:** Caso precise fazer alguma alteração manual, salve o arquivo modificado com outro nome (ex: `bmw_global_sales_2018_2025_limpo.csv`) ou, idealmente, faça todas as correções via código Python no diretório `/notebooks`.
* **Ignorar no Git (opcional):** Se a base de dados contiver informações extremamente sensíveis ou for pesada demais (acima de 50MB), é recomendado adicioná-la ao arquivo `.gitignore` do projeto para evitar travamentos no versionamento, mantendo no repositório apenas os scripts e o arquivo limpo compactado.
