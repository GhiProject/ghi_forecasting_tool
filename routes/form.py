from flask_app import app
from flask import render_template, request, jsonify, g
#import gspread
#from oauth2client.service_account import ServiceAccountCredentials
from db import *
import pprint

pp = pprint.PrettyPrinter()

@app.route("/form")
def form():
    method = request.args.get("method")

    ###
    ### Initial page, no parameters
    ###
    if method is None:
        return render_template("form.html", showthediv=0)

    ###
    ### Modified page, retrieve method values from parameters
    ###
    else:
        #method  = str(method.decode("utf-8"))
        year    = request.args.get("year", type=int)
        country = request.args.get("country")
        disease = request.args.get("disease")
        company = request.args.get("company")
        drug    = request.args.get("drug")

        country_row = request.args.get("country_row", type=int)
        country_col = request.args.get("country_col", type=int)
        #pp.pprint("company name = " + company);
        ## Authorize credentials
        #scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        #creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
        #client = gspread.authorize(creds)

        ## Open spreadsheet to corresponding year
        #if year == 2010:
        #    spreadsheet = client.open("ORS Global Burden of Disease 2013 (2010/2013)")
        #elif year == 2013:
        #    spreadsheet = client.open("ORS Global Burden of Disease 2015 (2010/2015)")
        #elif year == 2015:
        #    spreadsheet = client.open("ORS Global Burden of Disease 2015 (2010/2015)")

        ### Retrieve corresponding JSON data  ###

        # Retrieve countries
        if method == "getCountries":
            g.db = connect_db()
            if year == 2010:
             data = g.db.execute('select country from country2010')
            elif year == 2013:
             data = g.db.execute('select country from country2013')
            elif year == 2015:
             data = g.db.execute('select country from country2015')
            country_cells = data.fetchall()
            pp.pprint(country_cells)
            return jsonify(
                countries=[
                    {
                        "country": country_cell[0]
                    }
                    for country_cell in country_cells
                ]
            )


        # Retrieve diseases
        if method == "getDiseases":
            # worksheet = spreadsheet.worksheet("DALY")
            # disease_cells = worksheet.range(country_row, country_col+1, country_row, country_col+1+9)
            g.db = connect_db()
            if year == 2010:
                data = g.db.execute('select disease from disbars')
            elif year == 2013:
                data = g.db.execute('select disease from disbars')
            elif year == 2015:
                data = g.db.execute('select disease from disbars2010B2015')
            disease_cells = data.fetchall()
            # pp.pprint(disease_cells)
            return jsonify(
                diseases=[
                    {
                        "disease": disease_cell[0]
                    }
                    for disease_cell in disease_cells
                ]
            )


        # Retrieve companies
        if method == "getCompanies":
            # worksheet = spreadsheet.worksheet("Company")
            # TODO fill out the rest of this block, populating company_cells and formatting JSON
            g.db = connect_db()
            pp.pprint('Inside Company')
            if year == 2010:
                data = g.db.execute('select distinct company from drugr2010 where lower(company) not like "%unmet need%"')
            elif year == 2013:
                data = g.db.execute(''' select distinct company from drugr2013 where lower(company) not like '%unmet need%' ''')
            elif year == 2015:
                data = g.db.execute('''select distinct company from drugr2015 where lower(company) not like '%unmet need%' ''')
            company_cells = data.fetchall()
            pp.pprint(company_cells)
            return jsonify(
                companies=[
                    {
                        "company": company_cell[0]
                    }
                    for company_cell in company_cells
                ]
            )


        # Retrieve drugs
        if method == "getDrugs":
            # worksheet = spreadsheet.worksheet("Company")
            # TODO fill out the rest of this block, populating drug_cells and formatting JSON
            g.db = connect_db()
            pp.pprint(company)
            if year == 2010:
                data = g.db.execute(
                    'select drug from drugr2010 where company = ?',
                (company,))
            elif year == 2013:
                data = g.db.execute('select drug from drugr2013 where company = ?',
                (company,))
            elif year == 2015:
                data = g.db.execute('select drug from drugr2015 where company = ?',
                (company,))
            drug_cells = data.fetchall()
            pp.pprint(drug_cells)
            return jsonify(
                drugs=[
                    {
                        "drug": drug_cell[0]
                    }
                    for drug_cell in drug_cells
                ]
            )


    #TODO Return error status if method name is not matched
    return