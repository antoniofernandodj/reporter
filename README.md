# ReportMaster 📊

## Framework Inteligente para Geração de Relatórios Profissionais

**A solução que seu chefe estava esperando!** 🎯

ReportMaster é um framework Python que abstrai completamente a complexidade de gerar relatórios em PDF, oferecendo uma API declarativa e super intuitiva.

### Por que ReportMaster?

✅ **API Super Simples**: Crie relatórios completos em 3 linhas de código  
✅ **Altamente Abstrato**: Não precisa conhecer HTML, CSS ou WeasyPrint  
✅ **Temas Prontos**: 5 temas profissionais pré-configurados  
✅ **Componentes Inteligentes**: KPIs, gráficos, tabelas formatadas automaticamente  
✅ **Configuração Declarativa**: Usa dataclasses e builders pattern  
✅ **Poderoso**: Usa Jinja2 + WeasyPrint por baixo (quando você precisar customizar)

---

## 🚀 Instalação

```bash
pip install pandas jinja2 weasyprint matplotlib --break-system-packages
```

**Nota**: WeasyPrint requer algumas dependências do sistema:

```bash
# Ubuntu/Debian
sudo apt-get install python3-dev python3-pip python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

# macOS
brew install cairo pango gdk-pixbuf libffi
```

---

## ⚡ Quick Start

### Relatório Mais Simples do Mundo (3 linhas!)

```python
from report_framework import quick_report
import pandas as pd

data = pd.DataFrame({
    'Produto': ['A', 'B', 'C'],
    'Vendas': [1000, 1500, 1200]
})

quick_report(
    title="Relatório de Vendas",
    data=data,
    output_path="meu_relatorio.pdf"
)
```

**Pronto!** Você tem um PDF profissional com capa, índice e tabela formatada.

---

## 📚 Exemplos de Uso

### 1. Dashboard com KPIs

```python
from report_framework import create_report, ReportTheme

report = create_report("Dashboard Q1 2025", theme=ReportTheme.EXECUTIVE)

report.add_kpi_grid(
    title="Indicadores Principais",
    kpis=[
        {'label': 'Receita', 'value': 'R$ 2.5M', 'trend': 'up', 'change': '+15%'},
        {'label': 'Clientes', 'value': '342', 'trend': 'up', 'change': '+22%'},
        {'label': 'Conversão', 'value': '3.2%', 'trend': 'down', 'change': '-0.5%'},
    ],
    columns=3
)

report.generate("dashboard.pdf")
```

### 2. Relatório com Múltiplas Seções

```python
report = create_report("Análise Trimestral")

# Resumo executivo
report.add_executive_summary(
    highlights=[
        "Crescimento de 15% na receita",
        "Expansão da base de clientes",
        "Lançamento de 3 novos produtos"
    ],
    metrics={'MRR': 'R$ 833K', 'CAC': 'R$ 450'}
)

# Dados detalhados
report.add_table("Vendas por Produto", vendas_df)

# Gráfico
report.add_chart(
    title="Evolução Mensal",
    chart_type=ChartType.LINE,
    data={'Jan': [800], 'Fev': [850], 'Mar': [900]}
)

report.generate("trimestral.pdf")
```

### 3. Análise Comparativa

```python
report.add_comparison(
    title="Comparação de Fornecedores",
    items=[
        {'name': 'Fornecedor A', 'Preço': 'R$ 45K', 'Qualidade': '⭐⭐⭐⭐⭐'},
        {'name': 'Fornecedor B', 'Preço': 'R$ 38K', 'Qualidade': '⭐⭐⭐⭐'},
    ],
    comparison_fields=['Preço', 'Qualidade', 'Prazo']
)
```

---

## 🎨 Temas Disponíveis

```python
from report_framework import ReportTheme

# Escolha entre:
ReportTheme.CORPORATE    # Tradicional, azul corporativo
ReportTheme.MODERN       # Moderno, roxo vibrante
ReportTheme.MINIMAL      # Minimalista, preto e branco
ReportTheme.EXECUTIVE    # Premium, cinza escuro
ReportTheme.COLORFUL     # Colorido, rosa chamativo
```

---

## 🏗️ Componentes Disponíveis

### Seções de Texto
```python
report.add_section(
    title="Introdução",
    content="Texto do relatório aqui...",
    page_break_before=True  # Inicia nova página
)
```

### Tabelas Formatadas
```python
report.add_table(
    title="Dados de Vendas",
    data=df  # DataFrame do pandas
)
```

### Gráficos
```python
from report_framework import ChartType

report.add_chart(
    title="Vendas Mensais",
    chart_type=ChartType.LINE,  # BAR, PIE, AREA, SCATTER
    data={'Serie1': [10, 20, 30], 'Serie2': [15, 25, 35]},
    labels=['Jan', 'Fev', 'Mar']
)
```

### Grid de KPIs
```python
report.add_kpi_grid(
    title="Indicadores",
    kpis=[
        {
            'label': 'Receita Total',
            'value': 'R$ 2.5M',
            'trend': 'up',      # up, down, neutral
            'change': '+15%'
        }
    ],
    columns=4  # 2, 3 ou 4 colunas
)
```

### Resumo Executivo
```python
report.add_executive_summary(
    highlights=["Ponto 1", "Ponto 2"],
    metrics={'KPI': 'Valor'}
)
```

### Comparação
```python
report.add_comparison(
    title="Análise Comparativa",
    items=[{'name': 'Item 1', 'campo': 'valor'}],
    comparison_fields=['campo1', 'campo2']
)
```

