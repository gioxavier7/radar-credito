import pandas as pd
import os

# pasta de saída da Camada Silver
pasta_tgt = './tgt'

# cria a pasta caso ela não exista
os.makedirs(pasta_tgt, exist_ok=True)


# carregar os dados brutos da Camada Bronze
inad = pd.read_csv('./csl/t_cred_inad_csl.csv')
comp = pd.read_csv('./csl/t_cred_comp_csl.csv')

# remover registros duplicados
inad = inad.drop_duplicates()
comp = comp.drop_duplicates()

# converter período para data para realizar as operações temporais
inad['periodo'] = pd.to_datetime(inad['periodo'])
comp['periodo'] = pd.to_datetime(comp['periodo'])

# corrigir outlier de Jan/2022 na inadimplência
inad.loc[inad['periodo'] == '2022-01-01', 'inadimplencia_pf_bruto'] = 3.3

# renomear as colunas
inad = inad.rename(columns={
    'inadimplencia_pf_bruto': 'inadimplencia_pf'
})

comp = comp.rename(columns={
    'comprometimento_total_bruto': 'comprometimento_total',
    'comprometimento_sem_imob_bruto': 'comprometimento_sem_imob'
})

# união das tabelas em uma única base Silver consolidada
consolidado = pd.merge(
    inad,
    comp,
    on='periodo',
    how='inner'
).sort_values('periodo')

# formatar as datas de volta para texto
inad['periodo'] = inad['periodo'].dt.strftime('%Y-%m-%d')
comp['periodo'] = comp['periodo'].dt.strftime('%Y-%m-%d')
consolidado['periodo'] = consolidado['periodo'].dt.strftime('%Y-%m-%d')

# salvar arquivos saneados da Camada Silver
inad.to_csv(f'{pasta_tgt}/t_cred_inad_tgt.csv', index=False)
comp.to_csv(f'{pasta_tgt}/t_cred_comp_tgt.csv', index=False)
consolidado.to_csv(f'{pasta_tgt}/t_cred_cons_tgt.csv', index=False)

print("Camada Silver processada e salva com sucesso")