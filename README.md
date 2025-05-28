# SmartCup API

**API desenvolvida com FastAPI (Python) para comunicação e gerenciamento dos dados do projeto SmartCup.**

## 📌 Sobre o Projeto

A **SmartCup API** é parte fundamental do sistema de dispenser inteligente de líquidos, sendo responsável pela integração entre o protótipo Arduino, a interface de usuário (frontend) e o armazenamento inteligente dos dados gerados pela utilização do sistema.

A API gerencia validações de clientes através dos codigos NFC lidos pelo prototipo, registros de transações, controle de saldos e aplicação das diversas regras de negócio definidas no projeto.

## ⚙️ Funcionalidades

- Validação e autenticação de usuários/clientes.
- Gerenciamento de transações e histórico de consumo.
- Aplicação automática de regras de negócios e gestão de saldos.
- Coleta, processamento e armazenamento de dados operacionais.

## 🛠️ Tecnologias utilizadas

- Python
- FastAPI
- Postgress via Supabase

## 📡 Integração

Esta API conecta-se diretamente com:
- Protótipo Arduino: [SmartCup_Arduino](https://github.com/LeonardoSextare/SmartCup_Prototipo).
- Front-end [SmartCup-FrontEnd-React](https://github.com/PedroHVL14/SmartCup-FrontEnd-React).

## 📃 Licença

Este projeto é licenciado sob a licença **MIT** – consulte o arquivo [LICENSE](LICENSE) para obter detalhes.
