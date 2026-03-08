# Technical Skills Database - Kaggle Standard Format
TECHNICAL_SKILLS = {
    'programming_languages': [
        'Python', 'Java', 'C++', 'C#', 'JavaScript', 'TypeScript',
        'PHP', 'Ruby', 'Go', 'Rust', 'Kotlin', 'Swift', 'R', 'MATLAB',
        'VB.NET', 'Scala', 'Perl', 'Groovy', 'Haskell', 'Elixir',
        'C', 'Objective-C', 'Shell', 'Bash', 'PowerShell', 'Lua',
        'Clojure', 'Scheme', 'Jython'
    ],
    'web_technologies': [
        'HTML', 'CSS', 'React', 'Angular', 'Vue.js', 'Node.js',
        'Express', 'Django', 'Flask', 'FastAPI', 'Spring Boot',
        'ASP.NET', 'Laravel', 'Ruby on Rails', 'Webpack', 'REST API',
        'GraphQL', 'AJAX', 'Bootstrap', 'Material UI', 'Tailwind CSS',
        'Next.js', 'Nuxt', 'Ember', 'Svelte', 'MEAN Stack', 'MERN Stack',
        'Responsive Design', 'Sass', 'Less', 'jQuery', 'CORS', 'SOAP'
    ],
    'database': [
        'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Oracle', 'Redis',
        'Cassandra', 'DynamoDB', 'SQLite', 'Elasticsearch', 'Neo4j',
        'Firebase', 'Memcached', 'CouchDB', 'Hbase', 'MariaDB',
        'DB2', 'Sybase', 'Solr', 'InfluxDB', 'Graph Database',
        'Database Design', 'Data Modeling', 'Query Optimization'
    ],
    'machine_learning': [
        'Machine Learning', 'Deep Learning', 'TensorFlow', 'Keras',
        'PyTorch', 'Scikit-learn', 'XGBoost', 'LightGBM', 'Neural Networks',
        'NLP', 'Computer Vision', 'Reinforcement Learning', 'LSTM',
        'CNN', 'RNN', 'Transformers', 'BERT', 'GPT', 'Regression',
        'Classification', 'Clustering', 'Ensemble Methods', 'Feature Engineering',
        'Hyperparameter Tuning', 'Model Evaluation', 'Time Series Forecasting',
        'Anomaly Detection', 'Sentiment Analysis', 'Recommendation Systems',
        'GAN', 'Autoencoders', 'Dimensionality Reduction'
    ],
    'data_science': [
        'Data Analysis', 'Data Visualization', 'Pandas', 'NumPy',
        'Matplotlib', 'Seaborn', 'Plotly', 'Tableau', 'Power BI',
        'Statistics', 'Probability', 'A/B Testing', 'Data Mining', 'ETL',
        'Hypothesis Testing', 'Correlation Analysis', 'Regression Analysis',
        'Data Storytelling', 'Business Analytics', 'Jupyter Notebook',
        'SAS', 'SPSS', 'Ggplot2', 'D3.js', 'Qlik View'
    ],
    'cloud_platforms': [
        'AWS', 'Azure', 'Google Cloud', 'GCP', 'Kubernetes', 'Docker',
        'EC2', 'S3', 'Lambda', 'RDS', 'SQS', 'SNS', 'CloudFront',
        'Azure DevOps', 'Azure Functions', 'App Service', 'Cloud Storage',
        'Google Cloud Storage', 'Compute Engine', 'Cloud Functions',
        'Cloud Dataflow', 'BigQuery', 'Heroku', 'DigitalOcean'
    ],
    'big_data': [
        'Spark', 'Hadoop', 'Hive', 'Pig', 'MapReduce', 'Kafka',
        'Flink', 'Big Data', 'Scala', 'HDFS', 'Yarn', 'Zookeeper',
        'Flume', 'Sqoop', 'Oozie', 'HBase', 'Impala', 'Presto',
        'Data Warehouse', 'Data Lake', 'Stream Processing'
    ],
    'devops': [
        'DevOps', 'CI/CD', 'Jenkins', 'Git', 'GitHub', 'GitLab',
        'Docker', 'Kubernetes', 'Linux', 'Terraform', 'Ansible',
        'Puppet', 'Chef', 'Saltstack', 'CircleCI', 'TravisCI',
        'GitHub Actions', 'GitLab CI', 'Prometheus', 'Grafana',
        'ELK Stack', 'Splunk', 'CloudWatch', 'New Relic', 'Datadog',
        'Nginx', 'Apache', 'IaC', 'Infrastructure as Code'
    ],
    'soft_skills': [
        'Communication', 'Leadership', 'Team Work', 'Problem Solving',
        'Critical Thinking', 'Project Management', 'Agile', 'Scrum',
        'Kanban', 'Mentoring', 'Presentation', 'Documentation',
        'Cross-functional Collaboration', 'Attention to Detail',
        'Time Management', 'Adaptability', 'Creativity', 'Innovation'
    ],
    'additional_tools': [
        'Git', 'SVN', 'Jira', 'Confluence', 'Slack', 'VS Code',
        'IntelliJ', 'Visual Studio', 'Sublime Text', 'Atom',
        'Postman', 'Insomnia', 'DBeaver', 'MySQL Workbench',
        'PgAdmin', 'Vim', 'Emacs', 'SSH', 'Putty', 'WinSCP',
        'Tmux', 'Screen', 'Debugger', 'Profiler', 'Load Testing'
    ]
}

def get_all_skills():
    """Get all skills as a flat list"""
    all_skills = []
    for category, skills in TECHNICAL_SKILLS.items():
        all_skills.extend(skills)
    return all_skills

def get_skills_by_category(category):
    """Get skills by category"""
    return TECHNICAL_SKILLS.get(category, [])

def get_skill_categories():
    """Get list of all skill categories"""
    return list(TECHNICAL_SKILLS.keys())

def get_skills_count():
    """Get total number of skills"""
    return len(get_all_skills())

def is_skill_in_database(skill):
    """Check if a skill exists in the database"""
    return skill in get_all_skills()

def get_category_for_skill(skill):
    """Get the category for a specific skill"""
    for category, skills in TECHNICAL_SKILLS.items():
        if skill in skills:
            return category
    return None
