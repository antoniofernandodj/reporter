# ReportMaster - Extensões e Roadmap

## 🔌 Como Estender o Framework

O ReportMaster foi projetado para ser extensível. Aqui estão algumas formas de expandir suas capacidades:

---

## 1. Criar Novos Temas

```python
# Em report_framework.py, adicione ao método _load_themes():

def _get_seu_tema_customizado(self) -> str:
    """Seu tema corporativo"""
    return '''
    @page {
        size: A4;
        margin: 2cm;
        @bottom-right {
            content: counter(page);
        }
    }
    
    body {
        font-family: 'Sua Fonte', sans-serif;
        color: #sua-cor;
    }
    
    .section-title {
        color: #sua-cor-principal;
        border-bottom: 3px solid #sua-cor-principal;
    }
    
    .kpi-card {
        background: linear-gradient(135deg, #cor1, #cor2);
        color: white;
    }
    
    /* ... seu CSS customizado ... */
    '''
```

**Uso:**
```python
# Adicione ao enum ReportTheme
class ReportTheme(Enum):
    # ... existentes ...
    MEU_TEMA = "meu_tema"

# Use normalmente
report = create_report("Título", theme=ReportTheme.MEU_TEMA)
```

---

## 2. Criar Componentes Customizados

### Exemplo: Timeline

```python
# Adicione à classe ReportBuilder:

def add_timeline(
    self,
    title: str,
    events: List[Dict[str, Any]]
) -> 'ReportBuilder':
    """Adiciona uma linha do tempo visual"""
    html = self._generate_timeline_html(events)
    section = Section(title=title, custom_html=html)
    self.sections.append(section)
    return self

def _generate_timeline_html(self, events: List[Dict]) -> str:
    """Gera HTML para timeline"""
    html = '<div class="timeline">'
    
    for event in events:
        html += f'''
        <div class="timeline-item">
            <div class="timeline-date">{event['date']}</div>
            <div class="timeline-content">
                <h4>{event['title']}</h4>
                <p>{event['description']}</p>
            </div>
        </div>
        '''
    
    html += '</div>'
    return html
```

**CSS no tema:**
```css
.timeline {
    position: relative;
    padding-left: 30px;
}

.timeline::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 2px;
    background: #ccc;
}

.timeline-item {
    margin-bottom: 20px;
    position: relative;
}

.timeline-date {
    font-weight: bold;
    color: #666;
    margin-bottom: 5px;
}
```

**Uso:**
```python
report.add_timeline(
    title="Marcos do Projeto",
    events=[
        {'date': 'Jan 2025', 'title': 'Início', 'description': 'Kickoff do projeto'},
        {'date': 'Mar 2025', 'title': 'MVP', 'description': 'Primeira versão lançada'},
    ]
)
```

---

## 3. Integrações com Bibliotecas

### Integração com Plotly (gráficos interativos -> estáticos)

```python
def add_plotly_chart(
    self,
    title: str,
    fig: 'plotly.graph_objs.Figure'
) -> 'ReportBuilder':
    """Adiciona gráfico Plotly convertido para imagem"""
    import plotly.io as pio
    import base64
    from io import BytesIO
    
    # Converte Plotly para imagem
    img_bytes = pio.to_image(fig, format='png', width=1000, height=600)
    img_base64 = base64.b64encode(img_bytes).decode()
    
    html = f'<img src="data:image/png;base64,{img_base64}" class="chart-image" />'
    
    section = Section(title=title, custom_html=html)
    self.sections.append(section)
    return self
```

### Integração com Seaborn

```python
def add_seaborn_chart(
    self,
    title: str,
    plot_function: Callable,
    data: pd.DataFrame,
    **kwargs
) -> 'ReportBuilder':
    """Adiciona gráfico Seaborn"""
    import seaborn as sns
    import matplotlib.pyplot as plt
    import io
    import base64
    
    fig, ax = plt.subplots(figsize=(10, 6))
    plot_function(data=data, ax=ax, **kwargs)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode()
    
    html = f'<img src="data:image/png;base64,{img_base64}" class="chart-image" />'
    section = Section(title=title, custom_html=html)
    self.sections.append(section)
    return self
```

