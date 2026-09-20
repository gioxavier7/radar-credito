import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# 1. CONFIGURAÇÃO DAS PASTAS
# ============================================================

# Localização do projeto
pasta_projeto = Path(__file__).parent.parent

# Camada Gold
pasta_gold = pasta_projeto / 'ddm'

# Pasta da análise estatística
pasta_estatistica = pasta_projeto / 'estatistica'

# Pasta onde os gráficos serão salvos
pasta_graficos = pasta_estatistica / 'graficos'

# Criar as pastas caso não existam
pasta_graficos.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. CARREGAR OS DADOS DA CAMADA GOLD
# ============================================================

arquivo_gold = pasta_gold / 't_cred_modelagem_ddm.csv'

df = pd.read_csv(arquivo_gold)

# Converter período para data
df['periodo'] = pd.to_datetime(df['periodo'])


print('=' * 60)
print('ANÁLISE ESTATÍSTICA - RADAR CRÉDITO')
print('=' * 60)

print('\nDados carregados com sucesso!')
print(f'Quantidade de registros: {len(df)}')


# ============================================================
# 3. DEFINIR AS VARIÁVEIS ANALISADAS
# ============================================================

variaveis = [
    'inadimplencia_pf',
    'comprometimento_total',
    'comprometimento_sem_imob'
]


# ============================================================
# 4. ESTATÍSTICA DESCRITIVA
# ============================================================

print('\n' + '=' * 60)
print('1. ESTATÍSTICA DESCRITIVA')
print('=' * 60)


# Média
media = df[variaveis].mean()

# Mediana
mediana = df[variaveis].median()

# Moda
moda = df[variaveis].mode().iloc[0]

# Mínimo
minimo = df[variaveis].min()

# Máximo
maximo = df[variaveis].max()

# Amplitude
amplitude = maximo - minimo

# Variância
variancia = df[variaveis].var()

# Desvio padrão
desvio_padrao = df[variaveis].std()

# Quartis
q1 = df[variaveis].quantile(0.25)
q3 = df[variaveis].quantile(0.75)


# Criar tabela com os resultados
estatistica = pd.DataFrame({
    'Media': media,
    'Mediana': mediana,
    'Moda': moda,
    'Minimo': minimo,
    'Maximo': maximo,
    'Amplitude': amplitude,
    'Variancia': variancia,
    'Desvio_Padrao': desvio_padrao,
    'Q1': q1,
    'Q3': q3
})


print('\n')
print(estatistica.round(2))


# Salvar estatísticas
estatistica.round(2).to_csv(
    pasta_estatistica / 'estatistica_descritiva.csv'
)


# ============================================================
# 5. CORRELAÇÃO
# ============================================================

print('\n' + '=' * 60)
print('2. MATRIZ DE CORRELAÇÃO')
print('=' * 60)

correlacao = df[variaveis].corr()

print('\n')
print(correlacao.round(2))

# Salvar correlação
correlacao.round(2).to_csv(
    pasta_estatistica / 'correlacao.csv'
)


# ============================================================
# 6. GRÁFICO 1
# EVOLUÇÃO DA INADIMPLÊNCIA
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    df['periodo'],
    df['inadimplencia_pf'],
    marker='o'
)

plt.title('Evolução da Inadimplência de Pessoas Físicas')
plt.xlabel('Período')
plt.ylabel('Inadimplência (%)')

plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    pasta_graficos / '01_evolucao_inadimplencia.png',
    dpi=300
)

plt.close()


# ============================================================
# 7. GRÁFICO 2
# EVOLUÇÃO DOS COMPROMETIMENTOS
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    df['periodo'],
    df['comprometimento_total'],
    marker='o',
    label='Comprometimento Total'
)

plt.plot(
    df['periodo'],
    df['comprometimento_sem_imob'],
    marker='o',
    label='Comprometimento sem Imobiliário'
)

plt.title('Evolução dos Indicadores de Comprometimento')
plt.xlabel('Período')
plt.ylabel('Percentual (%)')

