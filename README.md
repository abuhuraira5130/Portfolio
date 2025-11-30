# Abu Huraira - AI Developer Portfolio

A production-ready, full-stack portfolio website showcasing AI, blockchain, and full-stack development projects. This repository contains both the Next.js frontend and Django REST API backend.

## Project Structure

```
myportfolio/
├── frontend/           # Next.js 15 application
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── public/
│   └── package.json
├── backend/            # Django REST API
│   ├── config/         # Django project (settings, urls, wsgi, asgi)
│   ├── portfolio/      # Django app
│   ├── store/          # Django app
│   ├── static/
│   ├── manage.py
│   ├── requirements.txt
│   └── .env            # Backend environment (not committed)
├── .env.example        # Environment variables template
├── railway.json        # Railway deployment config (backend service)
└── README.md
```

## Features

- **Modern Design**: Responsive, dark/light mode, smooth animations
- **SEO Optimized**: Meta tags, structured data, sitemap
- **Performance**: Image optimization, lazy loading, code splitting
- **Accessibility**: ARIA labels, keyboard navigation, color contrast
- **Backend Integration**: Django REST API for dynamic content
- **Analytics**: Vercel Analytics and Google Analytics
- **Contact Form**: Email notifications with validation
- **Admin Dashboard**: Manage projects and content (optional)

## Tech Stack

### Frontend
- Next.js 15 (App Router)
- TypeScript
- Tailwind CSS
- Framer Motion (animations)
- Lucide React (icons)

### Backend
- Django REST Framework
- MySQL/PostgreSQL
- JWT Authentication
- WhiteNoise for static files
- Gunicorn for production

### Deployment
- Frontend: Vercel, Railway, or any static host
- Backend: Railway, Render, or DigitalOcean

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.9+
- MySQL or PostgreSQL
- pip and npm/pnpm

### Installation

1. Clone the repository
\`\`\`bash
git clone https://github.com/yourusername/portfolio.git
cd portfolio
\`\`\`

2. Set up environment variables
\`\`\`bash
cp .env.example .env
# Edit .env with your configuration
\`\`\`

3. **Frontend Setup**
\`\`\`bash
cd frontend
npm install
npm run dev
# Opens on http://localhost:3000
\`\`\`

4. **Backend Setup** (in a separate terminal)
\`\`\`bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
# API running on http://localhost:8000
\`\`\`

\`\`\`bash
npm install
\`\`\`

3. Set up environment variables
\`\`\`bash
cp .env.local.example .env.local
# Edit .env.local with your configuration
\`\`\`

4. Run development server
\`\`\`bash
npm run dev
\`\`\`

5. Open [http://localhost:3000](http://localhost:3000)

## API Endpoints

### Contact Form
- **POST** `/api/contact` - Submit contact form

### Projects
- **GET** `/api/projects` - Fetch all projects
- **POST** `/api/projects` - Create project (admin)
- **PUT** `/api/projects/:id` - Update project (admin)
- **DELETE** `/api/projects/:id` - Delete project (admin)

### Skills
- **GET** `/api/skills` - Fetch all skills

## Deployment

### Railway (Recommended for Combined Stack)

Railway makes it easy to deploy both services from a single repo.

**Prerequisites:**
- Railway account (free tier available)
- GitHub repo connected to Railway

**Setup:**

1. **Create two services on Railway**
   - Service 1: Backend (Django)
   - Service 2: Frontend (Next.js)

2. **Configure Backend Service**
   - **Build Command:** `pip install -r backend/requirements.txt && python backend/manage.py collectstatic --noinput`
   - **Start Command:** `cd backend && gunicorn config.wsgi --bind 0.0.0.0:$PORT --workers 3 --log-file -`
   - **Environment Variables:**
     ```
     SECRET_KEY=your-secret-key-here
     DEBUG=false
     ALLOWED_HOSTS=*.railway.app
     DATABASE_URL=<Railway MySQL/Postgres URL>
     CORS_ALLOWED_ORIGINS=https://your-frontend-url.railway.app
     ```

3. **Configure Frontend Service**
   - **Build Command:** `cd frontend && npm ci && npm run build`
   - **Start Command:** `cd frontend && npm start`
   - **Environment Variables:**
     ```
     NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
     ```

4. **Deploy**
   - Push to GitHub
   - Railway will automatically detect changes and redeploy

### Vercel (Frontend Only)

If you prefer to host the frontend on Vercel:

1. Push to GitHub
2. Connect repository to Vercel
3. Set **Root Directory** to `frontend`
4. Set environment variables (e.g., `NEXT_PUBLIC_API_URL`)
5. Deploy

### Render/DigitalOcean (Backend Only)

For hosting the backend separately:

1. Connect GitHub repository
3. Set **Build Command:** `pip install -r backend/requirements.txt && python backend/manage.py migrate && python backend/manage.py collectstatic --noinput`
4. Set **Start Command:** `cd backend && gunicorn config.wsgi --bind 0.0.0.0:$PORT --workers 3 --log-file -`
5. Set environment variables from `.env.example`
5. Deploy

## Environment Variables

Create a `.env` file in the project root (or in `backend/` and `frontend/`) with:

\`\`\`
# Django Backend
SECRET_KEY=your-strong-secret-key-here
DEBUG=false
ALLOWED_HOSTS=*
DB_ENGINE=mysql
DB_NAME=portfolio_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
DATABASE_URL=mysql://user:password@host:port/dbname  # Optional

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=no-reply@yourdomain.com

# Frontend (Next.js)
NEXT_PUBLIC_API_URL=http://localhost:8000

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000
\`\`\`

## Production Checklist

- [ ] Set strong `SECRET_KEY` in production
- [ ] Set `DEBUG=false`
- [ ] Configure `ALLOWED_HOSTS` for your domain
- [ ] Set up database (MySQL/PostgreSQL)
- [ ] Configure email settings
- [ ] Set `NEXT_PUBLIC_API_URL` to production backend
- [ ] Enable HTTPS/SSL
- [ ] Run `python manage.py collectstatic` before deployment
- [ ] Test both services locally before deploying

## Performance Metrics

- Lighthouse Score: 95+
- Core Web Vitals: All Green
- Page Load Time: <2s
- SEO Score: 100

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Contact

- Email: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Abu Huraira](https://linkedin.com/in/yourusername)
- Twitter: [@yourusername](https://twitter.com/yourusername)

---

Built with ❤️ by Abu Huraira
1. Create account on Render/Railway
2. Connect GitHub repository
3. Set environment variables
4. Deploy

## Environment Variables

\`\`\`
NEXT_PUBLIC_API_URL=https://api.yourportfolio.com
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
EMAIL_SERVICE_KEY=your_key
DJANGO_SECRET_KEY=your_key
DATABASE_URL=postgresql://...
\`\`\`

## Performance Metrics

- Lighthouse Score: 95+
- Core Web Vitals: All Green
- Page Load Time: <2s
- SEO Score: 100

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Contact

- Email: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Abu Huraira](https://linkedin.com/in/yourusername)
- Twitter: [@yourusername](https://twitter.com/yourusername)

---

Built with ❤️ by Abu Huraira
