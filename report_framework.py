"""
ReportMaster - Framework declarativo para geração de relatórios profissionais
Usa Jinja2 + WeasyPrint em baixo nível, mas expõe API super abstrata
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union, Callable
from datetime import datetime
from pathlib import Path
from enum import Enum
from jinja2 import Template, Environment, BaseLoader
from weasyprint import HTML, CSS
import pandas as pd
from io import BytesIO
import base64


class ReportTheme(Enum):
    """Temas pré-definidos para relatórios"""
    CORPORATE = "corporate"
    MODERN = "modern"
    MINIMAL = "minimal"
    EXECUTIVE = "executive"
    COLORFUL = "colorful"


class ChartType(Enum):
    """Tipos de gráficos suportados"""
    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    AREA = "area"
    SCATTER = "scatter"


@dataclass
class Section:
    """Representa uma seção do relatório"""
    title: str
    content: Optional[str] = None
    subsections: List['Section'] = field(default_factory=list)
    data_table: Optional[pd.DataFrame] = None
    chart: Optional[Dict[str, Any]] = None
    custom_html: Optional[str] = None
    page_break_before: bool = False
    page_break_after: bool = False


@dataclass
class ReportConfig:
    """Configuração do relatório"""
    title: str
    subtitle: Optional[str] = None
    author: Optional[str] = None
    company: Optional[str] = None
    logo_path: Optional[str] = None
    theme: ReportTheme = ReportTheme.CORPORATE
    date: datetime = field(default_factory=datetime.now)
    show_page_numbers: bool = True
    show_toc: bool = True
    header_text: Optional[str] = None
    footer_text: Optional[str] = None
    custom_css: Optional[str] = None


class ReportBuilder:
    """Construtor de relatórios com API fluente"""
    
    def __init__(self, config: ReportConfig):
        self.config = config
        self.sections: List[Section] = []
        self._themes = self._load_themes()
        
    def add_section(
        self,
        title: str,
        content: Optional[str] = None,
        page_break_before: bool = False,
        page_break_after: bool = False
    ) -> 'ReportBuilder':
        """Adiciona uma seção de texto"""
        section = Section(
            title=title,
            content=content,
            page_break_before=page_break_before,
            page_break_after=page_break_after
        )
        self.sections.append(section)
        return self
    
    def add_table(
        self,
        title: str,
        data: Union[pd.DataFrame, List[Dict], Dict],
        highlight_rows: Optional[Callable] = None,
        page_break_before: bool = False
    ) -> 'ReportBuilder':
        """Adiciona uma tabela de dados com formatação automática"""
        if isinstance(data, dict):
            df = pd.DataFrame([data])
        elif isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = data
            
        section = Section(
            title=title,
            data_table=df,
            page_break_before=page_break_before
        )
        self.sections.append(section)
        return self
    
    def add_chart(
        self,
        title: str,
        chart_type: ChartType,
        data: Dict[str, List],
        labels: Optional[List[str]] = None,
        colors: Optional[List[str]] = None,
        page_break_before: bool = False
    ) -> 'ReportBuilder':
        """Adiciona um gráfico (renderizado como SVG/imagem)"""
        section = Section(
            title=title,
            chart={
                'type': chart_type.value,
                'data': data,
                'labels': labels,
                'colors': colors
            },
            page_break_before=page_break_before
        )
        self.sections.append(section)
        return self
    
    def add_kpi_grid(
        self,
        title: str,
        kpis: List[Dict[str, Any]],
        columns: int = 3
    ) -> 'ReportBuilder':
        """Adiciona um grid de KPIs (Key Performance Indicators)"""
        html = self._generate_kpi_html(kpis, columns)
        section = Section(
            title=title,
            custom_html=html
        )
        self.sections.append(section)
        return self
    
    def add_executive_summary(
        self,
        highlights: List[str],
        metrics: Dict[str, Any]
    ) -> 'ReportBuilder':
        """Adiciona um resumo executivo formatado"""
        html = self._generate_executive_summary_html(highlights, metrics)
        section = Section(
            title="Resumo Executivo",
            custom_html=html,
            page_break_after=True
        )
        self.sections.insert(0, section)
        return self
    
    def add_comparison(
        self,
        title: str,
        items: List[Dict[str, Any]],
        comparison_fields: List[str]
    ) -> 'ReportBuilder':
        """Adiciona uma comparação lado a lado"""
        html = self._generate_comparison_html(items, comparison_fields)
        section = Section(
            title=title,
            custom_html=html
        )
        self.sections.append(section)
        return self
    
    def generate(self, output_path: Optional[str] = None) -> bytes:
        """Gera o PDF do relatório"""
        html_content = self._build_html()
        css_content = self._build_css()
        
        html_obj = HTML(string=html_content)
        css_obj = CSS(string=css_content)
        
        pdf_bytes = html_obj.write_pdf(stylesheets=[css_obj])
        
        if output_path:
            Path(output_path).write_bytes(pdf_bytes)
        
        return pdf_bytes
    
    def _build_html(self) -> str:
        """Constrói o HTML completo do relatório"""
        template = Template(self._get_base_template())
        
        # Prepara dados para o template
        context = {
            'config': self.config,
            'sections': self._prepare_sections(),
            'date_formatted': self.config.date.strftime('%d/%m/%Y'),
            'logo_base64': self._get_logo_base64() if self.config.logo_path else None,
            'theme': self.config.theme.value
        }
        
        return template.render(**context)

    def _build_css(self) -> str:
        """Constrói o CSS do relatório baseado no tema"""
        base_css = self._themes[self.config.theme.value]

        if self.config.custom_css:
            base_css += f"\n\n/* Custom CSS */\n{self.config.custom_css}"

        return base_css

    def _prepare_sections(self) -> List[Dict]:
        """Prepara as seções para renderização"""
        prepared = []
        
        for section in self.sections:
            section_data = {
                'title': section.title,
                'content': section.content,
                'page_break_before': section.page_break_before,
                'page_break_after': section.page_break_after,
                'custom_html': section.custom_html
            }
            
            # Renderiza tabela se existir
            if section.data_table is not None:
                section_data['table_html'] = self._render_table(section.data_table)
            
            # Renderiza gráfico se existir
            if section.chart is not None:
                section_data['chart_html'] = self._render_chart(section.chart)
            
            prepared.append(section_data)
        
        return prepared

    def _render_table(self, df: pd.DataFrame) -> str:
        """Renderiza DataFrame como HTML formatado"""
        # Aplica formatação condicional
        html = '<div class="data-table-wrapper">'
        html += '<table class="data-table">'
        
        # Cabeçalho
        html += '<thead><tr>'
        for col in df.columns:
            html += f'<th>{col}</th>'
        html += '</tr></thead>'
        
        # Corpo
        html += '<tbody>'
        for _, row in df.iterrows():
            html += '<tr>'
            for val in row:
                # Formata valores numéricos
                if isinstance(val, (int, float)):
                    if isinstance(val, float):
                        formatted = f'{val:,.2f}'
                    else:
                        formatted = f'{val:,}'
                else:
                    formatted = str(val)
                html += f'<td>{formatted}</td>'
            html += '</tr>'
        html += '</tbody>'
        
        html += '</table></div>'
        return html

    def _render_chart(self, chart_config: Dict) -> str:
        """Renderiza gráfico como SVG inline ou imagem"""
        # Aqui você pode integrar com matplotlib, plotly, etc.
        # Por simplicidade, vou criar um placeholder
        chart_type = chart_config['type']
        data = chart_config['data']
        
        # Exemplo básico com matplotlib (requer matplotlib instalado)
        try:
            import matplotlib.pyplot as plt
            import io
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            if chart_type == 'bar':
                for label, values in data.items():
                    ax.bar(range(len(values)), values, label=label)
            elif chart_type == 'line':
                for label, values in data.items():
                    ax.plot(values, label=label, marker='o')
            elif chart_type == 'pie':
                values = list(data.values())[0]
                labels = chart_config.get('labels', [])
                ax.pie(values, labels=labels, autopct='%1.1f%%')
            
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Converte para base64
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            plt.close()
            buf.seek(0)
            img_base64 = base64.b64encode(buf.read()).decode()
            
            return f'<img src="data:image/png;base64,{img_base64}" class="chart-image" />'
        except ImportError:
            return '<div class="chart-placeholder">Gráfico (matplotlib não disponível)</div>'

    def _generate_kpi_html(self, kpis: List[Dict], columns: int) -> str:
        """Gera HTML para grid de KPIs"""
        html = f'<div class="kpi-grid kpi-grid-{columns}">'
        
        for kpi in kpis:
            trend = kpi.get('trend', 'neutral')
            trend_icon = '↑' if trend == 'up' else '↓' if trend == 'down' else '→'
            trend_class = f'trend-{trend}'
            
            html += f'''
            <div class="kpi-card">
                <div class="kpi-label">{kpi['label']}</div>
                <div class="kpi-value">{kpi['value']}</div>
                <div class="kpi-trend {trend_class}">
                    <span class="trend-icon">{trend_icon}</span>
                    <span class="trend-text">{kpi.get('change', '')}</span>
                </div>
            </div>
            '''
        
        html += '</div>'
        return html

    def _generate_executive_summary_html(
        self,
        highlights: List[str],
        metrics: Dict[str, Any]
    ) -> str:
        """Gera HTML para resumo executivo"""
        html = '<div class="executive-summary">'
        
        # Métricas principais
        if metrics:
            html += '<div class="summary-metrics">'
            for key, value in metrics.items():
                html += f'''
                <div class="summary-metric">
                    <span class="metric-label">{key}:</span>
                    <span class="metric-value">{value}</span>
                </div>
                '''
            html += '</div>'
        
        # Highlights
        if highlights:
            html += '<div class="summary-highlights">'
            html += '<h4>Destaques:</h4>'
            html += '<ul class="highlights-list">'
            for highlight in highlights:
                html += f'<li>{highlight}</li>'
            html += '</ul>'
            html += '</div>'
        
        html += '</div>'
        return html

    def _generate_comparison_html(
        self,
        items: List[Dict],
        fields: List[str]
    ) -> str:
        """Gera HTML para comparação"""
        html = '<div class="comparison-grid">'
        
        for item in items:
            html += '<div class="comparison-item">'
            html += f'<h4 class="comparison-title">{item.get("name", "Item")}</h4>'
            html += '<div class="comparison-fields">'
            
            for field in fields:
                value = item.get(field, 'N/A')
                html += f'''
                <div class="comparison-field">
                    <span class="field-label">{field}:</span>
                    <span class="field-value">{value}</span>
                </div>
                '''
            
            html += '</div></div>'
        
        html += '</div>'
        return html

    def _get_logo_base64(self) -> str:
        """Converte logo para base64"""
        if self.config.logo_path and Path(self.config.logo_path).exists():
            with open(self.config.logo_path, 'rb') as f:
                return base64.b64encode(f.read()).decode()
        return ""

    def _get_base_template(self) -> str:
        """Template HTML base do relatório"""
        return TEMPLATE_STRING

    def _load_themes(self) -> Dict[str, str]:
        """Carrega temas CSS pré-definidos"""
        return {
            'corporate': self._get_corporate_theme(),
            'modern': self._get_modern_theme(),
            'minimal': self._get_minimal_theme(),
            'executive': self._get_executive_theme(),
            'colorful': self._get_colorful_theme()
        }

    def _get_corporate_theme(self) -> str:
        """Tema corporativo tradicional"""
        return CORPORATE_THEME_CSS

    def _get_modern_theme(self) -> str:
        """Tema moderno com cores vibrantes"""
        base = self._get_corporate_theme()
        return base.replace('#1a4d7a', '#6366f1').replace('#f5f5f5', '#f8fafc')

    def _get_minimal_theme(self) -> str:
        """Tema minimalista"""
        base = self._get_corporate_theme()
        return base.replace('#1a4d7a', '#000000').replace('border-left: 4px solid', 'border-left: 2px solid')

    def _get_executive_theme(self) -> str:
        """Tema executivo premium"""
        base = self._get_corporate_theme()
        return base.replace('#1a4d7a', '#2c3e50')

    def _get_colorful_theme(self) -> str:
        """Tema colorido"""
        base = self._get_corporate_theme()
        return base.replace('#1a4d7a', '#e91e63')


# Funções de conveniência para criação rápida
def create_report(title: str, theme: ReportTheme = ReportTheme.CORPORATE) -> ReportBuilder:
    """Cria um novo relatório com configuração padrão"""
    config = ReportConfig(title=title, theme=theme)
    return ReportBuilder(config)


def quick_report(
    title: str,
    data: pd.DataFrame,
    summary: Optional[str] = None,
    output_path: Optional[str] = None
) -> bytes:
    """Cria um relatório rápido a partir de um DataFrame"""
    builder = create_report(title)
    
    if summary:
        builder.add_section("Resumo", summary)
    
    builder.add_table("Dados", data)
    
    return builder.generate(output_path)


TEMPLATE_STRING = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{{ config.title }}</title>
    </head>
    <body class="theme-{{ theme }}">
        <!-- Capa -->
        <div class="cover-page">
            {% if logo_base64 %}
            <div class="logo">
                <img src="data:image/png;base64,{{ logo_base64 }}" alt="Logo" />
            </div>
            {% endif %}
            
            <h1 class="report-title">{{ config.title }}</h1>
            
            {% if config.subtitle %}
            <h2 class="report-subtitle">{{ config.subtitle }}</h2>
            {% endif %}
            
            <div class="report-meta">
                {% if config.author %}
                <p><strong>Autor:</strong> {{ config.author }}</p>
                {% endif %}
                {% if config.company %}
                <p><strong>Empresa:</strong> {{ config.company }}</p>
                {% endif %}
                <p><strong>Data:</strong> {{ date_formatted }}</p>
            </div>
        </div>
        
        <!-- Índice -->
        {% if config.show_toc and sections|length > 3 %}
        <div class="toc-page">
            <h2>Índice</h2>
            <ul class="toc">
                {% for section in sections %}
                <li><a href="#section-{{ loop.index }}">{{ section.title }}</a></li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}
        
        <!-- Seções -->
        {% for section in sections %}
        <div class="section {% if section.page_break_before %}page-break-before{% endif %} {% if section.page_break_after %}page-break-after{% endif %}" id="section-{{ loop.index }}">
            <h2 class="section-title">{{ section.title }}</h2>
            
            {% if section.content %}
            <div class="section-content">{{ section.content|safe }}</div>
            {% endif %}
            
            {% if section.custom_html %}
            <div class="section-custom">{{ section.custom_html|safe }}</div>
            {% endif %}
            
            {% if section.table_html %}
            {{ section.table_html|safe }}
            {% endif %}
            
            {% if section.chart_html %}
            <div class="chart-container">
                {{ section.chart_html|safe }}
            </div>
            {% endif %}
        </div>
        {% endfor %}
        
        <!-- Rodapé -->
        {% if config.footer_text %}
        <div class="report-footer">
            {{ config.footer_text }}
        </div>
        {% endif %}
    </body>
    </html>
'''

CORPORATE_THEME_CSS = '''
    @page {
        size: A4;
        margin: 2.5cm 2cm;
        @bottom-right {
            content: "Página " counter(page) " de " counter(pages);
            font-size: 9pt;
            color: #666;
        }
    }
    
    body {
        font-family: 'Helvetica', 'Arial', sans-serif;
        color: #333;
        line-height: 1.6;
        font-size: 11pt;
    }
    
    .cover-page {
        page-break-after: always;
        text-align: center;
        padding-top: 30%;
    }
    
    .logo img {
        max-width: 200px;
        margin-bottom: 2cm;
    }
    
    .report-title {
        font-size: 32pt;
        color: #1a4d7a;
        margin-bottom: 0.5cm;
        font-weight: bold;
    }
    
    .report-subtitle {
        font-size: 18pt;
        color: #666;
        margin-bottom: 2cm;
        font-weight: normal;
    }
    
    .report-meta {
        font-size: 12pt;
        color: #666;
    }
    
    .toc-page {
        page-break-after: always;
    }
    
    .toc {
        list-style: none;
        padding: 0;
    }
    
    .toc li {
        padding: 0.5cm 0;
        border-bottom: 1px solid #eee;
    }
    
    .section-title {
        color: #1a4d7a;
        font-size: 18pt;
        margin-top: 1cm;
        margin-bottom: 0.5cm;
        border-bottom: 2px solid #1a4d7a;
        padding-bottom: 0.3cm;
    }
    
    .section-content {
        margin-bottom: 1cm;
        text-align: justify;
    }
    
    .data-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1cm 0;
        font-size: 10pt;
    }
    
    .data-table th {
        background-color: #1a4d7a;
        color: white;
        padding: 0.3cm;
        text-align: left;
        font-weight: bold;
    }
    
    .data-table td {
        padding: 0.3cm;
        border-bottom: 1px solid #ddd;
    }
    
    .data-table tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    
    .kpi-grid {
        display: grid;
        gap: 0.5cm;
        margin: 1cm 0;
    }
    
    .kpi-grid-2 { grid-template-columns: repeat(2, 1fr); }
    .kpi-grid-3 { grid-template-columns: repeat(3, 1fr); }
    .kpi-grid-4 { grid-template-columns: repeat(4, 1fr); }
    
    .kpi-card {
        background: #f5f5f5;
        padding: 0.5cm;
        border-radius: 5px;
        border-left: 4px solid #1a4d7a;
    }
    
    .kpi-label {
        font-size: 9pt;
        color: #666;
        margin-bottom: 0.2cm;
    }
    
    .kpi-value {
        font-size: 24pt;
        font-weight: bold;
        color: #1a4d7a;
        margin-bottom: 0.2cm;
    }
    
    .kpi-trend {
        font-size: 10pt;
    }
    
    .trend-up { color: #27ae60; }
    .trend-down { color: #e74c3c; }
    .trend-neutral { color: #666; }
    
    .chart-image {
        max-width: 100%;
        height: auto;
        margin: 1cm 0;
    }
    
    .page-break-before {
        page-break-before: always;
    }
    
    .page-break-after {
        page-break-after: always;
    }
    
    .executive-summary {
        background: #f0f8ff;
        padding: 0.7cm;
        border-radius: 5px;
        margin: 1cm 0;
    }
    
    .summary-metrics {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.5cm;
        margin-bottom: 0.5cm;
    }
    
    .summary-metric {
        background: white;
        padding: 0.3cm;
        border-radius: 3px;
    }
    
    .metric-value {
        font-weight: bold;
        color: #1a4d7a;
    }
    
    .highlights-list {
        margin-top: 0.3cm;
    }
    
    .highlights-list li {
        margin-bottom: 0.2cm;
    }
    
    .comparison-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 0.5cm;
        margin: 1cm 0;
    }
    
    .comparison-item {
        background: #f9f9f9;
        padding: 0.5cm;
        border-radius: 5px;
    }
    
    .comparison-title {
        color: #1a4d7a;
        font-size: 14pt;
        margin-bottom: 0.3cm;
    }
    
    .comparison-field {
        margin-bottom: 0.2cm;
        font-size: 10pt;
    }
    
    .field-label {
        color: #666;
    }
    
    .field-value {
        font-weight: bold;
        color: #333;
    }
'''
