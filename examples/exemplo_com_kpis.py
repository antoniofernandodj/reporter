from src.reporter.report_framework import (
    create_report,
    ReportTheme,
    ChartType,
)
import pandas as pd



def exemplo_com_kpis():
    """Relatório com indicadores chave"""
    report = create_report(
        title="Dashboard Executivo - Q1 2025",
        theme=ReportTheme.EXECUTIVE
    )
    
    # KPIs no topo
    report.add_kpi_grid(
        title="Indicadores Principais",
        kpis=[
            {'label': 'Receita Total', 'value': 'R$ 2.5M', 'trend': 'up', 'change': '+15%'},
            {'label': 'Novos Clientes', 'value': '342', 'trend': 'up', 'change': '+22%'},
            {'label': 'Taxa Conversão', 'value': '3.2%', 'trend': 'down', 'change': '-0.5%'},
            {'label': 'Ticket Médio', 'value': 'R$ 7.3K', 'trend': 'up', 'change': '+8%'},
        ],
        columns=4
    )
    
    # Resumo executivo
    report.add_executive_summary(
        highlights=[
            "Crescimento de 15% na receita em relação ao trimestre anterior",
            "Expansão significativa na base de clientes (342 novos)",
            "Lançamento de 3 novos produtos com boa aceitação",
            "Taxa de churn mantida abaixo de 2%"
        ],
        metrics={
            'MRR': 'R$ 833K',
            'CAC': 'R$ 450',
            'LTV': 'R$ 12K',
            'NPS': '78'
        }
    )
    
    # Dados detalhados
    vendas_por_produto = pd.DataFrame({
        'Produto': ['Premium', 'Standard', 'Basic'],
        'Unidades': [450, 1200, 2100],
        'Receita': [1350000, 960000, 420000],
        'Crescimento': ['18%', '12%', '8%']
    })
    
    report.add_table(
        title="Vendas por Produto",
        data=vendas_por_produto,
        page_break_before=True
    )
    
    # Gráfico
    report.add_chart(
        title="Evolução Mensal de Receita",
        chart_type=ChartType.LINE,
        data={
            'Janeiro': [800000],
            'Fevereiro': [850000],
            'Março': [900000]
        }
    )
    
    pdf = report.generate("files/dashboard_executivo.pdf")
    print("✅ Dashboard executivo gerado!")
