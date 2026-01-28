from report_framework import (
    create_report,
    ReportTheme,
)
import pandas as pd
import numpy as np



def exemplo_pipeline():
    """Como integrar em um pipeline de dados"""
    
    def gerar_relatorio_vendas_mensal(mes, ano):
        """Função que seria chamada automaticamente todo mês"""
        
        # Simula busca de dados do banco
        vendas = pd.DataFrame({
            'Produto': ['A', 'B', 'C', 'D', 'E'],
            'Vendas': np.random.randint(1000, 5000, 5),
            'Meta': [3000, 3500, 2500, 4000, 3000]
        })
        
        vendas['% Meta'] = ((vendas['Vendas'] / vendas['Meta']) * 100).round(1)
        
        # Cria relatório
        report = create_report(
            title=f"Relatório de Vendas - {mes}/{ano}",
            theme=ReportTheme.CORPORATE
        )
        
        # Adiciona conteúdo
        total_vendas = vendas['Vendas'].sum()
        total_meta = vendas['Meta'].sum()
        atingimento = (total_vendas / total_meta * 100)
        
        report.add_kpi_grid(
            title="Resumo do Mês",
            kpis=[
                {'label': 'Total Vendido', 'value': f'R$ {total_vendas:,.0f}', 'trend': 'up'},
                {'label': 'Atingimento', 'value': f'{atingimento:.1f}%', 'trend': 'up'},
            ]
        )
        
        report.add_table(
            title="Detalhamento por Produto",
            data=vendas
        )
        
        # Salva com nome padrão
        filename = f"files/vendas_{ano}_{mes:02d}.pdf"
        report.generate(filename)
        
        return filename
    
    # Uso:
    arquivo = gerar_relatorio_vendas_mensal(mes=1, ano=2025)
    print(f"✅ Pipeline executado! Arquivo: {arquivo}")
