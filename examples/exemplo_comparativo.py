from src.reporter.report_framework import (
    create_report,
    ReportTheme,
)
import pandas as pd


def exemplo_comparativo():
    """Relatório comparando diferentes opções"""
    report = create_report(
        title="Análise de Fornecedores",
        theme=ReportTheme.MODERN
    )
    
    report.add_section(
        title="Objetivo",
        content="""
        Este relatório apresenta uma análise comparativa de três fornecedores
        potenciais para nosso projeto de expansão. A avaliação considera
        critérios de preço, qualidade, prazo de entrega e suporte técnico.
        """
    )
    
    # Comparação visual
    report.add_comparison(
        title="Comparação de Fornecedores",
        items=[
            {
                'name': 'Fornecedor A',
                'Preço': 'R$ 45K',
                'Qualidade': '⭐⭐⭐⭐⭐',
                'Prazo': '30 dias',
                'Suporte': '24/7'
            },
            {
                'name': 'Fornecedor B',
                'Preço': 'R$ 38K',
                'Qualidade': '⭐⭐⭐⭐',
                'Prazo': '45 dias',
                'Suporte': 'Horário comercial'
            },
            {
                'name': 'Fornecedor C',
                'Preço': 'R$ 52K',
                'Qualidade': '⭐⭐⭐⭐⭐',
                'Prazo': '20 dias',
                'Suporte': '24/7 + Dedicado'
            }
        ],
        comparison_fields=['Preço', 'Qualidade', 'Prazo', 'Suporte']
    )
    
    # Matriz de decisão
    matriz = pd.DataFrame({
        'Critério': ['Preço', 'Qualidade', 'Prazo', 'Suporte', 'Total'],
        'Peso': ['30%', '40%', '20%', '10%', '100%'],
        'Fornecedor A': [7, 10, 8, 10, 8.7],
        'Fornecedor B': [9, 8, 6, 5, 7.4],
        'Fornecedor C': [6, 10, 10, 10, 8.8]
    })
    
    report.add_table(
        title="Matriz de Decisão (Notas 0-10)",
        data=matriz
    )
    
    report.add_section(
        title="Recomendação",
        content="""
        <strong>Recomendamos o Fornecedor C</strong> com base na pontuação
        ponderada de 8.8, que demonstra excelência em qualidade, prazo e
        suporte. Apesar do investimento maior, o valor agregado justifica
        a diferença de preço.
        """,
        page_break_before=True
    )
    
    pdf = report.generate("files/analise_fornecedores.pdf")
    print("✅ Análise comparativa gerada!")
