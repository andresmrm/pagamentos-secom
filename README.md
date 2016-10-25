# Pagamentos Secom

Visualizações de pagamentos feitos pela Secretaria de Comunicação Social da Presidência da República (SECOM).

# Rodando localmente

Clone esse repositório e, assumindo que você tem `virtualenv` instalado, faça:

    virtualenv env
    . env/bin/activate
    pip install -r requirements.txt
    python main.py
  
Para gerar uma versão estática do site faça:

    python congelar.py
