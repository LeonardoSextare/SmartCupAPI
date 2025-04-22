# 🥤 SmartCup API

API central do projeto **SmartCup**, parte do Trabalho de Graduação em Analise e Desenvolvimento na **Fatec Jales**.  
Esta API possui toda a logica e regra de negocio do sistema além de conectar o front-end à máquina protótipo de bebidas inteligentes.

---

## ✨ Visão Geral

- 🔗 **Integração central** entre o aplicativo web/mobile e a máquina física de bebidas.
- 🧑‍💼 Gerenciamento de clientes, copos inteligentes (NFC), máquinas, bebidas, operações de consumo e administradores.
- 📦 Estrutura robusta com FastAPI, PostgreSQL e Supabase.

---

## 🚀 Tecnologias Utilizadas

| Tecnologia    | Versão Recomendada |
| ------------- | ------------------ |
| Python        | 3.11+              |
| FastAPI       | 0.110+             |
| Uvicorn       | 0.29+              |
| psycopg2      | 2.9+               |
| python-dotenv | 1.0+               |
| Supabase      | -                  |
| PostgreSQL    | 15+                |

---

## ⚙️ Instalação e Execução

1. **Clone o repositório:**

   ```sh
   git clone <url-do-repositorio>
   cd SmartCupAPI
   ```

2. **Crie e ative um ambiente virtual:**

   ```sh
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # ou
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Instale as dependências:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Configure o arquivo `.env`:**

   ```
   SUPABASE_URL=...
   SUPABASE_ANON_KEY=...
   ```

5. **Configure o banco de dados:**

   - Execute os scripts SQL em `scripts/` no seu PostgreSQL.

6. **Inicie a API:**

   ```sh
   uvicorn app.main:app --reload
   ```

7. **Acesse a documentação interativa:**
   [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📚 Endpoints Principais

- `/administrador` – Administradores do sistema
- `/bebida` – Bebidas disponíveis
- `/cliente` – Clientes cadastrados
- `/copo` – Copos inteligentes (NFC)
- `/maquina` – Máquinas de bebidas
- `/operacao` – Operações de consumo

Consulte a documentação Swagger para detalhes de cada rota.

---

## 📄 Licença

MIT License. Veja o arquivo [`LICENSE`](LICENSE).
