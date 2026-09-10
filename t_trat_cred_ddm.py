import pandas as pd
import os

# pastas de entrada (Silver) e saída (Gold)
pasta_tgt = './tgt'
pasta_gold = './ddm'

os.makedirs(pasta_gold, exist_ok=True)

# carrega a base consolidada da Camada Silver
consolidado = pd.read_csv(f'{pasta_tgt}/t_cred_cons_tgt.csv')
consolidado['periodo'] = pd.to_datetime(consolidado['periodo'])

# tabela Gold 1: Dataset de Modelagem Econométrica (Engenharia de Recursos)
# filtro de Período Seguro (2011 a 2025 - excluindo dados preliminares de 2026)
gold_modelagem = consolidado[
    (consolidado['periodo'] >= '2011-03-01') & 
    (consolidado['periodo'] <= '2025-12-31')
].copy().sort_values('periodo')

# cria defasagens temporais (Lags de 1, 3, 6, 11 e 12 meses)
for lag in [1-5]:
    gold_modelagem[f'comprometimento_total_lag_{lag}'] = gold_modelagem['comprometimento_total'].shift(lag)
    gold_modelagem[f'comprometimento_sem_imob_lag_{lag}'] = gold_modelagem['comprometimento_sem_imob'].shift(lag)

# cria variáveis de variação mensal
gold_modelagem['diff_inadimplencia_pf'] = gold_modelagem['inadimplencia_pf'].diff()
gold_modelagem['diff_comprometimento_total'] = gold_modelagem['comprometimento_total'].diff()

# reformata o campo de data para texto no padrão internacional (AAAA-MM-DD)
gold_modelagem['periodo'] = gold_modelagem['periodo'].dt.strftime('%Y-%m-%d')

#tabela Gold 2: Resumo Agregado Anual (Data Mart para Dashboards e Relatórios)
consolidado['ano'] = consolidado['periodo'].dt.year
gold_anual = consolidado.groupby('ano').agg(
    inadimplencia_pf_media=('inadimplencia_pf', 'mean'),
    inadimplencia_pf_max=('inadimplencia_pf', 'max'),
    inadimplencia_pf_min=('inadimplencia_pf', 'min'),
    comprometimento_total_medio=('comprometimento_total', 'mean'),
    comprometimento_sem_imob_medio=('comprometimento_sem_imob', 'mean')
).reset_index().round(2)

# salva os arquivos finais da Camada Gold
gold_modelagem.to_csv(f'{pasta_gold}/t_cred_modelagem_ddm.csv', index=False)
gold_anual.to_csv(f'{pasta_gold}/t_cred_resumo_anual_ddm.csv', index=False)

print("Camada Gold processada e salva com sucesso!")