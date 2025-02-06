import os
import markdown
import yaml
import json
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# Caminhos para os diretórios
input_dir = r"D:\_ethalya _vault\Caps"          # Diretório com arquivos .md
output_dir = r"../charpters" # Onde os arquivos PHP serão salvos
template_path = r"../templates/template.php"  # Caminho para o template PHP
json_file_path = "generated_files.json"  # Onde armazenaremos os arquivos PHP gerados

################# Funções Suporte #################
def load_generated_files():
    """Carrega os dados do arquivo JSON e valida o formato."""
    try:
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

                # Validação: todos os valores devem ser dicionários
                for key, value in data.items():
                    if not isinstance(value, dict):
                        print(f"{Fore.YELLOW}Corrigindo entrada inválida no JSON para o arquivo {key}.")
                        data[key] = {"created_at": "", "updated_at": ""}

                return data
        else:
            return {}
    except json.JSONDecodeError as e:
        print(f"Erro ao carregar o arquivo JSON: {e}")
        return {}

def save_generated_files(generated_files):
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(generated_files, f, ensure_ascii=False, indent=4)

def update_generated_file_status(filename, status="created"):
    generated_files = load_generated_files()
    current_time = datetime.now().isoformat()  # Formata a data/hora como string
    
    if filename not in generated_files:
        # Novo arquivo: adiciona as datas de criação e última atualização
        generated_files[filename] = {
            "created_at": current_time,
            "updated_at": current_time,
        }
    elif status == "updated":
        # Atualiza a data de última atualização
        generated_files[filename]["updated_at"] = current_time
    
    # Salva as mudanças no JSON
    save_generated_files(generated_files)

def step():
    print("\n")
    step = input("Aperte Enter para voltar ao menu>>>")
    print("\n")
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Unix/Linux/MacOS
        os.system('clear')

################# Funções Ativas #################
def generate_php_files():
    print("Gerando novos arquivos PHP...\n")
    generated_files = load_generated_files()

    for filename in os.listdir(input_dir):
        if filename.endswith('.md'):
            md_path = os.path.join(input_dir, filename)
            php_filename = f"{os.path.splitext(filename)[0]}.php"
            
            # Lê o conteúdo do arquivo .md e verifica o status
            with open(md_path, 'r', encoding='utf-8') as md_file:
                md_content = md_file.read()
            
            parts = md_content.split('---')
            if len(parts) < 3:
                continue
            
            metadata = yaml.safe_load(parts[1])
            status = metadata.get('Status', '').lower()
            
            if status != "finalizado":
                continue
            
            if filename in generated_files:
                print(f"Arquivo {filename} {Fore.YELLOW}{Style.BRIGHT}já foi gerado anteriormente. {Fore.RED}{Style.BRIGHT}Pulando...{Style.RESET_ALL}")
                continue
            
            # Gera o arquivo PHP (mesma lógica anterior)
            with open(template_path, 'r', encoding='utf-8') as template_file:
                template = template_file.read()
            
            php_content = template.replace("{{Title}}", metadata.get('Title', 'Sem título'))
            php_content = php_content.replace("{{charpter}}", metadata.get('Charpter', 'N/A'))
            php_content = php_content.replace("{{content}}", markdown.markdown(parts[2]))

            php_path = os.path.join(output_dir, php_filename)
            with open(php_path, 'w', encoding='utf-8') as php_file:
                php_file.write(php_content)
            
            # Registra no JSON a data de criação
            update_generated_file_status(filename)
            print(f"Arquivo {php_filename} {Fore.GREEN}{Style.BRIGHT}gerado com sucesso.{Style.RESET_ALL}")
    step()

