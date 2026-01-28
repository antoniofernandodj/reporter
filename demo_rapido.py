#!/usr/bin/env python3
"""
DEMO: ReportMaster - Geração de Relatório em 30 segundos!

Este script demonstra como é ABSURDAMENTE SIMPLES gerar
um relatório profissional com o ReportMaster.

Execute: python demo_rapido.py
"""

from report_framework import create_report, ReportTheme, ChartType
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("=" * 60)
print("🚀 DEMO: ReportMaster Framework")
print("=" * 60)
print()

# ============================================================================
# PARTE 1: O Relatório Mais Simples (literalmente 3 linhas!)
# ============================================================================
print("📊 Criando relatório simples (3 linhas de código)...")

from report_framework import quick_report

dados_simples = pd.DataFrame({
    'Produto': ['Notebook', 'Mouse', 'Teclado', 'Monitor', 'Webcam'],
    'Quantidade': [150, 340, 280, 95, 120],
    'Valor Unitário': [3500, 45, 180, 1200, 250]
})

dados_simples['Total'] = dados_simples['Quantidade'] * dados_simples['Valor Unitário']

pdf_simples = quick_report(
    title="Relatório de Vendas Rápido",
    data=dados_simples,
    summary="Vendas de periféricos do mês de Janeiro/2025",
    output_path="/mnt/user-data/outputs/relatorio_simples.pdf"
)

print("   ✅ Relatório simples criado: relatorio_simples.pdf")
print()

# ============================================================================
# PARTE 2: Dashboard Executivo Completo (mais elaborado, mas ainda simples!)
# ============================================================================
print("📈 Criando dashboard executivo completo...")

# Gera dados fictícios realistas
np.random.seed(42)

# Dados de vendas mensais
vendas_mensais = pd.DataFrame({
    'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
    'Receita': [850000, 920000, 1050000, 980000, 1120000, 1250000],
    'Despesas': [520000, 540000, 610000, 590000, 650000, 720000],
    'Lucro': [330000, 380000, 440000, 390000, 470000, 530000]
})

# Dados por produto
vendas_produto = pd.DataFrame({
    'Categoria': ['Eletrônicos', 'Informática', 'Acessórios', 'Gaming'],
    'Unidades': [1250, 2340, 4580, 890],
    'Receita (R$)': [2850000, 4200000, 820000, 1350000],
    '% do Total': [31.5, 46.4, 9.1, 14.9],
    'Crescimento': ['+12%', '+18%', '+5%', '+22%']
})

# Top 5 vendedores
top_vendedores = pd.DataFrame({
    'Vendedor': ['Ana Silva', 'Carlos Santos', 'Maria Oliveira', 'João Costa', 'Paula Souza'],
    'Vendas': [1850000, 1620000, 1480000, 1350000, 1280000],
    'Metas': [1500000, 1500000, 1400000, 1300000, 1200000],
    '% Meta': [123.3, 108.0, 105.7, 103.8, 106.7]
})

# Cria o relatório
report = create_report(
    title="Dashboard Executivo - 1º Semestre 2025",
    theme=ReportTheme.EXECUTIVE
)

# Grid de KPIs principais
report.add_kpi_grid(
    title="Indicadores-Chave",
    kpis=[
        {
            'label': 'Receita Total',
            'value': 'R$ 6.17M',
            'trend': 'up',
            'change': '+47% vs 2024'
        },
        {
            'label': 'Lucro Líquido',
            'value': 'R$ 2.54M',
            'trend': 'up',
            'change': '+38%'
        },
        {
            'label': 'Margem',
            'value': '41.2%',
            'trend': 'up',
            'change': '+2.1pp'
        },
        {
            'label': 'Novos Clientes',
            'value': '1.847',
            'trend': 'up',
            'change': '+156'
        },
        {
            'label': 'Ticket Médio',
            'value': 'R$ 3.342',
            'trend': 'up',
            'change': '+8%'
        },
        {
            'label': 'NPS',
            'value': '82',
            'trend': 'neutral',
            'change': '±0'
        }
    ],
    columns=3
)

# Resumo executivo
report.add_executive_summary(
    highlights=[
        "Crescimento de 47% na receita total em relação ao mesmo período de 2024",
        "Margem de lucro aumentou 2.1 pontos percentuais, chegando a 41.2%",
        "Categoria Gaming apresentou o maior crescimento: +22%",
        "1.847 novos clientes adquiridos, superando a meta em 23%",
        "NPS mantido em 82 pontos, demonstrando alta satisfação dos clientes"
    ],
    metrics={
        'ROI Campanha': '385%',
        'CAC': 'R$ 285',
        'LTV': 'R$ 12.400',
        'Taxa Retenção': '94%'
    }
)