**Uso:**
```python
report.add_seaborn_chart(
    title="Correlação entre Variáveis",
    plot_function=sns.heatmap,
    data=correlation_matrix,
    annot=True,
    cmap='coolwarm'
)
```

---

## 4. Componentes Avançados

### Mapa de Calor

```python
def add_heatmap(
    self,
    title: str,
    data: pd.DataFrame,
    cmap: str = 'RdYlGn'
) -> 'ReportBuilder':
    """Adiciona mapa de calor"""
    import seaborn as sns
    # ... implementação similar ao seaborn_chart
```

### Gauge/Medidor

```python
def add_gauge(
    self,
    title: str,
    value: float,
    max_value: float,
    thresholds: Dict[str, float]
) -> 'ReportBuilder':
    """Adiciona medidor tipo gauge"""
    html = self._generate_gauge_html(value, max_value, thresholds)
    section = Section(title=title, custom_html=html)
    self.sections.append(section)
    return self
```

### Scorecard

```python
def add_scorecard(
    self,
    title: str,
    metrics: List[Dict[str, Any]],
    weights: Optional[Dict[str, float]] = None
) -> 'ReportBuilder':
    """Adiciona balanced scorecard"""
    html = self._generate_scorecard_html(metrics, weights)
    section = Section(title=title, custom_html=html)
    self.sections.append(section)
    return self
```

---

## 5. Exportar para Outros Formatos

### Exportar HTML

```python
def generate_html(self, output_path: Optional[str] = None) -> str:
    """Gera versão HTML do relatório (sem converter para PDF)"""
    html_content = self._build_html()
    css_content = self._build_css()
    
    full_html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <style>{css_content}</style>
    </head>
    {html_content}
    </html>
    '''
    
    if output_path:
        Path(output_path).write_text(full_html, encoding='utf-8')
    
    return full_html
```

### Exportar para DOCX

```python
def generate_docx(self, output_path: str) -> bytes:
    """Gera versão DOCX do relatório"""
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor
    
    doc = Document()
    
    # Título
    title = doc.add_heading(self.config.title, 0)
    title.alignment = 1  # Centro
    
    # Seções
    for section in self.sections:
        doc.add_heading(section.title, 1)
        
        if section.content:
            doc.add_paragraph(section.content)
        
        if section.data_table is not None:
            # Adiciona tabela
            table = doc.add_table(
                rows=len(section.data_table) + 1,
                cols=len(section.data_table.columns)
            )
            # ... preenche tabela
    
    doc.save(output_path)
    return Path(output_path).read_bytes()
```

---

## 🚀 Roadmap de Features Futuras

### Versão 2.0 (Curto Prazo)

- [ ] **Templates Editáveis**: Editor visual de temas
- [ ] **Mais Componentes**:
  - [ ] Waterfall charts
  - [ ] Funnel charts
  - [ ] Sankey diagrams
  - [ ] Mapas geográficos
  - [ ] Word clouds
- [ ] **Suporte a Markdown**: Seções em Markdown puro
- [ ] **Temas Dinâmicos**: Mudar cores via configuração
- [ ] **Validação de Dados**: Alerts para dados inválidos

### Versão 3.0 (Médio Prazo)

- [ ] **Relatórios Interativos**: Export para HTML com JS
- [ ] **Dashboard Web**: Visualizar no navegador
- [ ] **Agendamento**: Geração automática programada
- [ ] **Templates Marketplace**: Compartilhar temas
- [ ] **Multi-formato**: PPTX, XLSX, etc
- [ ] **Internacionalização**: Suporte completo i18n

### Versão 4.0 (Longo Prazo)

- [ ] **IA Integrada**: Sugestões automáticas de visualizações
- [ ] **Auto-insights**: Análise automática dos dados
- [ ] **Collaborative**: Múltiplos autores
- [ ] **Cloud Native**: API REST para geração
- [ ] **Real-time**: Atualização em tempo real

---

## 💡 Ideias da Comunidade

### Componentes Solicitados

1. **SWOT Matrix**
```python
report.add_swot_analysis(
    strengths=['...'],
    weaknesses=['...'],
    opportunities=['...'],
    threats=['...']
)
```

