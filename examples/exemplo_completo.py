from src.reporter.report_framework import (
    ReportTheme,
    ChartType,
    ReportConfig
)
import pandas as pd
from datetime import datetime



def exemplo_completo():
    """Relatório com todas as configurações personalizadas"""
    from src.reporter.report_framework import ReportBuilder
    
    # Configuração detalhada
    config = ReportConfig(
        title="Relatório Anual de Sustentabilidade",
        subtitle="Compromisso com o Futuro",
        author="João Silva",
        company="EcoTech Solutions",
        logo_path="logo.png",  # Se existir
        theme=ReportTheme.COLORFUL,
        date=datetime(2024, 12, 31),
        show_page_numbers=True,
        show_toc=True,
        header_text="Confidencial",
        footer_text="© 2024 EcoTech Solutions - Todos os direitos reservados",
        custom_css="""
        .section-title {
            color: #27ae60 !important;
        }
        """
    )
    
    report = ReportBuilder(config)
    
    # Seções do relatório
    report.add_section(
        title="Mensagem da Diretoria",
        content="""
        Em 2024, reafirmamos nosso compromisso com a sustentabilidade através
        de ações concretas que resultaram em impactos mensuráveis em nossa
        operação e comunidades.
        """
    )
    
    report.add_kpi_grid(
        title="Impacto Ambiental",
        kpis=[
            {'label': 'Redução CO₂', 'value': '-45%', 'trend': 'up', 'change': 'vs 2023'},
            {'label': 'Energia Renovável', 'value': '82%', 'trend': 'up', 'change': '+12%'},
            {'label': 'Reciclagem', 'value': '91%', 'trend': 'up', 'change': '+5%'},
        ]
    )
    
    # Dados de emissões
    emissoes = pd.DataFrame({
        'Ano': [2020, 2021, 2022, 2023, 2024],
        'Emissões (tCO₂)': [5200, 4800, 4200, 3500, 2850],
        'Meta': [5000, 4500, 4000, 3500, 3000]
    })
    
    report.add_table(
        title="Evolução das Emissões",
        data=emissoes
    )
    
    report.add_chart(
        title="Trajetória de Descarbonização",
        chart_type=ChartType.LINE,
        data={
            'Real': [5200, 4800, 4200, 3500, 2850],
            'Meta': [5000, 4500, 4000, 3500, 3000]
        },
        labels=['2020', '2021', '2022', '2023', '2024']
    )
    
    pdf = report.generate("files/relatorio_sustentabilidade.pdf")
    print("✅ Relatório completo gerado!")