plt.xticks(rotation=45)
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    pasta_graficos / '02_evolucao_comprometimento.png',
    dpi=300
)

plt.close()


# ============================================================
# 8. GRÁFICO 3
# MÉDIA ANUAL DOS INDICADORES
# ============================================================

df['ano'] = df['periodo'].dt.year

media_anual = df.groupby('ano')[variaveis].mean()


plt.figure(figsize=(12, 6))

plt.plot(
    media_anual.index,
    media_anual['inadimplencia_pf'],
    marker='o',
    label='Inadimplência PF'
)

plt.plot(
    media_anual.index,
    media_anual['comprometimento_total'],
    marker='o',
    label='Comprometimento Total'
)

plt.plot(
    media_anual.index,
    media_anual['comprometimento_sem_imob'],
    marker='o',
    label='Comprometimento sem Imobiliário'
)

plt.title('Média Anual dos Indicadores de Crédito')
plt.xlabel('Ano')
plt.ylabel('Média (%)')

plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    pasta_graficos / '03_media_anual.png',
    dpi=300
)

plt.close()


# Salvar médias anuais
media_anual.round(2).to_csv(
    pasta_estatistica / 'media_anual.csv'
)


# ============================================================
# 9. GRÁFICO 4
# INADIMPLÊNCIA X COMPROMETIMENTO TOTAL
# ============================================================

plt.figure(figsize=(8, 6))

plt.scatter(
    df['comprometimento_total'],
    df['inadimplencia_pf']
)

plt.title(
    'Inadimplência PF x Comprometimento Total'
)

plt.xlabel('Comprometimento Total (%)')
plt.ylabel('Inadimplência PF (%)')

plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    pasta_graficos / '04_inadimplencia_x_comprometimento.png',
    dpi=300
)

plt.close()


# Correlação específica
corr_inad_comp = df[
    ['inadimplencia_pf', 'comprometimento_total']
].corr().iloc[0, 1]

print('\nCorrelação entre inadimplência e comprometimento total:')
print(round(corr_inad_comp, 2))


# ============================================================
# 10. GRÁFICO 5
# COMPROMETIMENTO TOTAL X SEM IMOBILIÁRIO
# ============================================================

plt.figure(figsize=(8, 6))

plt.scatter(
    df['comprometimento_total'],
    df['comprometimento_sem_imob']
)

plt.title(
    'Comprometimento Total x Comprometimento sem Imobiliário'
)

plt.xlabel('Comprometimento Total (%)')
plt.ylabel('Comprometimento sem Imobiliário (%)')

plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    pasta_graficos / '05_comprometimento_total_x_sem_imob.png',
    dpi=300
)

plt.close()


# Correlação específica
corr_comp = df[
    ['comprometimento_total', 'comprometimento_sem_imob']
].corr().iloc[0, 1]

print('\nCorrelação entre os indicadores de comprometimento:')
print(round(corr_comp, 2))


# ============================================================
# 11. GRÁFICO 6
# BOXPLOT DAS VARIÁVEIS
# ============================================================

plt.figure(figsize=(9, 6))

dados_boxplot = [
    df['inadimplencia_pf'].dropna(),
    df['comprometimento_total'].dropna(),
    df['comprometimento_sem_imob'].dropna()
]

plt.boxplot(
    dados_boxplot,
    labels=[
        'Inadimplência PF',
        'Comprometimento Total',
        'Comprometimento sem Imob.'
    ]
)

plt.title('Distribuição dos Indicadores de Crédito')
plt.ylabel('Percentual (%)')

plt.xticks(rotation=15)

plt.grid(True, axis='y', alpha=0.3)

plt.tight_layout()

plt.savefig(
    pasta_graficos / '06_boxplot.png',
    dpi=300
)

plt.close()


# ============================================================
# 12. FINALIZAÇÃO
# ============================================================

print('\n' + '=' * 60)
print('ANÁLISE CONCLUÍDA!')
print('=' * 60)

print(f'\nResultados estatísticos:')
print(pasta_estatistica)

print(f'\nGráficos:')
print(pasta_graficos)