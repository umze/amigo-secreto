# Amigo Secreto 🎁

Um script de console em Python para organizar sorteios de Amigo Secreto de forma fácil e automatizada. Ele gerencia a lista de participantes, realiza o sorteio garantindo que ninguém tire a si mesmo, e envia o resultado para cada um por e-mail.

## Funcionalidades

- **Gerenciamento de Amigos**: Adicione e remova participantes facilmente. A lista é salva em um arquivo `friends.json`.
- **Sorteio Inteligente**: Utiliza um algoritmo que garante um sorteio justo, sem que ninguém tire o próprio nome.
- **Envio Automático de E-mails**: Envia um e-mail personalizado para cada participante com o nome do amigo sorteado.
- **Configuração Segura**: Armazena suas credenciais de e-mail de forma segura em um arquivo `.env`, que não deve ser compartilhado.
- **Interface de Console**: Um menu simples e interativo para guiar o usuário por todas as etapas.

## Requisitos

- Python 3.6 ou superior (caso você baixe direto do código fonte)

## Instalação
### Código fonte:
1.  **Clone o repositório ou baixe os arquivos:**
    ```bash
    git clone https://github.com/umze/amigo-secreto.git
    cd amigo-secreto
    ```

2.  **Instale as dependências:**
    É recomendado criar um ambiente virtual (virtualenv) primeiro.
    ```bash
    pip install -r requirements.txt
    ```
3. **Execute o script a partir do seu terminal:**
    ```bash
    python main.py
    ```
### Executável:
Vá na aba "releases" do repositório, baixe o arquivo de acordo com o sistema operacional e abra ele. Simples!

## Configuração do E-mail

O script utiliza uma conta do Gmail para enviar os e-mails. Para que funcione, você precisa configurar seu e-mail e uma **Senha de App**.

**⚠️ Importante: Use uma Senha de App!**
Devido às políticas de segurança do Google, você não pode usar a sua senha normal do Gmail. É necessário gerar uma "Senha de App".

1.  **Ative a Verificação em Duas Etapas** na sua Conta Google, caso ainda não esteja ativa.
2.  Acesse [Senhas de app](https://myaccount.google.com/apppasswords) na sua Conta Google.
3.  Crie uma nova senha de app:
    -   **Selecione o app**: "E-mail"
    -   **Selecione o dispositivo**: "Outro (*nome personalizado*)" (ex: "Script Amigo Secreto")
    -   Clique em **Gerar**.
4.  O Google irá gerar uma senha de 16 caracteres. **Copie essa senha.**

Agora, no programa:

1.  Execute o programa
2.  Escolha a opção **3 - Configurar/testar email**.
3.  Escolha a opção **1 - Definir email** e insira seu endereço do Gmail.
4.  Escolha a opção **2 - Definir senha (senha de app)** e cole a **senha de 16 caracteres** que você gerou.
5.  Teste na opção **3 - Testar login SMTP**.

Essas informações serão salvas em um arquivo `.env` na pasta de dados do seu sistema operacional (a "appdata").
