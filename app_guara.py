import streamlit as st
import pandas as pd
import requests
import json
import os
import time
from datetime import datetime

st.set_page_config(page_title="G.U.A.R.A. - Gestão Acadêmica", page_icon="🐺", layout="wide")
ARQUIVO_DADOS = "central_producoes_historicas.xlsx"

# ==========================================
# MÓDULO 1: GERENCIADOR EXPANDIDO
# ==========================================
def inicializar_sistema():
    if not os.path.exists(ARQUIVO_DADOS):
        df = pd.DataFrame(columns=[
            "Data_Registro", "Tipo_Atividade", "Autores", "Titulo", 
            "Revista_Veiculo", "Instituicao_Vinculo", "Edicao_Volume", "Paginas", 
            "Ano_Publicacao", "Status_Lattes", "Status_ORCID", "Status_LinkedIn"
        ])
        df.to_excel(ARQUIVO_DADOS, index=False)
        return df
    return pd.read_excel(ARQUIVO_DADOS)

def checar_duplicata(df, titulo, ano):
    duplicados = df[(df['Titulo'].str.lower().str.strip() == titulo.lower().strip()) & 
                    (df['Ano_Publicacao'] == int(ano))]
    return not duplicados.empty

def registrar_atividade(tipo, autores, titulo, revista, instituicao, edicao, paginas, ano):
    df = inicializar_sistema()
    
    if checar_duplicata(df, titulo, ano):
        return False, "Produção já existe na base de dados!"
    
    nova_linha = pd.DataFrame([{
        "Data_Registro": datetime.now().strftime("%Y-%m-%d"),
        "Tipo_Atividade": tipo,
        "Autores": autores,
        "Titulo": titulo.strip(),
        "Revista_Veiculo": revista,
        "Instituicao_Vinculo": instituicao,
        "Edicao_Volume": edicao,
        "Paginas": paginas,
        "Ano_Publicacao": int(ano),
        "Status_Lattes": "Pendente",
        "Status_ORCID": "Pendente",
        "Status_LinkedIn": "Pendente"
    }])
    
    df = pd.concat([df, nova_linha], ignore_index=True)
    df.to_excel(ARQUIVO_DADOS, index=False)
    return True, "Registrado com sucesso!"

