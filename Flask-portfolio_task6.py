from flask import Flask, request, render_template_string, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Your portfolio information - Edit this section with your details
PORTFOLIO = {
    'name': 'Naman Jain',
    'title': 'Web Developer',
    'email': 'naman2505jain@gmail.com',
    'phone': '+91 98765 43210',
    'github': 'https://github.com/JainNaman5',
    'linkedin': 'https://www.linkedin.com/in/naman-jain-0182505n/',
    'bio': 'I am a passionate web developer with experience in building modern web applications.',
    
    'skills': ['Python', 'Flask', 'HTML', 'CSS', 'JavaScript', 'React', 'Git'],
    
    'projects': [
        {
            'name': 'Web scrapper',
            'description': 'A web scraper built with Python and BeautifulSoup',
            'tech': 'Python, BeautifulSoup, HTML',
            'link': 'https://github.com/JainNaman5/Intership_2025_python'
        }
    ]
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ portfolio.name }} - Portfolio</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f4f4f4;
        }

        .container {
            max-width: 1100px;
            margin: 0 auto;
            padding: 0 20px;
        }

        /* Header */
        header {
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 2rem 0;
        }

        header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }

        header p {
            font-size: 1.2rem;
            margin-bottom: 1rem;
        }

        .contact-info {
            margin-top: 1rem;
        }

        .contact-info a {
            color: #3498db;
            text-decoration: none;
            margin: 0 15px;
        }

        .contact-info a:hover {
            text-decoration: underline;
        }

        /* Sections */
        .section {
            background: white;
            margin: 2rem 0;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .section h2 {
            color: #2c3e50;
            margin-bottom: 1rem;
            border-bottom: 2px solid #3498db;
            padding-bottom: 0.5rem;
        }

        /* About */
        .about p {
            font-size: 1.1rem;
            line-height: 1.8;
        }

        /* Skills */
        .skills-list {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 1rem;
        }

        .skill {
            background: #3498db;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
        }

        /* Projects */
        .project {
            border: 1px solid #ddd;
            padding: 1.5rem;
            margin: 1rem 0;
            border-radius: 5px;
            background: #f9f9f9;
        }

        .project h3 {
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }

        .project p {
            margin-bottom: 0.5rem;
        }

        .project .tech {
            color: #666;
            font-style: italic;
            font-size: 0.9rem;
        }

        .project a {
            color: #3498db;
            text-decoration: none;
            font-weight: bold;
        }

        .project a:hover {
            text-decoration: underline;
        }

        /* Contact Form */
        .contact-form {
            max-width: 600px;
            margin: 0 auto;
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: bold;
        }

        .form-group input,
        .form-group textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 1rem;
        }

        .form-group textarea {
            height: 120px;
            resize: vertical;
        }

        .btn {
            background: #3498db;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1rem;
            width: 100%;
        }

        .btn:hover {
            background: #2980b9;
        }

        /* Alert Messages */
        .alert {
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
        }

        .alert-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .alert-error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        /* Footer */
        footer {
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 1rem 0;
            margin-top: 2rem;
        }

        /* Responsive */
        @media (max-width: 768px) {
            header h1 {
                font-size: 2rem;
            }
            
            .contact-info a {
                display: block;
                margin: 5px 0;
            }
            
            .skills-list {
                justify-content: center;
            }
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header>
        <div class="container">
            <h1>{{ portfolio.name }}</h1>
            <p>{{ portfolio.title }}</p>
            <div class="contact-info">
                <a href="mailto:{{ portfolio.email }}">{{ portfolio.email }}</a>
                <a href="tel:{{ portfolio.phone }}">{{ portfolio.phone }}</a>
                <a href="{{ portfolio.github }}" target="_blank">GitHub</a>
                <a href="{{ portfolio.linkedin }}" target="_blank">LinkedIn</a>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="container">
        <!-- About Section -->
        <section class="section about">
            <h2>About Me</h2>
            <p>{{ portfolio.bio }}</p>
        </section>

        <!-- Skills Section -->
        <section class="section">
            <h2>Skills</h2>
            <div class="skills-list">
                {% for skill in portfolio.skills %}
                    <span class="skill">{{ skill }}</span>
                {% endfor %}
            </div>
        </section>

        <!-- Projects Section -->
        <section class="section">
            <h2>Projects</h2>
            {% for project in portfolio.projects %}
                <div class="project">
                    <h3>{{ project.name }}</h3>
                    <p>{{ project.description }}</p>
                    <p class="tech">Technologies: {{ project.tech }}</p>
                    <p><a href="{{ project.link }}" target="_blank">View Project</a></p>
                </div>
            {% endfor %}
        </section>

        <!-- Contact Section -->
        <section class="section">
            <h2>Contact Me</h2>
            
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ category }}">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            
            <form class="contact-form" method="POST" action="/contact">
                <div class="form-group">
                    <label for="name">Name:</label>
                    <input type="text" id="name" name="name" required>
                </div>
                
                <div class="form-group">
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="email" required>
                </div>
                
                <div class="form-group">
                    <label for="message">Message:</label>
                    <textarea id="message" name="message" required></textarea>
                </div>
                
                <button type="submit" class="btn">Send Message</button>
            </form>
        </section>
    </main>

    <!-- Footer -->
    <footer>
        <div class="container">
            <p>&copy; 2025 {{ portfolio.name }}. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, portfolio=PORTFOLIO)

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    message = request.form.get('message', '').strip()
    
    # Simple validation
    if not name or not email or not message:
        flash('All fields are required!', 'error')
        return redirect(url_for('home'))
    
    # Save message to file
    try:
        with open('messages.txt', 'a', encoding='utf-8') as f:
            f.write(f"Name: {name}\nEmail: {email}\nMessage: {message}\n{'-'*30}\n")
        
        flash('Thank you! Your message has been sent.', 'success')
    except:
        flash('Sorry, there was an error. Please try again.', 'error')
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    print("Portfolio website running at: http://127.0.0.1:5000")
    app.run(debug=True)