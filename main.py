#!/usr/bin/env python3
# coding: utf-8

import json
import locale
from flask import Flask, render_template, url_for, Markup, send_from_directory
import processador as pr
import sinonimos


locale.setlocale(locale.LC_ALL, '')
app = Flask(__name__, static_url_path='')
app.jinja_env.line_statement_prefix = '#'
app.config['TEMPLATES_AUTO_RELOAD'] = True


df = pr.abrir_planilha()


@app.template_filter('sep_float')
def sep_float(f):
    return locale.format("%.2f", f, grouping=True)


@app.template_global('aviso_grupos')
def aviso_grupos():
    return Markup('<a href="%s">Alguns fornecedores' % url_for('grupos') +
                  ' foram agrupados conforme' +
                  ' listado nessa outra página.</a>')


@app.route('/<path:path>')
def arquivos(path):
    return send_from_directory('static', path)


@app.template_filter('paginas')
def paginas(atual):
    return [(link, nome, link == atual) for link, nome in [
        ('totais', 'Totais'),
        ('maiores', 'Maiores'),
        ('grupos', 'Grupos'),
    ]]


@app.route("/")
def sobre():
    return render_template('sobre.html')


@app.route("/maiores/")
def maiores():
    n = 20
    return render_template(
        'maiores.html',
        pagina_atual='maiores',
        n_maiores=n,
        dados_ano=json.dumps(pr.serializar_categorias(
            pr.total_por_maiores_fornecedores_globais_por_data(df, 'Ano', n),
            'Ano')),
        dados_mes=json.dumps(pr.serializar_categorias(
            pr.total_por_maiores_fornecedores_globais_por_data(df, 'Mês', n),
            'Mês')),
    )


@app.route("/grupos/")
def grupos():
    return render_template(
        'grupos.html',
        pagina_atual='grupos',
        grupos=sorted([(a, sorted(r)) for a, r in sinonimos.apelidos.items()]),
        nao_agrupados=sorted(
            [f.strip()
             for f in df.Fornecedor.drop_duplicates().tolist()
             if f not in sinonimos.apelidos]))


@app.route("/totais/")
def totais():
    return render_template(
        'totais.html',
        pagina_atual='totais',
        dados=json.dumps(pr.analises_por_data(df, 'Ano')),
        datas=pr.listar_datas(df, 'Mês'),
        fornecedores=pr.total_por_fornecedor(df).to_dict('split')['data'])


if __name__ == "__main__":
    import os
    from os import path

    extra_dirs = ['templates']
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in os.walk(extra_dir):
            for filename in files:
                filename = path.join(dirname, filename)
                if path.isfile(filename):
                    extra_files.append(filename)
    app.run(debug=True, extra_files=extra_files)
