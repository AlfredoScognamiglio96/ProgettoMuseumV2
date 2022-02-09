import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, abort, request
from MuseumProject import app,db
from MuseumProject.forms import LoginForm, UpdateAccountForm, PostForm
from MuseumProject.models import Administrator, Post
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        admin = Administrator.query.filter_by(email=form.email.data).first()                         #Query login
        if admin and Administrator.query.filter_by(password=form.password.data).first():
            login_user(admin)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

#Funzione per salvare l immagine del profilo
def save_profile_image(form_profile_image):
    #random_hex = secrets.token_hex(8)
    file_extension = os.path.join(form_profile_image.filename)
    profile_image_fn = file_extension  #random_hex +
#Tramite il join utilizzo il percorso fino alla radice dove viene recuperata l immagine
    profile_image_path = os.path.join(app.root_path, 'static/images', profile_image_fn)
    output_size = (125,125)
    i = Image.open(form_profile_image)
    i.thumbnail(output_size)
    i.save(profile_image_path)
    return  profile_image_fn

#Funzione per salvare l immagine del post
def save_post_image(form_post_image):
    file_extension = os.path.join(form_post_image.filename)
    post_image_fn = file_extension
    post_image_path = os.path.join(app.root_path, 'static/images', post_image_fn)
    output_size = (500,500)
    k = Image.open(form_post_image)
    k.thumbnail(output_size)
    k.save(post_image_path)
    return post_image_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required                                                         #Per accedere a questa route dobbiamo essere prima loggati
def account():
    form = UpdateAccountForm()                                          #Istanza del form
    if form.validate_on_submit():                                       #If che parte dopo la validazione corretta
        if form.profile_image.data:
             picture_file = save_profile_image(form.profile_image.data)
             current_user.image_file = picture_file
        db.session.commit()
        flash('Immagine profilo aggiornata!', 'success')
        return redirect(url_for('account'))
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.profile_post.data:
            picture_post = save_post_image(form.profile_post.data)
            current_user.post_image = picture_post
        post = Post(title=form.title.data, descrizione=form.descrizione.data,post_image=form.profile_post.data.filename, admin_id=current_user.get_id())            #modifica effettuata qui
        db.session.add(post)
        db.session.commit()
        flash('Post creato!', 'success')
        return redirect(url_for('home'))
    id = current_user.get_id()                                          #modifica effettuata qui
    #admin_logged = Administrator.query.filter_by(id=id).first()
    post_user = Post.query.filter_by(id=id).first()                     #modifica effettuata qui
    print(id)
    print(post_user.post_image)
    post_image = url_for('static', filename='images/' + post_user.post_image)
    return render_template('create_post.html', title='New Post', post_image=post_image, form=form, legend='New Post')

#Route che gestisce l inserimento dell id del post all interno della route stessa
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)                                    #Se il post con l id ricercato non esiste viene fornito la pagina d errore
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.poster != current_user:
        abort(403)                                                          #403 è la risposta http per un percorso proibito
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.descrizione = form.descrizione.data
        post.image_post = form.profile_post.data
        db.session.commit()
        flash('Post aggiornato!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
         form.title.data = post.title
         form.descrizione.data = post.descrizione
         form.profile_post.data = post.image_post
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

#Route con cui vengono eliminati solo i post dell utente loggato nella sessione
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.poster != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post eliminato!', 'success')
    return redirect(url_for('home'))


#Route per mostrare tutti i post di un singolo admin
@app.route("/user/<string:first_name>")
def admin_posts(first_name):
    admin = Administrator.query.filter_by(first_name=first_name).first_or_404()
    posts = Post.query.filter_by(poster=admin)
    return render_template('admin_posts.html', posts=posts, admin=admin)