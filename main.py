import datetime
import os
import re
import sqlalchemy.exc
from flask import Flask, make_response
from flask import render_template, url_for, request, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    material = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    insert_material = db.Column(db.String(100))
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200))
    path_photos = db.Column(db.String(200))

    def __repr__(self):
        return self.name


class RingSizes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Ring_Id = db.Column(db.Integer, nullable=False)
    Size = db.Column(db.String(20), nullable=False)
    Count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return str(self.Ring_Id)


class ShoppingCart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    RingSizes_Id = db.Column(db.Integer, nullable=False)
    date_adding = db.Column(db.DateTime)
    Client_Id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return str(self.id)


class Clients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    Role_Id = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return self.id


@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    if request.cookies.get('theme') == 'dark':
        theme = "/css/1dark.css"
    else:
        theme = "/css/1.css"
    clientCookie = request.cookies.get('Client')
    if clientCookie is None:
        role = 0
    else:
        role = db.session.query(Clients).filter(Clients.login == clientCookie).first().Role_Id
    return render_template('index.html', title='Home', theme=theme, role=role)


@app.route('/About')
def About():
    if request.cookies.get('theme') == 'dark':
        theme = "/css/3dark.css"
    else:
        theme = "/css/3.css"
    clientCookie = request.cookies.get('Client')
    if clientCookie is None:
        role = 0
    else:
        role = db.session.query(Clients).filter(Clients.login == clientCookie).first().Role_Id
    return render_template('About.html', theme=theme, role=role)


@app.route('/Catalog')
def Catalog():
    if request.cookies.get('theme') == 'dark':
        theme = "/css/CatalogDark.css"
    else:
        theme = "/css/Catalog.css"
    clientCookie = request.cookies.get('Client')
    if clientCookie is None:
        role = 0
    else:
        role = db.session.query(Clients).filter(Clients.login == clientCookie).first().Role_Id
    items = Items.query.order_by(Items.price).all()

    return render_template('Catalog.html', theme=theme, items=items, role=role)


@app.route('/rings/<int:id>', methods=['GET', 'POST'])
def rings(id):
    if request.cookies.get('theme') == 'dark':
        theme = "/css/kolco1dark.css"
    else:
        theme = "/css/kolco1.css"
    if request.method == 'POST':
        size = request.form.get('sizeRing')

        clientCookie = request.cookies.get('Client')
        if clientCookie is not None:
            client = db.session.query(Clients).filter(Clients.login == clientCookie).first()
            if client.Role_Id == 1:
                RingSizes_Id = db.session.query(RingSizes).filter(RingSizes.Ring_Id == id). \
                    filter(RingSizes.Size == size).first().id
                item = ShoppingCart(RingSizes_Id=RingSizes_Id, date_adding=datetime.datetime.now(), Client_Id=client.id)
                if len(db.session.query(ShoppingCart).filter(ShoppingCart.Client_Id == client.id).
                               filter(ShoppingCart.RingSizes_Id == RingSizes_Id).all()) == 0:
                    db.session.add(item)
                    db.session.commit()
                return redirect(url_for('korzina'))
    else:
        ring = db.session.query(Items).filter(Items.id == id).first()
        photos = os.listdir(os.curdir + url_for('static', filename=ring.path_photos))
        sizes = []
        for size in db.session.query(RingSizes).filter(RingSizes.Ring_Id == id).filter(RingSizes.Count > 0).all():
            sizes.append(size.Size)
        clientCookie = request.cookies.get('Client')
        if clientCookie is None:
            role = 0
        else:
            role = db.session.query(Clients).filter(Clients.login == clientCookie).first().Role_Id
    return render_template('rings.html', theme=theme, ring=ring,
                               photos=photos, sizes=sizes, countSizes=len(sizes), role=role)


