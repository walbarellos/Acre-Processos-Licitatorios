import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# -------------------------------
# CONFIGURAÇÕES INICIAIS
# -------------------------------

# Endereços do sistema de licitações do Acre
LOGIN_URL = 'https://licitacao.ac.gov.br/editais/check_login.php'
LISTA_URL = 'https://licitacao.ac.gov.br/editais/index.php?task=lista_editais'

# Pasta onde os arquivos PDF serão salvos
DESTINO_PASTA = 'pdfs_editais'

# Informe seu CPF ou CNPJ de login e a senha do sistema (geralmente 4 a 5 dígitos)
USUARIO = os.getenv('USUARIO')
SENHA = os.getenv('SENHA')

# Verifica se as credenciais foram definidas no .env
if not USUARIO or not SENHA:
    raise Exception("❌ As variáveis de ambiente USUARIO e SENHA não foram definidas. Crie um arquivo .env e adicione as credenciais.")

# -------------------------------
# FAZENDO LOGIN NO SISTEMA
# -------------------------------

# Cria uma sessão para manter o login ativo durante as próximas requisições
sessao = requests.Session()

# Dados enviados no formulário de login
payload = {
    'cnpj': USUARIO,              # Campo "cnpj" recebe CPF ou CNPJ
    'senha': SENHA,               # Campo "senha" recebe a senha do sistema
    'task': 'check_login',        # Campos ocultos que fazem parte da autenticação
    'option': 'com_licitacoes'
}

# Envia os dados para o sistema para fazer o login
res_login = sessao.post(LOGIN_URL, data=payload)

# Verifica se o login funcionou corretamente
if "index.php?task=lista_editais" not in res_login.text and "sair" not in res_login.text.lower():
    print("⚠️ Erro: conteúdo retornado pelo sistema (parcial):\n", res_login.text[:1000])
    raise Exception("❌ Login falhou — verifique se o CPF/CNPJ e a senha estão corretos.")

# -------------------------------
# ACESSANDO A LISTA DE EDITAIS
# -------------------------------

# Após login, acessa a página onde estão os links dos editais
res_lista = sessao.get(LISTA_URL)

# Interpreta o conteúdo HTML da página usando BeautifulSoup
soup = BeautifulSoup(res_lista.text, 'html.parser')

# Procura por todos os links que terminam em ".pdf"
pdf_links = [
    urljoin(LISTA_URL, a['href'])  # Monta o link completo do PDF
    for a in soup.find_all('a', href=True)
    if a['href'].lower().endswith('.pdf')
]

print(f"🔎 Foram encontrados {len(pdf_links)} arquivos PDF de editais.")

# -------------------------------
# FAZENDO O DOWNLOAD DOS EDITAIS
# -------------------------------

# Cria a pasta onde os PDFs serão salvos (se ainda não existir)
os.makedirs(DESTINO_PASTA, exist_ok=True)

# Baixa um por um os arquivos encontrados
for link in pdf_links:
    # Extrai o nome do arquivo a partir do link
    nome_arquivo = os.path.basename(link.split('/')[-1])

    # Monta o caminho completo onde o arquivo será salvo localmente
    caminho = os.path.join(DESTINO_PASTA, nome_arquivo)

    # Verifica se o arquivo já existe para evitar baixar novamente
    if not os.path.exists(caminho):
        print(f"⬇️  Baixando: {nome_arquivo}")
        r = sessao.get(link)  # Baixa o conteúdo do arquivo PDF
        with open(caminho, 'wb') as f:
            f.write(r.content)  # Salva o conteúdo do PDF no disco
    else:
        print(f"✅ Já existe: {nome_arquivo}")
