from report_framework import (
    create_report,
    ReportTheme,
)
import pandas as pd


def exemplo_analise_tecnica():
    """Relatório técnico com análise estatística"""
    import numpy as np
    
    report = create_report(
        title="Análise de Performance - Sistema de Recomendação",
        theme=ReportTheme.MINIMAL
    )
    
    # Métricas de performance
    report.add_kpi_grid(
        title="Métricas de Modelo",
        kpis=[
            {'label': 'Acurácia', 'value': '94.2%', 'trend': 'up', 'change': '+2.1%'},
            {'label': 'Precisão', 'value': '91.8%', 'trend': 'up', 'change': '+1.5%'},
            {'label': 'Recall', 'value': '89.3%', 'trend': 'neutral', 'change': '-0.3%'},
            {'label': 'F1-Score', 'value': '90.5%', 'trend': 'up', 'change': '+0.8%'},
        ]
    )
    
    # Matriz de confusão
    confusion = pd.DataFrame({
        'Predito\\Real': ['Positivo', 'Negativo'],
        'Positivo': [4523, 412],
        'Negativo': [487, 3578]
    })
    
    report.add_table(
        title="Matriz de Confusão",
        data=confusion
    )
    
    # Comparação de algoritmos
    algoritmos = pd.DataFrame({
        'Algoritmo': ['Random Forest', 'XGBoost', 'Neural Network', 'SVM'],
        'Acurácia': [0.942, 0.938, 0.935, 0.921],
        'Tempo Treino (min)': [45, 62, 180, 28],
        'Tempo Inferência (ms)': [12, 8, 15, 5]
    })
    
    report.add_table(
        title="Comparação de Algoritmos",
        data=algoritmos
    )
    
    report.add_section(
        title="Conclusões",
        content="""
        O modelo Random Forest apresentou o melhor balanço entre acurácia
        e tempo de execução. Recomenda-se sua implementação em produção
        com monitoramento contínuo das métricas.
        """
    )
    
    pdf = report.generate("files/analise_modelo.pdf")
    print("✅ Análise técnica gerada!")
