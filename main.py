import sqlite3 #biblioteca do banco de dados
from datetime import date #biblioteca para trabalhar com o tempo (data e hora)

#conexão com o banco de dados
conexao = sqlite3.connect('elixo.db') #abre o arquivo do banco
cursor = conexao.cursor() #executa os comando do SQL no banco

#tabela de login/cadastro de usuarios
cursor.execute("""
create table if not exists usuarios(
    id integer primary key autoincrement,
    nome text not null,
    tipo text not null,
    cpf text,
    cnpj text,
    email text not null unique,
    senha text not null
)
""")

#tabela de locais físicos que recebem e-lixo
cursor.execute("""
create table if not exists pontos_coleta(
    id integer primary key autoincrement,
    usuarios_id integer not null,
    nome text not null,
    endereco text not null,
    foreign key (usuarios_id) references usuarios(id))
""")

#tabela materias
cursor.execute("""
create table if not exists materiais(
    id integer primary key autoincrement,
    nome text not null,
    categoria text)
""")

#tabela que vai conecta as demais tabelas
cursor.execute("""
create table if not exists descartes(
    id integer primary key autoincrement,
    usuarios_id integer not null,
    pontos_coleta_id integer not null,
    materiais_id integer not null,
    data_descarte text not null,
    foreign key (usuarios_id) references usuarios(id),
    foreign key (pontos_coleta_id) references pontos_coleta(id),
    foreign key (materiais_id) references materiais(id)
    
)
""")


base = 32
tamanho = 95

saber = {
    '1':'Pessoa',
    '2':'Empresa'
}

categoria = {
    '1':'Eletrônicos',
    '2':'Informática',
    '3':'Eletrodomésticos',
    '4':'Pilhas e Baterias',
    '5':'Cabos e Acessórios',
    '6':'Lâmpadas',
    '7':'Componentes Eletrônicos'
}

#Cripto da senha
def cesar(texto,deslocamento):
    resultado = ''
    for letra in texto:
        numero = ord(letra) #pega o codigo ASCII da letra
        numero -= base #recalibra pra escala 0-25
        deslocado = (numero + deslocamento) % tamanho #aplica o deslocamento e da a volta se estourar
        deslocado += base #volta para o ASCII real
        nova_letra = chr(deslocado) #transforma n° de volta em letra
        resultado += nova_letra
    return resultado


def decifrar(texto,deslocamento): #desfaz cesar tem a mesma logica só que subtrai o deslocamento
    resultado = ''
    for letra in texto:
        numero = ord(letra)
        numero -= base
        deslocado = (numero - deslocamento) % tamanho
        deslocado += base
        nova_letra = chr(deslocado)
        resultado += nova_letra
    return resultado

#Aplicação de XOR
'''
Funciona para letra e n°
Cifra e decifra
'''
def xor(texto, chave):
    resultado = ''
    for letra in texto:
        numero = ord(letra)
        numero_xor = numero ^ chave
        nova_letra = chr(numero_xor)
        resultado += nova_letra
    return resultado

#Cifra em duas camas: Cesar e XOR
def cifras(texto, deslocamento, chave_xor):
    p1 = cesar(texto,deslocamento)
    p2 = xor(p1,chave_xor)
    return p2

#Decifra na ordem inversa: XOR e Cesar
def decifras(texto, deslocamento, chave_xor):
    p1 = xor(texto,chave_xor)
    p2 = decifrar(p1,deslocamento)
    return p2

#Cripto CPF
def cpf_cesar(txt, deslocamento): #adaptada pra digitos (0-9,10 digitos no total), trocada pela base 48/10
    resultado = ''
    for num in txt:
        numero = ord(num)
        numero -= 48 #recalibra pra escala 0-9
        deslocado = (numero + deslocamento) % 10 #desloca e dá a volta a cada 10 digitos
        deslocado += 48 #volta pra escala ASCII real
        cpf_cifras = chr(deslocado)
        resultado += cpf_cifras
    return resultado

