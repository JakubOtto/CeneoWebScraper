from app import app
from flask import render_template, request, redirect, url_for, send_file, send_from_directory
import os
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from app.utils import extract_tag, selectors
from IPython.display import HTML
from urllib.parse import quote
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt
import io
import base64
import numpy as np

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/extraction', methods=['POST','GET'])
def extraction():
    if request.method == 'POST':
        product_code= request.form.get('product_code')
        url = f'https://www.ceneo.pl/{product_code}#tab=reviews'
        all_opinions = []

        while(url):
            print(url)
            response = requests.get(url)
            page_dom = BeautifulSoup(response.text, "html.parser")
            opinions = page_dom.select("div.js_product-review")

            product_name = page_dom.select_one('h1')
            
            
            for opinion in opinions:
                single_opinion={}
                for key, value in selectors.items():
                    single_opinion[key] = extract_tag(opinion, *value)
                single_opinion['Nazwa'] = product_name.get_text()
                single_opinion['Kod Produktu'] = product_code
                all_opinions.append(single_opinion)
            try:
                url='https://www.ceneo.pl' + extract_tag(page_dom, "a.pagination__next", "href")
                with open(f"./app/data/opinions/{product_code}.json", "w", encoding="UTF-8") as jf:
                    json.dump(all_opinions, jf, indent=4, ensure_ascii=False)
                df = pd.DataFrame(all_opinions)
                df.to_excel(f"./app/data/opinions/{product_code}.xlsx", index=False)
                df.to_csv(f"./app/data/opinions/{product_code}.csv", index=False)
                
                return redirect(url_for('productsite',product_code=product_code))
                
            except TypeError:
                url=None
                error_message="Wpisano błędny kod artykułu, spróbuj ponownie."
                return render_template("extraction.html", error_message=error_message)
            
        
        
    return render_template("extraction.html")

@app.route('/productlist', methods=['POST','GET'])
def productlist():
    folder_path = "./app/data/opinions/"
    file_names = os.listdir(folder_path)
    allproducts= []
    for i in file_names:
        if i.split('.')[1]=='xlsx'or i.split('.')[1]=='csv':
            continue
        full_path = os.path.join(folder_path, i)
        with open(full_path, 'r', encoding='utf-8') as f:
            fcontent = json.load(f)
            totalcon=0
            totalpros=0
            ocenad=0
            total=len(fcontent)
            single={}
            for j in fcontent:
                ocena = float(j['Ocena'].split('/')[0].replace(',', '.'))
                ocenad += ocena
                totalcon += len(j['Wady'])
                totalpros += len(j['Zalety'])
                single = {
                    'Nazwa': f'<a href="/productsite/{quote(j["Kod Produktu"])}">{j["Nazwa"]}</a>',
                    'Liczba Wad': totalcon,
                    'Liczba Zalet': totalpros,
                    'Liczba opinii': total,
                    'Srednia ocena': ocenad / total,
                    'Kod': j['Kod Produktu'],
                    'Pobierz JSON': f'<a href="/download/{quote(j["Kod Produktu"])}.json"><button type="button" class="btn btn-secondary" style="margin-top: 10px;">Pobierz JSON</button></a>',
                    'Pobierz XLSX': f'<a href="/download/{quote(j["Kod Produktu"])}.xlsx"><button type="button" class="btn btn-secondary" style="margin-top: 10px;">Pobierz XLSX</button></a>',
                    'Pobierz CSV': f'<a href="/download/{quote(j["Kod Produktu"])}.csv"><button type="button" class="btn btn-secondary" style="margin-top: 10px;">Pobierz CSV</button></a>'
                }
            allproducts.append(single)
    df=pd.DataFrame(allproducts)
    df=df.drop('Kod',axis=1)
    
    return render_template("productlist.html", productlist=df.to_html(header=1, classes='table table-bordered table-striped text-center', table_id='productlist', escape=False))

@app.route('/productsite/<product_code>')
def productsite(product_code):
    opinions = pd.read_json(f"./app/data/opinions/{product_code}.json")
    opinions = opinions.drop('Nazwa', axis=1)
    opinions = opinions.drop('Kod Produktu', axis=1)
    for i in range(len(opinions)):
        if len(opinions.loc[i, "Zalety"]) == 0:
            opinions.loc[i, "Zalety"] = "Brak danych"
        else:
            opinions.loc[i,"Zalety"] ="-"+" -".join(opinions.loc[i, "Zalety"])
        if len(opinions.loc[i, "Wady"]) == 0:
            opinions.loc[i, "Wady"] = "Brak danych"
        else:
            opinions.loc[i,"Wady"] ="-"+" -".join(opinions.loc[i, "Wady"])
    
        
    return render_template("productsite.html", product_code=product_code, opinions=opinions.to_html(header=1, classes='table table-striped table-success', table_id='products'))

@app.route('/charts/<product_code>')
def charts(product_code):
    
    opinions = pd.read_json(f"./app/data/opinions/{product_code}.json")
    opinions.Ocena = opinions.Ocena.map(lambda x: float(x.split("/")[0].replace(",",".")))
    opinions_count = opinions.shape[0]
    pros_count = opinions.Zalety.map(bool).sum()
    cons_count = opinions.Wady.map(bool).sum()
    avg_rating = opinions.Ocena.mean()
    ratings = opinions.Ocena.value_counts().reindex(list(np.arange(0,5.5,0.5)),fill_value = 0)
    
    try:
        plt.close(fig1)
        plt.close(fig2)
    except:
        pass

    fig1, ax1 = plt.subplots()
    chart1 = ratings.plot.bar(ax=ax1)
    chart1.set_xlabel('Ocena')
    chart1.set_ylabel('Liczba opinii')
    chart1.set_title('Rozkład ocen')

    chart1_base64= io.BytesIO()
    plt.savefig(chart1_base64,format='png')
    plt.close(fig1)
    chart1_base64.seek(0)
    chart1_base64_encoded = base64.b64encode(chart1_base64.getvalue()).decode('utf-8')
    chart1_base64.close()

    fig2, ax2 = plt.subplots()
    chart2 = opinions.Polecenie.value_counts(dropna=False).plot.pie(label="", autopct="%1.1f%%", ax=ax2)
    chart2.set_title("Rekomendacje")

    chart2_base64= io.BytesIO()
    plt.savefig(chart2_base64,format='png')
    plt.close(fig2)
    chart2_base64.seek(0)
    chart2_base64_encoded = base64.b64encode(chart2_base64.getvalue()).decode('utf-8')
    chart2_base64.close()


    return render_template("charts.html", product_code=product_code, chart1_base64=chart1_base64_encoded, chart2_base64=chart2_base64_encoded)
@app.route('/author')
def author():
    return render_template("author.html")

@app.route('/download/<filename>')
def download(filename):
    directory = './app/data/opinions/'
    file_path = os.path.abspath(os.path.join(directory, filename))
    return send_file(file_path, as_attachment=True)