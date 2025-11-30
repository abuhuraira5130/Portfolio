# Deployment Guide

## Local Development

### Prerequisites
- Node.js 18+ installed
- npm or yarn package manager

### Setup

1. **Clone the repository**
   \`\`\`bash
   git clone https://github.com/yourusername/portfolio.git
   cd portfolio
   \`\`\`

2. **Install dependencies**
   \`\`\`bash
   npm install
   \`\`\`

3. **Run development server**
   \`\`\`bash
   npm run dev
   \`\`\`

4. **Open in browser**
   Navigate to `http://localhost:3000`

## Production Build

### Build for production
\`\`\`bash
npm run build
npm start
\`\`\`

## Deployment to Vercel

### Option 1: Using Vercel CLI
\`\`\`bash
npm i -g vercel
vercel
\`\`\`

### Option 2: GitHub Integration
1. Push code to GitHub
2. Connect repository to Vercel dashboard
3. Vercel automatically deploys on push

### Environment Variables
No environment variables required for local development. For production, ensure:
- `NEXT_PUBLIC_API_URL` is set if using backend API

## Performance Optimization

- Images are optimized with Next.js Image component
- Animations use GPU acceleration (transform, opacity)
- Code splitting enabled by default
- Lazy loading for images and components

## Troubleshooting

### Port 3000 already in use
\`\`\`bash
npm run dev -- -p 3001
\`\`\`

### Clear cache and reinstall
\`\`\`bash
rm -rf node_modules .next
npm install
npm run dev
\`\`\`

### Build errors
\`\`\`bash
npm run lint
npm run build
