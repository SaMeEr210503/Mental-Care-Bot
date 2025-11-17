# Quick Start Guide

Get the Mental Health Support System up and running in minutes!

## Prerequisites Check

- [ ] Python 3.8+ installed (`python --version`)
- [ ] Node.js 16+ installed (`node --version`)
- [ ] npm installed (`npm --version`)
- [ ] Webcam available
- [ ] (Optional) OpenAI API key for GPT responses

## Step 1: Backend Setup (5 minutes)

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. **Install dependencies:**
   ```bash
   pip install -r ../requirements.txt
   ```

5. **(Optional) Set up environment variables:**
   Create a `.env` file in the `backend` directory:
   ```
   OPENAI_API_KEY=your_key_here
   MONGODB_URI=mongodb://localhost:27017/
   ```

6. **Start the backend server:**
   ```bash
   python app.py
   ```

   You should see:
   ```
   Starting Mental Health Support System...
   Backend server running on http://localhost:5000
   ```

## Step 2: Frontend Setup (3 minutes)

1. **Open a new terminal and navigate to frontend:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

   The browser should automatically open to `http://localhost:3000`

## Step 3: First Use

1. **Allow camera access** when prompted by your browser
2. **Click "Start Camera"** to begin emotion detection
3. **Type a message** in the chat interface to start a conversation
4. **Switch to "Emotion Dashboard"** tab to see analytics

## Troubleshooting

### Camera Not Working
- Check browser permissions (Chrome: Settings > Privacy > Camera)
- Ensure no other app is using the camera
- Try refreshing the page

### Backend Won't Start
- Make sure port 5000 is not in use
- Check that all dependencies installed correctly
- Verify Python version is 3.8+

### Frontend Won't Start
- Make sure port 3000 is not in use
- Delete `node_modules` and run `npm install` again
- Check Node.js version is 16+

### Emotion Detection Not Working
- Ensure good lighting
- Face the camera directly
- Check that FER library installed correctly (may take time on first run)

### No GPT Responses
- If OpenAI API key not set, the system uses rule-based responses
- Check API key is correct in `.env` file
- Verify you have API credits

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [CHAT_EXAMPLES.md](CHAT_EXAMPLES.md) for example conversations
- Review [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for architecture details

## Production Deployment

1. **Build the frontend:**
   ```bash
   cd frontend
   npm run build
   ```

2. **Set environment variables:**
   ```bash
   export FLASK_ENV=production
   export FLASK_DEBUG=False
   ```

3. **Run with production server:**
   ```bash
   cd backend
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

## Support

For issues or questions:
- Check the troubleshooting section above
- Review error messages in browser console (F12) and terminal
- Ensure all dependencies are up to date