@app.route('/korzina', methods=['GET', 'POST'])
def korzina():
    if request.cookies.get('theme') == 'dark':
        theme = "css/korzinadark.css"
    else:
        theme = "css/korzina.css"
    if request.method == 'POST':
        idRing = request.form['idRing']
        db.session.delete(db.session.query(ShoppingCart).filter(ShoppingCart.id == idRing).one())
        db.session.commit()
    dict = {}
    sumPriceRing = 0
    clientCookie = request.cookies.get('Client')
    if clientCookie is None:
        role = 0
    else:
        role = db.session.query(Clients).filter(Clients.login == clientCookie).first().Role_Id
        items = ShoppingCart.query.\
            filter(ShoppingCart.Client_Id == db.session.query(Clients).filter(Clients.login == clientCookie).first()
                   .id).order_by(ShoppingCart.date_adding).all()
        for item in items:
            rg = db.session.query(RingSizes).filter(RingSizes.id == item.RingSizes_Id).first()
            if rg.Count > 0:
                dict.update({rg: [db.session.query(Items).filter(Items.id == rg.Ring_Id).first(), item.id]})
        for ring in dict.values():
            sumPriceRing += ring[0].price
    return render_template('korzina.html', theme=theme, data=dict, sum=sumPriceRing, role=role)


@app.route('/purchase', methods=['POST'])
def PayShoppingCart():
    clientCookie = request.cookies.get('Client')
    if clientCookie is None:
        return redirect(url_for('Catalog'))
    items = ShoppingCart.query. \
        filter(ShoppingCart.Client_Id == db.session.query(Clients).filter(Clients.login == clientCookie).first()
               .id).order_by(ShoppingCart.date_adding).all()
    for item in items:
        rg = db.session.query(RingSizes).filter(RingSizes.id == item.RingSizes_Id).first()
        count = rg.Count - 1
        rg.Count = count
        if rg.Count == 0:
            db.session.query(ShoppingCart).filter(ShoppingCart.RingSizes_Id == rg.id).delete()
        db.session.commit()
    db.session.query(ShoppingCart).filter(ShoppingCart.Client_Id == db.session.query(Clients)
                                          .filter(Clients.login == clientCookie).first().id).delete()
    db.session.commit()
    return redirect(url_for('korzina'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.cookies.get('theme') == 'dark':
        theme = "css/registrationdark.css"
    else:
        theme = "css/registration.css"
    if request.method == 'POST':
        phone = request.form['tel']
        email = request.form['log']
        password = request.form['pas']
        isNotPhoneNumber = not re.fullmatch("^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$", phone)
        isSmallPassword = len(password) < 6
        Client = Clients(login=email, password=password, Role_Id=1, phone=phone)
        if isSmallPassword or isNotPhoneNumber:
            if request.cookies.get('theme') == 'dark':
                theme = "css/registrationdark.css"
            else:
                theme = "css/registration.css"
            return render_template('registration.html',
                                   isSmallPassword=isSmallPassword, isNotPhoneNumber=isNotPhoneNumber, inputData=Client,  theme=theme)
        try:
            db.session.add(Client)
            db.session.commit()
            return redirect(url_for('login'))
        except sqlalchemy.exc.IntegrityError:
            return render_template('registration.html', isRepeatEmail=True, inputData=Client)
    else:
        clientCookie = request.cookies.get('Client')
        if clientCookie is not None:
            return redirect(url_for('index'))
        return render_template('registration.html', inputData=Clients(login="", password="", Role_Id=0, phone=""),  theme=theme)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.cookies.get('theme') == 'dark':
        theme = "/css/logindark.css"
    else:
        theme = "/css/login.css"
    if request.method == 'POST':
        email = request.form['log']
        password = request.form['pas']

        if len(db.session.query(Clients).filter(Clients.login == email).all()) == 0:
            if request.cookies.get('theme') == 'dark':
                theme = "/css/logindark.css"
            else:
                theme = "/css/login.css"
            return render_template('login.html', isNewEmail=True,
                                   inputData=Clients(login="", password=password, Role_Id=0, phone=""), theme=theme)
        if len(db.session.query(Clients).filter(Clients.login == email)
                       .filter(Clients.password == password).all()) == 0:
            if request.cookies.get('theme') == 'dark':
                theme = "/css/logindark.css"
            else:
                theme = "/css/login.css"
            return render_template('login.html', isIncorrectPassword=True,
                                   inputData=Clients(login=login, password="", Role_Id=0, phone=""), theme=theme)
        client = db.session.query(Clients).filter(Clients.login == email).first()
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('Client', client.login)
        return resp
    else:
        clientCookie = request.cookies.get('Client')
        if clientCookie is not None:
            return redirect(url_for('index'))
        return render_template('login.html', inputData=Clients(login="", password="", Role_Id=0, phone=""), theme=theme)


@app.route('/logout')
def logout():
    resp = make_response(redirect(request.referrer))
    resp.delete_cookie('Client')
    return resp


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
