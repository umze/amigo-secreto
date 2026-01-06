# Amigo Secreto 🎁

Um script de console em Python robusto para organizar sorteios de Amigo Secreto. Ele gerencia participantes, realiza o sorteio de forma cíclica (garantindo que ninguém tire a si mesmo) e envia os resultados via email com um layout HTML elegante e moderno.

## ✨ Funcionalidades

- **Persistência de Dados**: Salva a lista de amigos e configurações em pastas de sistema, garantindo que seus dados não sejam perdidos ao mover o script de pasta.
- **Sorteio Cíclico (Algoritmo de Sattolo)**: Garante matematicamente que ninguém tire a si mesmo e que o sorteio forme um ciclo único, onde todos presenteiam e são presenteados sem repetições.
- **Envio de emails em HTML**: Envia emails em HTML, tendo um visual bonito e totalmente personalizavel!
- **Segurança**: Gerenciamento de credenciais via variáveis de ambiente (`.env`) persistidas de forma segura no sistema.
- **Interface Rica**: Interface de terminal colorida e organizada utilizando a biblioteca `rich`.

---

## 🚀 Instalação e Execução

### 1. Requisitos
- Python 3.8 ou superior.
- Uma conta Gmail com **Verificação em Duas Etapas** ativa.

### 2. Preparação do Ambiente
Instale as dependências necessárias via pip:
```bash
pip install rich python-dotenv
```

### 3. Execução

```bash
python main.py
```

---

## 📧 Configuração do email (Gmail)

O script utiliza o servidor SMTP do Gmail. Devido às políticas de segurança do Google, você **não pode** usar sua senha normal.

1. **Ative a Verificação em Duas Etapas**: Obrigatório na sua conta Google.
2. **Gerar Senha de App**: Acesse [Senhas de App](https://myaccount.google.com/apppasswords).
3. **Gerar**: Escolha um nome (ex: "Amigo Secreto") e copie o código de 16 dígitos.
4. **No Programa**:
* Vá em `3 - Configurar/testar email`.
* Opção `1`: Digite seu email.
* Opção `2`: Cole a senha de 16 dígitos.
* Opção `3`: Teste a conexão.

---

## ❓ FAQ (Perguntas Frequentes)

### Onde os meus dados ficam salvos?

O script utiliza o padrão do sistema operacional para evitar poluir a pasta do projeto:

* **Windows**: `%appdata%\amigo_secreto\`
* **Linux**: `~/.local/share/amigo_secreto/`
* **macOS**: `~/Library/Application Support/amigo_secreto/`

### Como o sorteio garante que eu não me tire?

O código implementa o **Algoritmo de Sattolo**. Diferente de um sorteio aleatório comum que pode exigir várias tentativas até dar certo, o Sattolo cria um ciclo perfeito.

### Posso editar o modelo do email?

Sim. Dentro do arquivo `main.py`, você encontrará a variável `HTML_TEMPLATE`. Você pode alterar cores, textos e as "regras" diretamente lá.

### E se eu digitar um email errado?

Basta adicionar o amigo novamente com o **mesmo nome**. O script reconhecerá o nome existente e atualizará apenas o endereço de email no arquivo `friends.json`.

---

**Dica:** Sempre teste o envio com 2 emails próprios antes de disparar para o grupo todo para garantir que as configurações de rede e senha de app estão 100% corretas!
