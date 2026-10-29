# Sistema de Criptografia de Plataforma E-Lixo

Projeto acadêmico desenvolvido na disciplina Projeto e Desenvolvimento II (Sistemas de Informação, UNIP). Uma plataforma de descarte de lixo eletrônico em que pessoas e empresas se cadastram, e os dados sensíveis (senha e CPF) são protegidos por um algoritmo de criptografia criado do zero.

> ⚠️ **Aviso:** a criptografia deste projeto (Cifra de César + XOR) foi criada com fins **didáticos**, para estudar como funcionam esses algoritmos. Ela **não é segura para uso real**. Em produção, o correto é usar bibliotecas consolidadas, como bcrypt para senhas e Fernet para dados reversíveis.

## O que o sistema faz

- Cadastro de usuários do tipo **Pessoa** (CPF) ou **Empresa** (CNPJ), com validação de CPF
- Login com verificação de senha
- **Empresas:** cadastram pontos de coleta e visualizam a lista de pontos
- **Pessoas:** cadastram o material que será descartado, escolhem o ponto de coleta e registram o descarte
- Armazenamento em banco de dados SQLite

## Criptografia

Os algoritmos foram implementados em Python, sem bibliotecas prontas:

- **Senha:** Cifra de César adaptada para a faixa ASCII 32–126, combinada em camadas com XOR
- **CPF:** versão da Cifra de César adaptada para números

## Tecnologias

- Python 3
- SQLite (`sqlite3`)