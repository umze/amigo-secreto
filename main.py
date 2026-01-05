from rich import print
import os
import platform
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from getpass import getpass
import random
import json

# =========================
# ARQUIVOS / DADOS
# =========================

FRIENDS_FILE = "friends.json"
friends = {}  # vai ser carregado do json ao iniciar

HTML_TEMPLATE = """\
<html>
  <body style="margin:0;padding:0;background:#f5f5f5;font-family:Arial,Helvetica,sans-serif;">
    <div style="max-width:560px;margin:24px auto;background:#ffffff;border-radius:12px;overflow:hidden;border:1px solid #e6e6e6;">

      <div style="padding:18px 20px;background:#111827;color:#ffffff;">
        <div style="font-size:18px;font-weight:700;">🎁 Amigo Secreto</div>
        <div style="opacity:0.85;font-size:13px;margin-top:4px;">Seu amigo secreto chegou!</div>
      </div>

      <div style="padding:20px;color:#111827;">
        <p style="margin:0 0 12px 0;font-size:15px;">Oi, <b>{nome}</b>!</p>

        <div style="background:#f9fafb;border:1px solid #e5e7eb;border-radius:10px;padding:14px 14px;margin:14px 0;">
          <div style="font-size:13px;color:#6b7280;margin-bottom:6px;">Você tirou:</div>
          <div style="font-size:20px;font-weight:800;">{sorteado}</div>
        </div>

        <ul style="margin:0 0 14px 18px;padding:0;font-size:14px;color:#111827;">
          <li>Não conte pra ninguém (nem pro seu cachorro ou para o Martin).</li>
          <li>Capricha no presente (ou não, se tu odiar a pessoa que tirou).</li>
        </ul>

        <p style="margin:0;font-size:14px;color:#374151;">
          Boa sorte!<br>
        </p>
      </div>
    </div>
  </body>
</html>
"""

TEXT_FALLBACK = """\
Oi, {nome}!

Chegou o Amigo Secreto 😈
Você tirou: {sorteado}

Não conte pra ninguém.
Boa sorte!
"""


# =========================
# UTILITÁRIOS
# =========================

def clearTerminal():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def pause(msg="Pressione ENTER para continuar..."):
    getpass(msg)


def is_valid_email(s: str) -> bool:
    # validação simples pra evitar besteira óbvia
    return isinstance(s, str) and "@" in s and "." in s and " " not in s


def set_env_var(key, value, env_path=".env"):
    lines = []
    found = False

    try:
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        pass

    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            found = True
            break

    if not found:
        lines.append(f"{key}={value}\n")

    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(lines)


# =========================
# JSON: SALVAR / CARREGAR FRIENDS
# =========================