#desfaz cesar
def cpf_descifras(txt, deslocamento):
    resultado = ''
    for num in txt:
        numero = ord(num)
        numero -= 48
        deslocado = (numero - deslocamento) % 10
        deslocado += 48
        descifras_cpf = chr(deslocado)
        resultado += descifras_cpf
    return resultado

#cifra em duas camadas: cesar numerico e xor me cima
def cpf_cifras(cpf, deslocamento, chave_xor):
    p1 = cpf_cesar(cpf, deslocamento)
    p2 = xor(p1,chave_xor)
    return p2

#decifra na ordem inversa: xor e cesar
def cpf_decifras(cpf, deslocamento, chave_xor):
    p1 = xor(cpf,chave_xor)
    p2 = cpf_descifras(p1, deslocamento)
    return p2

DESLOCAMENTO = 3  # chave do César
CHAVE_XOR = 5  # chave do XOR

#cripto cnpj
def cnpj_cesar(txt,deslocamento):
    resultado = ''
    for num in txt:
        numero = ord(num)
        numero -= 48  # recalibra pra escala 0-9
        deslocado = (numero + deslocamento) % 10  # desloca e dá a volta a cada 10 digitos
        deslocado += 48  # volta pra escala ASCII real
        cnpj_cifras = chr(deslocado)
        resultado += cnpj_cifras
    return resultado

#decifra cnpj
def cnpj_descifras(txt,deslocamento):
    resultado = ''
    for num in txt:
        numero = ord(num)
        numero -= 48
        deslocado = (numero - deslocamento) % 10
        deslocado += 48
        descifras_cnpj = chr(deslocado)
        resultado += descifras_cnpj
    return resultado

#cifra em duas camadas: cesar numerico e xor me cima
def cnpj_cifras(cnpj, deslocamento, chave_xor):
    p1 = cnpj_cesar(cnpj, deslocamento)
    p2 = xor(p1,chave_xor)
    return p2

#decifra na ordem inversa: xor e cesar
def cnpj_decifras(cnpj,deslocamento, chave_xor):
    p1 = xor(cnpj,chave_xor)
    p2 = cnpj_descifras(p1, deslocamento)
    return p2


def cadastrar():
   cpf_protegido = None
   cnpj_protegido = None

   nome = input('Digite seu nome: ')
   email = input('Digite seu e-mail: ').strip().lower()

   while True:
        for chave, valor in saber.items():
            print(f"{chave} - {valor}")
        qual = input('Escolha sua categoria: ')
        if qual == '1':
            tipo = saber[qual]
            while True:
                cpf = input('Digite seu CPF: ').strip()
                if cpf.isdigit() and len(cpf) == 11:
                    print('CPF válido!')
                    cpf_protegido = cpf_cifras(cpf, DESLOCAMENTO, CHAVE_XOR)
                    break
                else:
                    print('CPF inválido! Digite os 11 números.')
            break
        elif qual == '2':
            tipo = saber[qual]
            while True:
                cnpj = input('Digite seu CNPJ: ').strip()
                if cnpj.isdigit() and len(cnpj) == 14:
                    print('CNPJ válido!')
                    cnpj_protegido = cnpj_cifras(cnpj, DESLOCAMENTO, CHAVE_XOR)
                    break
                else:
                    print('CNPJ inválido! Digite os 14 números.')
            break
        else:
            print('Opção inválida! Escolha 1 ou 2.')

   senha = input('Digite sua senha: ')
   senha_cifrada = cifras(senha, DESLOCAMENTO, CHAVE_XOR)
   try:
        cursor.execute('insert into usuarios (nome,tipo, cpf, cnpj,email, senha ) values (?,?,?,?,?,?) ', (nome,tipo,cpf_protegido, cnpj_protegido, email, senha_cifrada,))
        conexao.commit()
        print('Cadastro feito com sucesso!')
   except sqlite3.IntegrityError:
        print('E-mail já cadastrado!')


