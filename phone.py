import json
from flask import Flask
from flask import session, redirect, url_for, request
from flask import render_template
from markupsafe import escape

app = Flask(__name__)

app.secret_key = b'03a2303adadccae00eb7ea3127c9c670b2fa83a4c0885ecdb1ef9b632e8a600'

app_name = "Smartphone Store"

inventory_file = "inventory-data.json"
inventory_page = "inventory-page-tmpl.html"

def load_cart_data(file):
    with open(file, "r") as fileobj:
        return json.load(fileobj)
    
def save_cart_data(invobj,file):
    with open(file, "w") as fileobj:
        return json.dump(invobj,fileobj,indent = 4)

def update_cart_from_inventory_req(inv_dict,prev_cart_dict, reqobj):
    upated_cart_dict = prev_cart_dict.copy()
    if len(reqobj.args) > 1:
        for param_name in reqobj.args:
            if (param_name != "account") and (param_name in inv_dict):
                prod_id = param_name

                try:
                    qty= int(reqobj.args[prod_id])
                    if 0 <= qty <= inv_dict[prod_id][2]:
                        upated_cart_dict[prod_id]
                    else:
                        pass

                except KeyError:
                    pass
                except ValueError:
                    pass

    return upated_cart_dict

def cart_total(cart_dict, inv_dict):
    return sum(inv_dict[prod_id][1] * cart_dict[prod_id] for prod_id in cart_dict)


@app.route('/emptycart/<account>',methods=['GET'])
def empty_cart(account):
    session.pop(account,"")

    all_data = load_cart_data(inventory_file)
    carts_dict = all_data["carts"]
    carts_dict.pop(account, None)

    save_cart_data(all_data, inventory_file)

    inv_url = url_for("format_inventory")

    return"""
    <!Doctype html>
    <html>
        <head>
            <title>""" + app_name + """</title>
        </head>
        <body>
            <h2>""" + app_name + """</h2>
            <p>""" + account + """</p>
            <p>Check out the <a href=""" + inv_url+ """> Inventory</a></p>
        </body>
    </html>
"""

@app.route('/',methods = ['GET','POST'])
def format_inventory():

    account_name = request.args.get("account", "")

    if not account_name:
        account_name = session.get("account","default")

    session["account"] = account_name

    all_data_dict = load_cart_data(inventory_file)

    inventory_data = all_data_dict["inventory"]
    cart_data = all_data_dict["carts"]

    prev_buyer_cart = cart_data.get(account_name,dict())

    revised_cart_data = update_cart_from_inventory_req(inventory_data,prev_buyer_cart,request)

    cart_data[account_name] = revised_cart_data

    save_cart_data(all_data_dict,inventory_file)

    cart_total_price = cart_total(revised_cart_data,inventory_data)

    emptycart_url = url_for("empty_cart", account=account_name)

    html_reply = render_template(inventory_page,application_name = app_name, inv_data = inventory_data,
                                 account_name = account_name, cart_data = revised_cart_data, cart_price = cart_total_price
                                , emptycarturl = emptycart_url)

    return html_reply