def save_friends():
    # Salva o dict "friends" em friends.json
    try:
        with open(FRIENDS_FILE, "w", encoding="utf-8") as f:
            json.dump(friends, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print("[red][ERRO][/red] Não consegui salvar friends.json")
        print("Log:", type(e).__name__, e)


def load_friends():
    # Carrega friends.json para o dict "friends"
    global friends

    if not os.path.exists(FRIENDS_FILE):
        friends = {}
        return

    try:
        with open(FRIENDS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            friends = data if isinstance(data, dict) else {}
    except Exception as e:
        friends = {}
        print("[yellow][AVISO][/yellow] friends.json estava inválido e foi ignorado.")
        print("Log:", type(e).__name__, e)
        pause()


# =========================
# SORTEIO (SEM LOOP INFINITO)
# =========================

def sattolo_cycle(items):
    """
    Algoritmo de Sattolo: cria um ciclo único, garantindo que ninguém fica no mesmo lugar
    (ou seja, ninguém tira a si mesmo), desde que len(items) >= 2.
    """
    a = list(items)
    n = len(a)
    if n < 2:
        return a

    for i in range(n - 1, 0, -1):
        j = random.randrange(0, i)  # 0 <= j < i
        a[i], a[j] = a[j], a[i]
    return a


def make_pairs(friends_dict):
    names = list(friends_dict.keys())
    if len(names) < 2:
        return None

    shuffled = sattolo_cycle(names)
    pairs = {names[i]: shuffled[i] for i in range(len(names))}

    # paranoia saudável
    if any(k == v for k, v in pairs.items()):
        return None

    return pairs


# =========================
# MENUS: FRIENDS
# =========================

def friendList():
    while True:
        clearTerminal()
        print("[blue]Criar lista de amigos[/blue]")
        print("-------------")
        print("[cyan]Sua lista atual:[/cyan]")
        print(friends if friends else "[dim]vazia[/dim]")
        print("-------------")
        print("1 - Adicionar amigo")
        print("2 - Remover amigo")
        print("3 - Voltar")
        print("-------------")
        resp = input("Escolha uma opção: ").strip()

        if resp == "1":
            friendListAdd()
        elif resp == "2":
            friendListRemove()
        elif resp == "3":
            return


def friendListAdd():
    clearTerminal()
    print("[blue]Adicionar amigo[/blue]")
    print("-------------")
    newFriend = input("Digite o nome do novo amigo: ").strip()
    newFriendEmail = input("Digite o email do novo amigo: ").strip()

    if not newFriend:
        print("[red][ERRO][/red] Nome vazio.")
        pause()
        return

    if not is_valid_email(newFriendEmail):
        print("[red][ERRO][/red] Email parece inválido.")
        pause()
        return

    friends[newFriend] = newFriendEmail
    save_friends()
    print("[green][SUCESSO][/green] Amigo adicionado/atualizado e salvo no JSON.")
    pause()


def friendListRemove():
    clearTerminal()
    print("[blue]Remover amigo[/blue]")
    print("-------------")
    print("[cyan]Sua lista atual:[/cyan]")
    print(friends if friends else "[dim]vazia[/dim]")
    print("-------------")
    removeFriend = input("Digite o nome do amigo que deseja remover: ").strip()

    if removeFriend in friends:
        del friends[removeFriend]
        save_friends()
        print("[green][SUCESSO][/green] Removido e salvo no JSON.")
    else:
        print("[red][ERRO][/red] Não achei esse nome na lista.")
    pause()

def resetFriends():
    clearTerminal()
    print("[red]RESETAR LISTA DE AMIGOS[/red]")
    print("-------------")
    print("[red]ATENÇÃO[/red]")
    print("Isso vai APAGAR toda a lista de amigos.")
    print("Essa ação NÃO pode ser desfeita.")
    print("-------------")

    confirm = input("Digite 'SIM' para confirmar: ").strip().upper()

    if confirm != "SIM":
        print("[yellow]Operação cancelada.[/yellow]")
        pause()
        return

    friends.clear()
    save_friends()  # sobrescreve friends.json vazio

    print("[green][SUCESSO][/green] Lista de amigos resetada com sucesso.")
    pause()



# =========================
# MENU: EMAIL CONFIG
# =========================

def configEmail():
    while True:
        clearTerminal()
        print("[blue]Configurar/testar email[/blue]")
        print("-------------")
        print("[red]AVISO![/red]")
        print("Use um email alternativo. Não compartilhe o .env.")
        print("-------------")
        print("1 - Definir email")
        print("2 - Definir senha (senha de app)")
        print("3 - Testar login SMTP")
        print("4 - Voltar")
        print("-------------")
        resp = input("Escolha uma opção: ").strip()

        if resp == "1":
            setEmail()
        elif resp == "2":
            setPass()
        elif resp == "3":
            testEmail()
        elif resp == "4":
            return


def setEmail():
    clearTerminal()
    print("[blue]Definir email[/blue]")
    print("-------------")
    email = input("Digite o email (Gmail): ").strip()

    if not is_valid_email(email):
        print("[red][ERRO][/red] Email parece inválido.")
        pause()
        return

    set_env_var("EMAIL_USER", email)
    print("[green][SUCESSO][/green] EMAIL_USER salvo no .env.")
    pause()


def setPass():
    clearTerminal()
    print("[blue]Definir senha[/blue]")
    print("-------------")
    print("[red]AVISO![/red]")
    print("Use SENHA DE APP do Google (com 2FA ligado).")
    print("Por segurança, não aparece enquanto digita.")
    print("-------------")
    passw = getpass("Digite a senha de app aqui: ").strip()

    if not passw:
        print("[red][ERRO][/red] Senha vazia.")
        pause()
        return

    set_env_var("EMAIL_PASS", passw)
    print("[green][SUCESSO][/green] EMAIL_PASS salvo no .env.")
    pause()


def testEmail():
    clearTerminal()
    print("[blue]Testar login SMTP[/blue]")
    print("-------------")

    load_dotenv(override=True)
    user = os.getenv("EMAIL_USER")
    pwd = os.getenv("EMAIL_PASS")

    print("[INFO] Verificando EMAIL_USER e EMAIL_PASS...")
    if not user or not pwd:
        print("[red][ERRO][/red] EMAIL_USER ou EMAIL_PASS não estão definidos.")
        pause()
        return

    print("[INFO] Tentando conectar e logar no SMTP do Gmail...")
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as smtp:
            smtp.login(user, pwd)
        print("[green][SUCESSO][/green] Login SMTP OK!")
    except smtplib.SMTPAuthenticationError as e:
        print("[red][ERRO][/red] Falha de autenticação. (senha de app? 2FA?)")
        print("Log:", e)
    except Exception as e:
        print("[red][ERRO][/red] Erro de conexão.")
        print("Log:", type(e).__name__, e)

    pause()


# =========================
# SORTEIO + ENVIO
# =========================

def sendEmail():
    clearTerminal()
    load_dotenv(override=True)
    user = os.getenv("EMAIL_USER")
    pwd = os.getenv("EMAIL_PASS")

    print("[blue]Sortear e enviar emails[/blue]")
    print("-------------")
    print("[cyan]Sua lista de amigos:[/cyan]")
    print(friends if friends else "[dim]vazia[/dim]")
    print("-------------")

    if len(friends) < 2:
        print("[red][ERRO][/red] Precisa de pelo menos 2 amigos na lista.")
        pause()
        return

    if not user or not pwd:
        print("[red][ERRO][/red] Não foi definido EMAIL_USER ou EMAIL_PASS no .env.")
        pause()
        return

    print("[INFO] Sorteando...")
    pairs = make_pairs(friends)
    if not pairs:
        print("[red][ERRO][/red] Não foi possível gerar um sorteio válido. Tente de novo.")
        pause()
        return

    success = []
    failed = []

    try:
        print("[INFO] Conectando ao SMTP...")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as smtp:
            smtp.login(user, pwd)
            print("[green][SUCESSO][/green] Conectado!")

            print("[INFO] Enviando emails...")
            for nome, email_to in friends.items():
                sorteado = pairs[nome]

                html_body = HTML_TEMPLATE.format(nome=nome, sorteado=sorteado)
                text_body = TEXT_FALLBACK.format(nome=nome, sorteado=sorteado)

                msg = EmailMessage()
                msg["Subject"] = "🎁 Seu amigo secreto está aqui!"
                msg["From"] = user
                msg["To"] = email_to
                msg.set_content(text_body)  # fallback
                msg.add_alternative(html_body, subtype="html")

                try:
                    print("[INFO] Enviando para", email_to)
                    smtp.send_message(msg)
                    print("[green][SUCESSO][/green] O email foi enviado com sucesso para", email_to)
                    success.append(email_to)
                except Exception as e:
                    print("[red][ERRO][/red] O envio falhou para", email_to)
                    print("Log:", type(e).__name__, e)
                    failed.append((email_to, type(e).__name__))

    except smtplib.SMTPAuthenticationError as e:
        print("[red][ERRO][/red] Falha ao autenticar no SMTP (senha de app/2FA).")
        print("Log:", e)
        pause()
        return
    except Exception as e:
        print("[red][ERRO][/red] Erro geral de conexão/envio.")
        print("Log:", type(e).__name__, e)
        pause()
        return

    # ====== 3 PASSOS FINAIS ======
    print("-------------")
    print("[cyan]ENVIO FINALIZADO[/cyan]")
    print("-------------")
    print(f"[green]Enviados com sucesso:[/green] {len(success)}")
    print(f"[red]Falharam:[/red] {len(failed)}")
    print("-------------")

    if failed:
        print("[red]Lista de falhas:[/red]")
        for email_to, err_name in failed:
            print("-", email_to, f"[dim]({err_name})[/dim]")
        print("-------------")
        print("[yellow]Dica:[/yellow] Verifique emails, spam, bloqueio do Gmail e a senha de app.")
    else:
        print("[green][SUCESSO][/green] Todos os emails foram enviados com sucesso!")
    pause()


# =========================
# MENU PRINCIPAL
# =========================

def main_menu():
    while True:
        clearTerminal()
        print("[blue]Amigo Secreto[/blue]")
        print("-------------")
        print("1 - Criar lista de amigos")
        print("2 - Sortear e enviar emails")
        print("3 - Configurar/testar email")
        print("4 - Resetar lista de amigos")
        print("5 - Sair")
        print("-------------")
        resp = input("Escolha uma opção: ").strip()

        if resp == "1":
            friendList()
        elif resp == "2":
            sendEmail()
        elif resp == "3":
            configEmail()
        elif resp == "4":
            resetFriends()
        elif resp == "5":
            return


if __name__ == "__main__":
    load_friends()  # carrega friends.json automaticamente ao iniciar
    main_menu()
    