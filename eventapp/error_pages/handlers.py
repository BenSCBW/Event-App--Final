from flask import Blueprint,render_template

error_pages = Blueprint('error_pages',__name__)

@error_pages.app_errorhandler(404) #spajanje "našeg" napravljenog errora s error 404
def error_404(error):

    return render_template('error_pages/404.html'), 404 #Kada dođe do errora, otvorit ce se error stranica koju  smo mi napravili

@error_pages.app_errorhandler(403)
def error_403(error):
    #error 403(neovlašten pristup- update tudjeg bloga)

    return render_template('error_pages/403.html'), 403