---

## ⚙️ Configuração Avançada

```python
from report_framework import ReportConfig, ReportBuilder

config = ReportConfig(
    title="Título do Relatório",
    subtitle="Subtítulo opcional",
    author="Seu Nome",
    company="Sua Empresa",
    logo_path="caminho/para/logo.png",
    theme=ReportTheme.CORPORATE,
    date=datetime.now(),
    show_page_numbers=True,
    show_toc=True,  # Índice automático
    header_text="Confidencial",
    footer_text="© 2025 Empresa",
    custom_css="/* CSS personalizado */"
)

report = ReportBuilder(config)
```

---

## 🔧 Integração em Pipelines

```python
def gerar_relatorio_automatico(mes, ano):
    """Função para chamada automatizada"""
    
    # Busca dados do banco/API
    dados = buscar_dados_vendas(mes, ano)
    
    # Cria relatório
    report = create_report(f"Vendas {mes}/{ano}")
    report.add_kpi_grid(title="KPIs", kpis=calcular_kpis(dados))
    report.add_table("Detalhes", dados)
    
    # Salva com nome padrão
    filename = f"vendas_{ano}_{mes:02d}.pdf"
    report.generate(filename)
    
    # Envia por email, upload S3, etc.
    enviar_email(filename)
    
    return filename
```

---

## 🌍 Multi-idioma

```python
def criar_relatorio(idioma='pt'):
    traducoes = {
        'pt': {'titulo': 'Relatório'},
        'en': {'titulo': 'Report'},
        'es': {'titulo': 'Informe'}
    }
    
    t = traducoes[idioma]
    report = create_report(t['titulo'])
    # ... adiciona conteúdo
    return report.generate(f"relatorio_{idioma}.pdf")
```

---

## 📊 Formatação Automática

ReportMaster formata automaticamente:

- ✅ Números com separadores de milhares: `1,000,000`
- ✅ Valores monetários: `R$ 1.234,56`
- ✅ Percentuais: `15.5%`
- ✅ Cores alternadas em tabelas
- ✅ Headers com destaque
- ✅ Quebras de página inteligentes
- ✅ Numeração de páginas
- ✅ Índice automático

---

## 🎯 Casos de Uso

### Relatórios Corporativos
- ✅ Dashboards executivos
- ✅ Relatórios mensais/trimestrais
- ✅ Análises de performance
- ✅ Relatórios financeiros

### Análises Técnicas
- ✅ Relatórios de ML/Data Science
- ✅ Análises estatísticas
- ✅ Performance de sistemas
- ✅ Benchmarks

### Documentação
- ✅ Propostas comerciais
- ✅ Análises comparativas
- ✅ Estudos de viabilidade
- ✅ Relatórios de sustentabilidade

---

## 🆚 Comparação com Alternativas

| Feature | ReportMaster | Jinja+HTML | ReportLab | Pandas.to_pdf |
|---------|-------------|-----------|-----------|---------------|
| **Facilidade** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Flexibilidade** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **Temas Prontos** | ✅ 5 temas | ❌ | ❌ | ❌ |
| **KPIs Visuais** | ✅ | ❌ | ⚠️ Manual | ❌ |
| **Gráficos** | ✅ Integrado | ⚠️ Manual | ✅ | ❌ |
| **Curva Aprendizado** | 5 min | 2-3 horas | 1-2 horas | 30 min |

---

## 🚀 Próximos Passos

1. **Clone os exemplos**: `python exemplos_uso.py`
2. **Teste o quick_report**: Crie seu primeiro relatório em 3 linhas
3. **Explore os temas**: Veja qual combina com sua empresa
4. **Customize**: Adicione seu logo e cores corporativas
5. **Automatize**: Integre em seus pipelines de dados

---

## 💡 Dicas Pro

### Dica 1: Use DataFrames do Pandas
```python
# Ao invés de listas de dicionários, use DataFrames
df = pd.read_sql(query, connection)
report.add_table("Dados", df)  # Formatação automática!
```

### Dica 2: Quebre Páginas Estrategicamente
```python
report.add_section("Seção Importante", page_break_before=True)
# Garante que começa em página nova
```

### Dica 3: Combine Componentes
```python
# KPIs + Gráfico + Tabela = Dashboard completo
report.add_kpi_grid(...)
report.add_chart(...)
report.add_table(...)
```

### Dica 4: CSS Customizado para Marca
```python
config = ReportConfig(
    ...,
    custom_css="""
    .section-title { color: #FF6B35; }  /* Cor da marca */
    .kpi-value { font-family: 'Montserrat'; }
    """
)
```

---

## 🐛 Troubleshooting

### WeasyPrint não instala?
```bash
# Instale as dependências do sistema primeiro
sudo apt-get install libcairo2-dev libpango1.0-dev
```

### Fontes não aparecem?
```python
# Adicione fontes via CSS customizado
config.custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Roboto');
body { font-family: 'Roboto', sans-serif; }
"""
```

### PDF muito grande?
```python
# Reduza DPI dos gráficos (matplotlib)
plt.savefig(buf, format='png', dpi=100)  # padrão: 150
```

---

## 📝 Licença

MIT License - Use livremente em projetos comerciais!

---

## 🤝 Contribuindo

Quer adicionar novos componentes ou temas? PRs são bem-vindos!

---

## 💬 Suporte

Encontrou um bug ou tem sugestões? Abra uma issue no GitHub!

---

**Feito com ❤️ para tornar geração de relatórios algo prazeroso, não doloroso.**