# Seção de contexto
report.add_section(
    title="Contexto do Período",
    content="""
    O primeiro semestre de 2025 foi marcado por uma expansão significativa das operações,
    com a abertura de 3 novos canais de distribuição e o lançamento da linha Gaming Premium.
    
    Os investimentos em marketing digital resultaram em um aumento de 156 novos clientes,
    enquanto a taxa de retenção se manteve sólida em 94%, indicando alta satisfação
    e qualidade dos produtos oferecidos.
    """,
    page_break_before=True
)

# Tabela de evolução mensal
report.add_table(
    title="Evolução Financeira Mensal",
    data=vendas_mensais
)

# Gráfico de evolução
report.add_chart(
    title="Tendência de Receita e Lucro",
    chart_type=ChartType.LINE,
    data={
        'Receita': vendas_mensais['Receita'].tolist(),
        'Lucro': vendas_mensais['Lucro'].tolist()
    },
    labels=vendas_mensais['Mês'].tolist()
)

# Nova seção para produtos
report.add_section(
    title="Análise por Categoria de Produto",
    content="""
    A categoria Informática continua sendo o principal driver de receita (46.4%),
    seguida por Eletrônicos (31.5%). O destaque do semestre foi Gaming, com
    crescimento de 22% impulsionado pelo lançamento de novos produtos.
    """,
    page_break_before=True
)

# Tabela de produtos
report.add_table(
    title="Performance por Categoria",
    data=vendas_produto
)

# Gráfico de participação
report.add_chart(
    title="Participação no Faturamento",
    chart_type=ChartType.PIE,
    data={
        'Participação': vendas_produto['Receita (R$)'].tolist()
    },
    labels=vendas_produto['Categoria'].tolist()
)

# Top vendedores
report.add_section(
    title="Performance da Equipe de Vendas",
    content="""
    Nossa equipe comercial superou as metas estabelecidas, com todos os top 5
    vendedores atingindo pelo menos 103% de suas metas individuais. Ana Silva
    liderou o ranking com 123% de atingimento.
    """,
    page_break_before=True
)

report.add_table(
    title="Top 5 Vendedores do Semestre",
    data=top_vendedores
)

# Comparação de canais
report.add_comparison(
    title="Análise de Canais de Venda",
    items=[
        {
            'name': 'E-commerce',
            'Participação': '52%',
            'Crescimento': '+28%',
            'Conversão': '3.2%',
            'Ticket Médio': 'R$ 2.850'
        },
        {
            'name': 'Lojas Físicas',
            'Participação': '35%',
            'Crescimento': '+12%',
            'Conversão': '18.5%',
            'Ticket Médio': 'R$ 4.200'
        },
        {
            'name': 'B2B',
            'Participação': '13%',
            'Crescimento': '+65%',
            'Conversão': '42%',
            'Ticket Médio': 'R$ 15.800'
        }
    ],
    comparison_fields=['Participação', 'Crescimento', 'Conversão', 'Ticket Médio']
)

# Conclusões e próximos passos
report.add_section(
    title="Conclusões e Recomendações",
    content="""
    <strong>Principais Conquistas:</strong>
    <ul>
        <li>Crescimento sustentável acima das projeções</li>
        <li>Expansão bem-sucedida do canal B2B</li>
        <li>Manutenção de margens saudáveis</li>
        <li>Alta satisfação dos clientes (NPS 82)</li>
    </ul>
    
    <strong>Recomendações para o 2º Semestre:</strong>
    <ul>
        <li>Expandir portfólio Gaming com novos lançamentos</li>
        <li>Investir em automação do canal B2B</li>
        <li>Implementar programa de fidelidade no e-commerce</li>
        <li>Abrir 2 novas lojas físicas em regiões estratégicas</li>
    </ul>
    """,
    page_break_before=True
)

# Gera o PDF
pdf_completo = report.generate("/mnt/user-data/outputs/dashboard_executivo.pdf")

print("   ✅ Dashboard executivo criado: dashboard_executivo.pdf")
print()

# ============================================================================
# RESUMO
# ============================================================================
print("=" * 60)
print("✨ DEMO CONCLUÍDA COM SUCESSO!")
print("=" * 60)
print()
print("📁 Arquivos gerados:")
print("   1. relatorio_simples.pdf - Exemplo básico (3 linhas de código)")
print("   2. dashboard_executivo.pdf - Dashboard completo e profissional")
print()
print("🎯 Viu como é fácil?")
print("   • Não precisou escrever HTML")
print("   • Não precisou escrever CSS")
print("   • Não precisou configurar templates")
print("   • Apenas chamou métodos simples e intuitivos!")
print()
print("💡 Próximos passos:")
print("   • Veja os arquivos PDF gerados")
print("   • Explore os exemplos em exemplos_uso.py")
print("   • Leia a documentação completa em README.md")
print("   • Customize com seus dados e sua marca!")
print()
print("🚀 Agora é só apresentar pro chefe e ver a aprovação!")
print("=" * 60)
