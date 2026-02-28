
# NEXA - Assistente Local com Ollama
<img src="https://img.shields.io/badge/Nexa-Assistant-blue" />
<img src="https://img.shields.io/badge/Python-3.8%252B-green" />
<img src="https://img.shields.io/badge/Ollama-Llama3%253A8b-orange" />
<img src="https://img.shields.io/badge/CustomTkinter-GUI-purple" />

chatbot que roda localmente sem API nem TOKENS
Criei algumas emoções me inspirando no BMO de Hora da Aventura
usei o Ollama3 na versão llama3:8b por ser a mais em conta (de processamento) 

### Pré-requisitos:
Python 3.8 ou superior
Ollama instalado
Modelo Llama 3 (8B) baixado via Ollama

### Instalação:
git clone https://github.com/MatheusRibeiro0999/nexa.git
cd nexa
pip install customtkinter pillow ollama 

### Instale o Ollama (se não tiver)
### Acesse https://ollama.ai/

### Baixe o modelo Llama 3
ollama pull llama3:8b

### estrutura do projeto:
nexa/
│
├── main.py              # Ponto de entrada
├── ui.py                 # Interface gráfica e animações
├── chat_engine.py        # Integração com Ollama
├── assets/               # Animações do robô
│   ├── idle/            # Frames do estado inativo
│   ├── speaking/        # Frames falando
│   ├── listening/       # Frames ouvindo
│   ├── thinking/        # Frames pensando
│   └── error/           # Frames de erro
│
└── README.md


### 📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

### 🙏 Agradecimentos
Ollama - Pelo excelente gerenciamento de modelos locais
CustomTkinter - Pela biblioteca de interface moderna
Llama 3 - Pelo modelo de linguagem

### 📧 Contato
Desenvolvedor: Matheus Ribeiro
Email: ribeiro.amrs@gmail.com
GitHub: MatheusRibeiro0999

### ⭐ Se gostou do projeto, não esqueça de dar uma estrela!
