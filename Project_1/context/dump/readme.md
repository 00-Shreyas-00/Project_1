# Running the Shopping Query Agent

## Standard Startup
To start the FastAPI server, follow these steps:
1. Open a terminal in `shopping-query-agent/`.
2. Activate the virtual environment: `venv\Scripts\activate`
3. Run: `python -m uvicorn app.main:app --reload`

## Troubleshooting: WinError 10013
If you see the error `[WinError 10013] An attempt was made to access a socket in a way forbidden by its access permissions`, it means the port (default 8000) is ALREADY in use.

### Solutions:
1. **Stop the existing server**: Look for another terminal window where `uvicorn` is already running and stop it with `Ctrl+C`.
2. **Use a different port**: Run the server on a custom port, for example 8001:
   ```bash
   python -m uvicorn app.main:app --reload --port 8001
   ```

## API Access
Once started, you can visit:
- **Health Check**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
- **Interactive Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Search Endpoint**: `POST http://127.0.0.1:8000/api/v1/search`
  - Payload: `{"query": "Blue jeans under $50"}`