2. **Gantt Chart**
```python
report.add_gantt_chart(
    title="Cronograma do Projeto",
    tasks=[
        {'name': 'Fase 1', 'start': '2025-01', 'end': '2025-03'},
        {'name': 'Fase 2', 'start': '2025-04', 'end': '2025-06'},
    ]
)
```

3. **Financial Statements**
```python
report.add_financial_statement(
    statement_type='balance_sheet',  # ou 'income_statement', 'cashflow'
    data=df
)
```

4. **Risk Matrix**
```python
report.add_risk_matrix(
    risks=[
        {'name': 'Risco A', 'probability': 0.7, 'impact': 0.8},
        {'name': 'Risco B', 'probability': 0.3, 'impact': 0.9},
    ]
)
```

---

## 🔧 Configurações Avançadas

### Custom Fonts

```python
config = ReportConfig(
    ...,
    custom_css="""
    @font-face {
        font-family: 'MinhaFonte';
        src: url('fonts/minha-fonte.ttf');
    }
    body {
        font-family: 'MinhaFonte', sans-serif;
    }
    """
)
```

### Page Breaks Inteligentes

```python
# Evita quebras indesejadas
config.custom_css = """
.section {
    page-break-inside: avoid;
}
.kpi-grid {
    page-break-inside: avoid;
}
"""
```

### Watermarks

```python
config.custom_css = """
@page {
    background: 
        url(data:image/svg+xml;base64,...) 
        center center no-repeat;
}
"""
```

---

## 📚 Plugins de Terceiros

### Plugin de BI Tools

```python
# Integração com Tableau, Power BI, etc
from report_framework.plugins import TableauPlugin

plugin = TableauPlugin(workbook='meu_dashboard.twb')
report.add_tableau_view(
    title="Dashboard Tableau",
    view_name='Visão Geral'
)
```

### Plugin de Banco de Dados

```python
from report_framework.plugins import DatabasePlugin

db = DatabasePlugin(connection_string='...')
report.add_query_result(
    title="Vendas do Trimestre",
    query="SELECT * FROM vendas WHERE trimestre = 'Q1'"
)
```

---

## 🎓 Tutoriais Avançados

### 1. Relatório Multi-Regional

```python
def generate_regional_report(regions: List[str]):
    """Gera relatório para cada região"""
    for region in regions:
        data = fetch_data_for_region(region)
        
        report = create_report(
            title=f"Relatório {region}",
            theme=get_regional_theme(region)
        )
        
        report.add_kpi_grid(...)
        report.add_comparison(
            title="vs Outras Regiões",
            items=compare_with_other_regions(region, data)
        )
        
        report.generate(f"relatorio_{region}.pdf")
```

### 2. Relatório Condicional

```python
def generate_smart_report(data: pd.DataFrame):
    """Gera relatório adaptativo baseado nos dados"""
    report = create_report("Análise Inteligente")
    
    # Análise automática
    if data['vendas'].mean() > 1000000:
        report.add_section(
            "⚠️ Alerta",
            "Vendas excepcionalmente altas detectadas"
        )
    
    # Seção condicional
    if len(data) > 100:
        report.add_chart(
            "Tendência Histórica",
            ChartType.LINE,
            data
        )
    else:
        report.add_table("Dados Completos", data)
    
    report.generate("relatorio_adaptativo.pdf")
```

---

## 🤝 Como Contribuir

Quer adicionar uma feature? Siga estes passos:

1. **Fork** o repositório
2. **Crie** uma branch: `git checkout -b feature/minha-feature`
3. **Implemente** sua feature seguindo o padrão:
   - Adicione métodos à classe `ReportBuilder`
   - Implemente geração de HTML privado `_generate_*_html()`
   - Adicione CSS ao tema apropriado
   - Documente no README
4. **Teste** com exemplos práticos
5. **Commit**: `git commit -m 'Add: minha feature incrível'`
6. **Push**: `git push origin feature/minha-feature`
7. **Pull Request** com descrição detalhada

---

## 📞 Suporte e Comunidade

- 💬 **Discord**: [link]
- 📧 **Email**: support@reportmaster.dev
- 🐛 **Issues**: GitHub Issues
- 📖 **Docs**: docs.reportmaster.dev
- 🎥 **Tutoriais**: YouTube Channel

---

**O futuro do ReportMaster está nas mãos da comunidade!** 🚀