def att_caps():
    print("Atualizando capítulos...")
    generated_files = load_generated_files()

    for filename in os.listdir(input_dir):
        if filename.endswith('.md'):
            md_path = os.path.join(input_dir, filename)

            # Lê o conteúdo do arquivo para verificar o status
            with open(md_path, 'r', encoding='utf-8') as md_file:
                md_content = md_file.read()

            parts = md_content.split('---')
            if len(parts) < 3:
                print(f"Arquivo {filename} está mal formatado. {Fore.RED}{Style.BRIGHT}Pulando...{Style.RESET_ALL}")
                continue

            # Carrega os metadados
            metadata = yaml.safe_load(parts[1])
            status = metadata.get('Status', '').lower()

            # Verifica o status do capítulo
            if status != "finalizado":
                print(f"Arquivo {filename} não está finalizado. {Fore.RED}{Style.BRIGHT}Pulando...{Style.RESET_ALL}")
                continue

            # Recupera informações do JSON ou cria valores padrão
            file_info = generated_files.get(filename, {"created_at": "", "updated_at": ""})

            # Obtém a data de atualização, usando um valor padrão se necessário
            updated_at_str = file_info.get("updated_at", "1970-01-01T00:00:00")
            
            # Validação robusta para updated_at_str
            try:
                last_updated_time = datetime.fromisoformat(updated_at_str).timestamp()
            except (ValueError, OSError):
                print(f"Formato inválido ou erro em 'updated_at' para o arquivo {filename}. Usando valor padrão.")
                last_updated_time = datetime(1970, 1, 1).timestamp()

            # Verifica se o arquivo foi modificado
            md_mod_time = os.path.getmtime(md_path)

            if md_mod_time > last_updated_time:
                print(f"Arquivo {filename} foi modificado. {Fore.MAGENTA}{Style.BRIGHT}Atualizando...{Style.RESET_ALL}")

                with open(template_path, 'r', encoding='utf-8') as template_file:
                    template = template_file.read()

                php_content = template.replace("{{Title}}", metadata.get('Title', 'Sem título'))
                php_content = php_content.replace("{{charpter}}", metadata.get('Charpter', 'N/A'))
                php_content = php_content.replace("{{content}}", markdown.markdown(parts[2]))

                php_filename = f"{os.path.splitext(filename)[0]}.php"
                php_path = os.path.join(output_dir, php_filename)

                with open(php_path, 'w', encoding='utf-8') as php_file:
                    php_file.write(php_content)

                # Atualiza a data de última atualização no JSON
                generated_files[filename] = {
                    "created_at": file_info.get("created_at", datetime.now().isoformat()),
                    "updated_at": datetime.now().isoformat()
                }
                save_generated_files(generated_files)
                print(f"Arquivo {php_filename} {Fore.GREEN}{Style.BRIGHT}atualizado com sucesso.{Style.RESET_ALL}")
            else:
                print(f"Arquivo {filename} {Fore.YELLOW}{Style.BRIGHT}não foi modificado.{Style.RESET_ALL} Nenhuma atualização necessária.")
    step()

def show_status():
    print("Exibindo status...\n")
    
    # Carrega o JSON com os arquivos gerados
    generated_files = load_generated_files()
    
    # Lista de arquivos .md prontos para serem transformados em .php
    ready_to_generate = []
    
    # Lista de arquivos .php que precisam ser atualizados
    needs_update = []
    
    # Itera sobre os arquivos .md no diretório de entrada
    for filename in os.listdir(input_dir):
        if filename.endswith('.md'):
            md_path = os.path.join(input_dir, filename)
            
            # Lê o conteúdo do arquivo .md
            with open(md_path, 'r', encoding='utf-8') as md_file:
                md_content = md_file.read()

            # Obtém o metadata (frontmatter) do arquivo Markdown
            parts = md_content.split('---')
            if len(parts) < 3:
                continue  # Se o arquivo não tem frontmatter, ignora o arquivo
            
            metadata = yaml.safe_load(parts[1])
            status = metadata.get('Status', '').lower()

            # Verifica se o status é "finalizado"
            if status == "finalizado":
                # Se o arquivo .md ainda não foi gerado, ele está pronto para ser transformado em .php
                php_filename = f"{os.path.splitext(filename)[0]}.php"
                php_path = os.path.join(output_dir, php_filename)
                
                if filename not in generated_files:
                    ready_to_generate.append(filename)  # Arquivo .md pronto para ser gerado
                else:
                    # Se o arquivo .php já foi gerado, verifica se precisa ser atualizado
                    md_mod_time = os.path.getmtime(md_path)
                    php_mod_time = os.path.getmtime(php_path)
                    
                    # Se o arquivo .md foi modificado após o .php ser gerado, precisa ser atualizado
                    if md_mod_time > php_mod_time:
                        needs_update.append(filename)  # Arquivo .php precisa ser atualizado
    
    # Exibe o status
    if ready_to_generate:
        print(f"Arquivos .md {Fore.GREEN}{Style.BRIGHT}prontos{Style.RESET_ALL} para ser transformados em .php:")
        for file in ready_to_generate:
            print(f" - {Fore.GREEN}{Style.BRIGHT}{file}{Style.RESET_ALL}")
    else:
        print("Nenhum arquivo .md pronto para ser transformado em .php.")

    if needs_update:
        print(f"\nArquivos .php que precisam ser {Fore.MAGENTA}{Style.BRIGHT}atualizados{Style.RESET_ALL}:")
        for file in needs_update:
            print(f"  - {Fore.MAGENTA}{Style.BRIGHT}{file}{Style.RESET_ALL}")
    else:
        print("Nenhum arquivo .php precisa ser atualizado.")

    step()

def show_menu(): 
    opt = [
        "Gerar Arquivos PHP",
        "Ver Status dos Capítulos",
        "Atualizar Capítulos",
        f"{Fore.RED}{Style.BRIGHT}Sair{Style.RESET_ALL}"
    ]

    print(f"{Fore.CYAN}{Style.BRIGHT}----- CHARPTER FLOW -----{Style.RESET_ALL}")
    for i,j in enumerate(opt,1):
        print(f"{Fore.CYAN}{i}{Style.RESET_ALL} - {j}")
    choice = input("Escolha uma opção: ")
    return choice

def main():
    while True:
        choice = show_menu()

        if choice == "1":
            generate_php_files()
        elif choice == "2":
            show_status()
        elif choice == "3":
            att_caps()
        elif choice == "4":
            print("Saindo do programa.")
            if os.name == 'nt':  # Windows
                os.system('cls')
            else:  # Unix/Linux/MacOS
                os.system('clear')
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()