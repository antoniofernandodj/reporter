"""
Exemplos de uso do ReportMaster Framework
Demonstra a facilidade e praticidade da API
"""


from examples.exemplo_analise_tecnica import exemplo_analise_tecnica
from examples.exemplo_basico import exemplo_basico
from examples.exemplo_com_kpis import exemplo_com_kpis
from examples.exemplo_comparativo import exemplo_comparativo
from examples.exemplo_completo import exemplo_completo
from examples.exemplo_multi_idioma import exemplo_multi_idioma
from examples.exemplo_pipeline import exemplo_pipeline


def main():
    print("🚀 ReportMaster Framework - Exemplos de Uso\n")
    
    print("1. Relatório básico (3 linhas)...")
    exemplo_basico()
    
    print("\n2. Dashboard executivo com KPIs...")
    exemplo_com_kpis()
    
    print("\n3. Análise comparativa...")
    exemplo_comparativo()
    
    print("\n4. Relatório completo customizado...")
    exemplo_completo()
    
    print("\n5. Análise técnica...")
    exemplo_analise_tecnica()
    
    print("\n6. Pipeline automatizado...")
    exemplo_pipeline()
    
    print("\n7. Multi-idioma...")
    exemplo_multi_idioma()
    
    print("\n✨ Todos os exemplos executados com sucesso!")
