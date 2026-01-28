from src.reporter.report_framework import (
    create_report
)



def exemplo_multi_idioma():
    """Relatório com suporte a diferentes idiomas"""
    
    translations = {
        'pt': {
            'title': 'Relatório de Vendas',
            'summary': 'Resumo Executivo',
            'revenue': 'Receita',
            'customers': 'Clientes',
        },
        'en': {
            'title': 'Sales Report',
            'summary': 'Executive Summary',
            'revenue': 'Revenue',
            'customers': 'Customers',
        },
        'es': {
            'title': 'Informe de Ventas',
            'summary': 'Resumen Ejecutivo',
            'revenue': 'Ingresos',
            'customers': 'Clientes',
        }
    }

    # Gera em 3 idiomas
    for lang in ['pt', 'en', 'es']:
        t = translations[lang]
        report = create_report(title=t['title'])
        report.add_kpi_grid(
            title=t['summary'],
            kpis=[
                {'label': t['revenue'], 'value': '$ 2.5M', 'trend': 'up'},
                {'label': t['customers'], 'value': '342', 'trend': 'up'},
            ]
        )

        report.generate(f"files/report_{lang}.pdf")
        print(f"✅ Relatório gerado em {lang}")
