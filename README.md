# 📥 Script de Download de Licitações - Portal do Acre

Este projeto automatiza o processo de **login, acesso e download** dos arquivos de **licitações em PDF** publicados no site oficial do Governo do Estado do Acre:  
🔗 https://licitacao.ac.gov.br/editais/

> ⚠️ O portal **não possui API pública**. Por isso, este script simula o acesso humano e baixa os arquivos diretamente.

---

## ✨ Funcionalidades

- Realiza **login automático** com CPF/CNPJ e senha cadastrados no portal
- Acessa a página de **lista de editais**
- **Detecta e baixa** todos os arquivos PDF disponíveis
- Armazena os arquivos localmente na pasta `pdfs_editais/`
- **Evita downloads duplicados** (não baixa arquivos já existentes)

---

## 📦 Requisitos

- Python 3.7+
- Conexão com a internet
- Conta válida no portal de licitações do Acre

### Instalar dependências

```bash
pip install requests beautifulsoup4