def login():
    email = input('Digite seu e-mail:').strip().lower()
    senha = input('Digite sua senha: ')
    cursor.execute('select id,tipo,senha from usuarios where email = ?',(email,))
    busca = cursor.fetchone()
    if not busca:
        print('E-mail ou Senha incorretos!')
        return None
    else:
        id_user = busca[0]
        tipo = busca[1]
        senha_banco = busca[2]
        senha_original = decifras(senha_banco, DESLOCAMENTO, CHAVE_XOR)
        if senha == senha_original:
            print('Login feito com sucesso!')
            return id_user, tipo
        else:
            print('E-mail ou Senha incorretos!')
            return None


def material(usuario_id):
    nome_material = input('Qual o material que deseja descartar?')
    while True:
        print('Escolha uma categoria:')
        for i, cat in categoria.items():
            print(f'{i} - {cat}:\n')
        c = input('Digite sua categoria: ')
        if c in categoria:
            certa = categoria[c]
            break
        else:
            print('Categoria inválida!')

    pontos = listar_pontos()
    if not pontos:
        print('Cadastre um ponto de coleta antes de registrar o descarte!')
        return

    while True:
        escolha = input('Digite o ID do ponto escolhido: ')

        if escolha.isdigit() and any(p[0] == int(escolha) for p in pontos):
            ponto_id = int(escolha)
            break
        else:
            print('Ponto inválido!')

    cursor.execute('insert into materiais (nome, categoria) values (?,?) ', (nome_material, certa,))
    conexao.commit()
    print('Material cadastrado com sucesso!')
    material_id = cursor.lastrowid
    cursor.execute('''INSERT INTO descartes(usuarios_id, pontos_coleta_id, materiais_id, data_descarte)VALUES (?, ?, ?, ?) ''', (usuario_id, ponto_id, material_id, date.today().isoformat()))
    conexao.commit()
    print('Material cadastrado e descarte registrado com sucesso!')

def ponto(usuarios_id):
    nome_ponto = input('Nome do ponto de coleta:')
    endereco = input('Endereço: ')
    cursor.execute('insert into pontos_coleta (usuarios_id, nome, endereco) values (?,?,?)', (usuarios_id, nome_ponto, endereco))
    conexao.commit()
    print('Ponto cadastrado com sucesso!')


def listar_pontos():
    cursor.execute('select id,nome, endereco from pontos_coleta')
    pontos = cursor.fetchall()
    if not pontos:
        print('Não tem pontos cadastrados!')
        return False
    else:
        for p in pontos:
            print(f'{p[0]} - {p[1]} - {p[2]}')
    return pontos

def lista_menu(usuario_id, tipo):
    while True:
        if tipo == 'Empresa':
            print('[1] Novo ponto\n'
                  '[2] Ver pontos de coleta\n'
                  '[0] Sair')
            escolha = input('Escolha uma opção:')
            if escolha == '1':
                ponto(usuario_id)
            elif escolha == '2':
                listar_pontos()
            elif escolha == '0':
                break
            else:
                print('Opção Inválida!')
        elif tipo == 'Pessoa':
            print('[1] Novo Material\n'
                  '[2] Ver pontos de coleta\n'
                  '[0] Sair')
            escolha = input('Escolha uma opção:')
            if escolha == '1':
                material(usuario_id)
            elif escolha == '2':
                listar_pontos()
            elif escolha == '0':
                break
            else:
                print('Opção Inválida!')
        else:
            break

while True:
    print('[1] Cadastrar\n'
          '[2] Login\n'
          '[3] Sair\n')
    opc = input('Escolha um opção:')
    if opc == '1':
        cadastrar()
    elif opc == '2':
       user = login()
       if user:
           usuario_id, tipo = user
           print('Bem-vindo(a)!')
           lista_menu(usuario_id, tipo)
       else:
           print('Login incorreto!')
    elif opc == '3':
        print('Saindo do sistema!')
        break
    else:
        print('Opção Inválida!')

conexao.close()


    


