
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from openai import OpenAI
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///widgetx.db'
db = SQLAlchemy(app)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class Website(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/train', methods=['POST'])
def train():
    url = request.form['url']
    website = Website.query.filter_by(url=url).first()
    if not website:
        website = Website(url=url)
        db.session.add(website)
        db.session.commit()
    
    # Here you would typically scrape the website content
    # For simplicity, we'll just use the URL as content
    website.content = f"This is the content for {url}"
    db.session.commit()

    return jsonify({"message": "Website trained successfully"})

@app.route('/chat', methods=['POST'])
def chat():
    message = request.json['message']
    website_id = request.json['website_id']
    
    website = Website.query.get(website_id)
    if not website:
        return jsonify({"error": "Website not found"}), 404

    prompt = f"Website content: {website.content}\n\nUser: {message}\nAI:"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for the website."},
            {"role": "user", "content": prompt}
        ]
    )

    ai_message = response.choices[0].message.content.strip()
    return jsonify({"reply": ai_message})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
