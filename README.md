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

1. Abrir link: https://sistema1.planalto.gov.br/secomweb2/demanda/execucaocontratual
2. Escolher "veiculação", máximo período possível e preencher captcha
3. Clicar em "gerar arquivo excel"
4. Esperar, esperar, esperar...
4. Baixar substituindo o arquivo `Planilha_Exportacao.xlsx` antigo
5. Remova o arquivo `planilha.hdf`
6. Regere o site com: `python congelar.py`
