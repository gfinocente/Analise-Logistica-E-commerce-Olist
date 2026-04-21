import pandas as pd

# Ler arquivos principais
orders = pd.read_csv("olist_orders_dataset.csv")
customers = pd.read_csv("olist_customers_dataset.csv")
items = pd.read_csv("olist_order_items_dataset.csv")
reviews = pd.read_csv("olist_order_reviews_dataset.csv")
payments = pd.read_csv("olist_order_payments_dataset.csv")

# Mostrar tamanho de cada base
print("ORDERS:", orders.shape)
print("CUSTOMERS:", customers.shape)
print("ITEMS:", items.shape)
print("REVIEWS:", reviews.shape)
print("PAYMENTS:", payments.shape)

print("\nColunas de orders:")
print(orders.columns.tolist())

print("\nPrimeiras linhas de orders:")
print(orders.head())

import pandas as pd

# Ler dados
orders = pd.read_csv("olist_orders_dataset.csv")
payments = pd.read_csv("olist_order_payments_dataset.csv")

# Juntar tabelas
df = orders.merge(payments, on="order_id")

# Converter data
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

# Criar coluna de mês
df['mes'] = df['order_purchase_timestamp'].dt.to_period('M')

# Receita total
receita_total = df['payment_value'].sum()

print("\nReceita total:")
print(receita_total)

# Receita por mês
receita_mensal = df.groupby('mes')['payment_value'].sum()

# ======================
# ETAPA 3 - TICKET MÉDIO E CRESCIMENTO
# ======================

# Ticket médio por pedido
ticket_medio = df.groupby('order_id')['payment_value'].sum().mean()

print("\nTicket médio:")
print(ticket_medio)

# Crescimento mensal (%)
crescimento = receita_mensal.pct_change() * 100

print("\nCrescimento mensal (%):")
print(crescimento)

# ======================
# ETAPA 4 - ENTREGA VS SATISFAÇÃO
# ======================

reviews = pd.read_csv("olist_order_reviews_dataset.csv")

# juntar com base principal
df_full = df.merge(reviews, on="order_id")

# converter datas
df_full['order_delivered_customer_date'] = pd.to_datetime(df_full['order_delivered_customer_date'])
df_full['order_estimated_delivery_date'] = pd.to_datetime(df_full['order_estimated_delivery_date'])

# calcular atraso (em dias)
df_full['atraso'] = (df_full['order_delivered_customer_date'] - df_full['order_estimated_delivery_date']).dt.days

# média de avaliação por atraso
avaliacao_atraso = df_full.groupby('atraso')['review_score'].mean()

print("\nAvaliação média por atraso:")
print(avaliacao_atraso.head(20))

print("\nReceita por mês:")
print(receita_mensal)

# remover valores extremos (ruído)
df_full = df_full[(df_full['atraso'] > -30) & (df_full['atraso'] < 30)]

avaliacao_atraso = df_full.groupby('atraso')['review_score'].mean()

print("\nAvaliação média por atraso (filtrada):")
print(avaliacao_atraso)

import matplotlib.pyplot as plt

avaliacao_atraso.plot()

plt.title("Atraso vs Avaliação do Cliente")
plt.xlabel("Dias de atraso")
plt.ylabel("Nota média")

plt.show()

plt.figure(figsize=(10,5))
avaliacao_atraso.plot()

plt.grid()
plt.title("Atraso vs Avaliação do Cliente")
plt.xlabel("Dias de atraso")
plt.ylabel("Nota média")

plt.show()

# criar faixas de atraso
df_full['faixa_atraso'] = pd.cut(
    df_full['atraso'],
    bins=[-30, -10, -5, 0, 5, 10, 30],
    labels=['Muito cedo', 'Cedo', 'Leve atraso negativo', 'No prazo', 'Atraso leve', 'Atraso alto']
)

avaliacao_faixa = df_full.groupby('faixa_atraso')['review_score'].mean()

print(avaliacao_faixa)

# salvar base final
df_full.to_csv("base_final.csv", index=False)