# ==========================================
# MÓDULO 2: DOI AVANÇADO 
# ==========================================
def buscar_dados_doi(doi):
    doi_limpo = doi.replace("https://doi.org/", "").replace("http://doi.org/", "").replace("doi.org/", "").strip()
    try:
        url = f"https://api.crossref.org/works/{doi_limpo}"
        resp = requests.get(url, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()['message']
            
            # 1. Título
            titulos = data.get('title', [])
            titulo = titulos[0] if titulos else "Título não identificado"
            
            # 2. Autores e Instituição
            lista_autores = []
            lista_instituicoes = []
            
            if 'author' in data:
                for autor in data['author']:
                    nome = autor.get('given', '')
                    sobrenome = autor.get('family', '')
                    if nome or sobrenome:
                        lista_autores.append(f"{nome} {sobrenome}".strip())
                    
                    # Puxa filiação se a revista tiver enviado
                    if 'affiliation' in autor and len(autor['affiliation']) > 0:
                        for aff in autor['affiliation']:
                            inst_nome = aff.get('name', '')
                            if inst_nome and inst_nome not in lista_instituicoes:
                                lista_instituicoes.append(inst_nome)
            
            autores_str = ", ".join(lista_autores) if lista_autores else ""
            instituicao_str = ", ".join(lista_instituicoes) if lista_instituicoes else ""
            
            # 3. Revista / Veículo
            locais = data.get('container-title', [])
            revista = locais[0] if locais else data.get('publisher', '')
            
            # 4. Volume, Edição e Páginas
            volume = data.get('volume', '')
            issue = data.get('issue', '')
            edicao = f"Vol. {volume}" if volume else ""
            if issue:
                edicao += f", N. {issue}" if edicao else f"N. {issue}"
                
            paginas = data.get('page', '')
            
            # 5. Ano
            ano = datetime.now().year 
            if 'published-print' in data and 'date-parts' in data['published-print']:
                ano = data['published-print']['date-parts'][0][0]
            elif 'published-online' in data and 'date-parts' in data['published-online']:
                ano = data['published-online']['date-parts'][0][0]
            
            return {
                "autores": autores_str,
                "titulo": titulo,
                "revista": revista,
                "instituicao": instituicao_str,
                "edicao": edicao.strip(", "),
                "paginas": paginas,
                "ano": ano
            }
    except Exception as e:
        pass
    return None

# (O módulo ORCID e Lattes continuam iguais, apenas omitidos aqui por brevidade caso não tenham mudado, mas vamos mantê-los funcionais)
def enviar_para_orcid(orcid_id, access_token, titulo, ano, tipo):
    url = f"https://pub.orcid.org/v3.0/{orcid_id}/work"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json", "Accept": "application/json"}
    orcid_type = "JOURNAL_ARTICLE" if tipo == "Artigo" else "OTHER"
    payload = {"title": {"title": {"value": titulo}}, "type": orcid_type, "publication-date": {"year": {"value": str(ano)}}}
    try:
        resposta = requests.post(url, headers=headers, data=json.dumps(payload))
        return resposta.status_code == 201 
    except:
        return False

# ==========================================
# INTERFACE GRÁFICA (STREAMLIT)
# ==========================================
st.title("🐺 Projeto G.U.A.R.A.")
st.subheader("Gerenciador Unificado de Atualização de Registros Acadêmicos")

df_atual = inicializar_sistema()
aba1, aba2, aba3 = st.tabs(["📝 Registrar Produção", "📊 Minha Base de Dados", "🚀 Sincronizar ORCID"])

with aba1:
    col_doi, col_manual = st.columns(2)
    
    with col_doi:
        st.markdown("### Busca Automática por DOI")
        with st.form("form_doi"):
            doi_input = st.text_input("Cole o DOI do artigo")
            if st.form_submit_button("Buscar e Salvar"):
                st.info("Vasculhando base internacional...")
                dados = buscar_dados_doi(doi_input)
                if dados:
                    # Avisa se a instituição não veio na API
                    if not dados['instituicao']:
                        st.warning("⚠️ O registro deste artigo não informou sua instituição na base mundial. Edite depois se necessário.")
                        
                    sucesso, msg = registrar_atividade(
                        "Artigo", dados['autores'], dados['titulo'], dados['revista'], 
                        dados['instituicao'], dados['edicao'], dados['paginas'], dados['ano']
                    )
                    if sucesso:
                        st.success(f"Salvo: {dados['titulo']} ({dados['ano']})")
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.error("Falha ao buscar dados deste DOI.")

    with col_manual:
        st.markdown("### Registro Manual")
        with st.form("form_manual", clear_on_submit=True):
            tipo = st.selectbox("Tipo", ["Artigo", "Capítulo", "Livro", "Projeto"])
            autores = st.text_input("Autores (separados por vírgula)")
            titulo = st.text_input("Título da Produção")
            revista = st.text_input("Revista / Editora")
            instituicao = st.text_input("Sua Instituição de Vínculo")
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                edicao = st.text_input("Edição/Vol")
            with col_b:
                paginas = st.text_input("Páginas")
            with col_c:
                ano = st.number_input("Ano", min_value=1990, max_value=2050, value=datetime.now().year)
            
            if st.form_submit_button("Salvar Manualmente"):
                if titulo:
                    sucesso, msg = registrar_atividade(tipo, autores, titulo, revista, instituicao, edicao, paginas, ano)
                    if sucesso:
                        st.success(msg)
                        st.rerun()
                else:
                    st.error("O Título é obrigatório.")

with aba2:
    st.markdown("### Suas Produções Cadastradas")
    st.info("💡 **Dica:** Dê dois cliques em qualquer célula para editar. Você pode usar CTRL+C / CTRL+V e arrastar o canto das células para baixo para repetir informações.")
    
    # ==========================================
    # CORREÇÃO: Forçar colunas a serem texto 
    # (Desbloqueia a digitação de letras no Streamlit)
    # ==========================================
    colunas_texto = [
        "Tipo_Atividade", "Autores", "Titulo", "Revista_Veiculo", 
        "Instituicao_Vinculo", "Edicao_Volume", "Paginas", 
        "Status_Lattes", "Status_ORCID", "Status_LinkedIn"
    ]
    
    for col in colunas_texto:
        # Transforma tudo em texto e limpa os 'None'
        df_atual[col] = df_atual[col].fillna("").astype(str)
        df_atual[col] = df_atual[col].replace("None", "").replace("nan", "")
        
    # Exibe a tabela editável com o comando de largura atualizado
    df_editado = st.data_editor(
        df_atual, 
        num_rows="dynamic",
        key="editor_dados",
        width="stretch" 
    )
    
    # Salva e atualiza instantaneamente se houver mudanças
    if not df_editado.equals(df_atual):
        df_editado.to_excel(ARQUIVO_DADOS, index=False)
        st.rerun()
        
    # ==========================================
    # NOVO GERADOR BIBTEX
    # ==========================================
    def exportar_bibtex(df):
        bibtex = ""
        for i, row in df.iterrows():
            if not str(row['Titulo']).strip():
                continue # Pula linhas vazias
                
            # Isola o último nome do primeiro autor para criar a chave
            lista_autores = str(row['Autores']).split(',')
            primeiro_autor = lista_autores[0].strip().split(' ')[-1] if lista_autores[0] else "Autor"
            chave = f"{primeiro_autor}_{row['Ano_Publicacao']}"
            
            bibtex += f"@article{{{chave},\n"
            bibtex += f"  title={{{row['Titulo']}}},\n"
            bibtex += f"  publisher={{{row['Revista_Veiculo']}}},\n"
            bibtex += f"  author={{{row['Autores']}}},\n"
            
            # Adiciona páginas e volume apenas se existirem
            if str(row['Edicao_Volume']).strip():
                bibtex += f"  volume={{{row['Edicao_Volume']}}},\n"
            if str(row['Paginas']).strip():
                bibtex += f"  pages={{{row['Paginas']}}},\n"
                
            bibtex += f"  year={{{row['Ano_Publicacao']}}}\n"
            bibtex += "}\n\n"
        return bibtex

    st.markdown("---")
    col_excel, col_bib = st.columns(2)
    
    with col_excel:
        with open(ARQUIVO_DADOS, "rb") as file:
            st.download_button(
                "📊 Baixar Tabela (Excel)", 
                data=file, 
                file_name="guara_producoes.xlsx", 
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
    with col_bib:
        txt_bibtex = exportar_bibtex(df_editado)
        st.download_button(
            "📜 Baixar Padrão ORCID (BibTeX)",
            data=txt_bibtex,
            file_name="obras_orcid.bib",
            mime="text/plain"
        )

with aba3:
    st.markdown("### Sincronização Automática com ORCID")
    with st.form("form_orcid"):
        col_id, col_token = st.columns(2)
        with col_id:
            orcid_id_input = st.text_input("Seu ORCID ID")
        with col_token:
            access_token_input = st.text_input("Seu Access Token", type="password") 
            
        if st.form_submit_button("Sincronizar Pendentes", type="primary"):
            if orcid_id_input and access_token_input:
                pendentes = df_atual[df_atual['Status_ORCID'] == 'Pendente']
                if pendentes.empty:
                    st.info("Tudo atualizado!")
                else:
                    progresso = st.progress(0)
                    for i, (index, row) in enumerate(pendentes.iterrows()):
                        sucesso = enviar_para_orcid(orcid_id_input, access_token_input, row['Titulo'], row['Ano_Publicacao'], row['Tipo_Atividade'])
                        if sucesso:
                            df_atual.at[index, 'Status_ORCID'] = 'Enviado'
                        progresso.progress((i + 1) / len(pendentes))
                        time.sleep(1.5)
                    df_atual.to_excel(ARQUIVO_DADOS, index=False)
                    st.success("Concluído!")
                    time.sleep(1)
                    st.rerun()
