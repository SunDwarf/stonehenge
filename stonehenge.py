from flask import Flask, request, render_template
app = Flask(__name__)

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

import config

Base = automap_base()
engine = create_engine(config.pgsql["string"])
Base.prepare(engine, reflect=True)
Posts = Base.classes.posts
session = Session(engine)

from shdecoders import *
from shinfo import *

def getbyid(post_id):
	post=session.query(Posts).filter_by(id=post_id).first()
	return post
	
def getbyshortcode(post_shortcode):
	post=session.query(Posts).filter_by(shortcode=post_shortcode).first()
	return post
	
def getbytitle(post_title):
	post=session.query(Posts).filter_by(title=post_title).first()
	return post
	
@app.errorhandler(500)
def pageNotFound(error):
	print(error)
	return "500: "+str(error)
	
@app.route('/')
def display_index():
	posts=session.query(Posts).limit(100).all()
	return render_template('show_posts.html',posts=posts)
	
@app.route('/post/<int:post_id>')
@app.route('/id/<int:post_id>')
def show_id(post_id):
	post=getbyid(post_id)
	return display_post(post)

@app.route('/post/<string:post_shortcode>')
@app.route('/shortcode/<string:post_shortcode>')
def show_shortcode(post_shortcode):
	post=getbyshortcode(post_shortcode)
	return display_post(post)

@app.route('/title/<string:post_title>')
def show_title(post_title):
	post=getbytitle(post_title)
	return display_post(post)

def display_post(post):
	post.soulsphere = get_soulsphere(post.shortcode)
	post.redditwiki = get_redditwiki(post.title)
	post.length = get_length(post.content)
	post.unhex = unhex(post.content)
	post.unb64 = unb64(post.unhex)
	post.unb64_utf8 = unb64codec(post.unb64, 'utf-8')
	#post.unb64_utf8_ascii = utf2ascii(post.unb64_utf8)
	post.unb64_utf8_unhex = unhex(post.unb64_utf8)
	post.b64 = b64(post.content)
	md5a858 = "34a14a42e98ff96095af56604e290cae"
	md5a858des3 = des3decrypt(post.content,md5a858)
	md5a858des3cbc = des3decryptcbc(post.content,md5a858,"0000000000000000")
	post.md5a858des3 = md5a858des3
	post.md5a858des3_utf8 = unb64codec(md5a858des3,'utf-8')
	try:
		post.md5a858des3cbc = str(md5a858des3cbc,encoding='utf-8',errors='replace')
	except:
		post.md5a858des3cbc = md5a858des3cbc
		pass
	return render_template('show_one_post.html',post=post)

if __name__ == '__main__':
    app.run(host='0.0.0.0')