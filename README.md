# Pagamentos Secom

Visualizações de pagamentos feitos pela Secretaria de Comunicação Social da Presidência da República (SECOM).

https://andresmrm.github.io/pagamentos-secom/

# Rodando localmente

Clone esse repositório e, assumindo que você tem `virtualenv` instalado, faça:

    virtualenv env
    . env/bin/activate
    pip install -r requirements.txt
    python main.py
  
Para gerar uma versão estática do site faça:

    python congelar.py

# Atualizando os dados

1. Baixe a planilha do site da SECOM substituindo o arquivo `Planilha_Exportacao.xlsx` antigo
2. Remova o arquivo `planilha.hdf`
3. Regere o site com: `python congelar.py`
