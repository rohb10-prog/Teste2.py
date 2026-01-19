# 💰 Dashboard de Contas a Receber

Dashboard interativo para visualização e análise de contas a receber, desenvolvido com Streamlit e Plotly.

## 🚀 Demonstração

Acesse o dashboard online: [ADICIONE O LINK DO STREAMLIT AQUI]

## 📊 Funcionalidades

- **Gráfico de Barras Empilhadas**: Visualização clara dos valores por pagador e data
- **Filtros Interativos**:
  - Status de pagamento (Todos/Pendentes/Pagos)
  - Período personalizado ou predefinido (Hoje, 7 dias, 30 dias, Tudo)
- **Métricas em Tempo Real**:
  - Valor total
  - Quantidade de registros
  - Valor médio
- **Navegação Temporal**: Botões rápidos (Dia, Semana, Mês, 3 Meses, Tudo)
- **Tooltips Unificados**: Visualize o total do dia ao passar o mouse
- **Tabela Detalhada**: Lista completa com todos os registros filtrados
- **Atualização Automática**: Cache de 5 minutos para otimizar performance

## 🛠️ Tecnologias

- **Python 3.8+**
- **Streamlit**: Framework para dashboards interativos
- **Plotly**: Gráficos interativos e modernos
- **Pandas**: Manipulação e análise de dados

## 📦 Instalação Local

1. Clone o repositório:
```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o dashboard:
```bash
streamlit run app.py
```

4. Acesse no navegador: `http://localhost:8501`

## 🌐 Deploy no Streamlit Cloud

1. Faça fork deste repositório
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte sua conta do GitHub
4. Selecione o repositório e o arquivo `app.py`
5. Clique em "Deploy"

## 📁 Estrutura do Projeto

```
.
├── app.py              # Código principal do dashboard
├── requirements.txt    # Dependências do projeto
└── README.md          # Documentação
```

## 🔧 Configuração

O dashboard está configurado para ler dados de uma planilha do Google Sheets pública. Para usar sua própria planilha:

1. Abra o arquivo `app.py`
2. Localize a variável `SHEET_ID` na função `carregar_dados()`
3. Substitua pelo ID da sua planilha
4. Certifique-se de que a planilha está pública ou configurada para "Qualquer pessoa com o link pode visualizar"

### Formato da Planilha

A planilha deve conter as seguintes colunas:
- **Vencimento**: Data de vencimento (formato DD/MM/AAAA)
- **Valor**: Valor monetário (pode ser texto formatado como "R$ 1.000,00")
- **Pagador**: Nome do cliente/pagador
- **Pago** (opcional): Status do pagamento (TRUE/FALSE, SIM/NÃO, PAGO/PENDENTE)

## 📸 Screenshots

[Adicione screenshots do seu dashboard aqui]

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 👤 Autor

Seu Nome
- GitHub: [@seu_usuario](https://github.com/seu_usuario)

## 🙏 Agradecimentos

- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/)
- [Pandas](https://pandas.pydata.org/)
