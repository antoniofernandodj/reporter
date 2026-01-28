from src.reporter.report_framework import (
    quick_report,
)
import pandas as pd


def exemplo_basico():
    """Relatório mais simples possível"""
    data = pd.DataFrame({
        'Produto': ['A', 'B', 'C'],
        'Vendas': [1000, 1500, 1200],
        'Lucro': [200, 300, 250]
    })
    
    pdf = quick_report(
        title="Relatório de Vendas",
        data=data,
        summary="Análise trimestral de vendas por produto",
        output_path="files/relatorio_basico.pdf"
    )
    
    print("✅ Relatório básico gerado!")
