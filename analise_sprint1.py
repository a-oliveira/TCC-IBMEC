import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# 1. Carregar base com colunas de tempo
ARQUIVOS_CANDIDATOS = ["PLANILHA-02.csv", "PLANILHA-01.csv"]
COLUNA_ESTIMADO = "Tempo Estimado (Horas)"
COLUNA_REALIZADO = "Tempo Realizado (Horas)"

df = None
arquivo_usado = None

for nome_arquivo in ARQUIVOS_CANDIDATOS:
    caminho = Path(nome_arquivo)
    if not caminho.exists():
        continue

    # decimal="," converte corretamente valores como "3,5" para 3.5
    candidato = pd.read_csv(caminho, sep=";", decimal=",")
    if {COLUNA_ESTIMADO, COLUNA_REALIZADO}.issubset(candidato.columns):
        df = candidato
        arquivo_usado = nome_arquivo
        break

if df is None:
    raise ValueError(
        "Nenhum arquivo CSV válido encontrado com as colunas "
        f"'{COLUNA_ESTIMADO}' e '{COLUNA_REALIZADO}'. "
        "Verifique os arquivos em ARQUIVOS_CANDIDATOS."
    )

df[COLUNA_ESTIMADO] = pd.to_numeric(df[COLUNA_ESTIMADO], errors="coerce")
df[COLUNA_REALIZADO] = pd.to_numeric(df[COLUNA_REALIZADO], errors="coerce")
df = df.dropna(subset=[COLUNA_ESTIMADO, COLUNA_REALIZADO])

print(f"Arquivo utilizado: {arquivo_usado}")

print("--- VISÃO GERAL DOS DADOS ---")
print(df.info())
print("\n")

# 2. Estatística descritiva simples
colunas_analise = [COLUNA_ESTIMADO, COLUNA_REALIZADO]

print("--- ESTATÍSTICA DESCRITIVA ---")
descritiva = df[colunas_analise].describe()
print(descritiva)
# Salva a tabela descritiva para você colar no TCC
descritiva.to_csv("estatistica_descritiva_sprint1.csv", sep=";", decimal=",")

# 3. Gráfico de Dispersão (Correlação Estimativa x Realidade)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x=COLUNA_ESTIMADO, y=COLUNA_REALIZADO, alpha=0.6, color="#1f77b4")

# Linha de tendência ideal (Onde Estimado = Realizado)
max_val = max(df[COLUNA_ESTIMADO].max(), df[COLUNA_REALIZADO].max())
plt.plot([0, max_val], [0, max_val], color="red", linestyle="--", label="Tendência Ideal (Acerto de 100%)")

plt.title('Análise de Previsibilidade: Tempo Estimado vs. Realizado', fontsize=14)
plt.xlabel('Tempo Estimado (horas)', fontsize=12)
plt.ylabel('Tempo Realizado (horas)', fontsize=12)
plt.legend()
plt.grid(True, linestyle=':', alpha=0.7)

# Salva o gráfico como imagem para colocar no relatório
plt.tight_layout()
plt.savefig('grafico_dispersao_evidencia.png')
plt.show()

print("\nAnálise concluída! O gráfico e a tabela foram salvos na sua pasta.")