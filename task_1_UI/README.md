# Moptimizer

## To run the UI
1. Open the directory `task_1_UI/project`
2. IDE: VSCode
3. In the terminal, run:
   ```bash
   npm i
   npm run dev
4. After running npm run dev, a URL will appear in the  terminal. Copy this URL and open it in your browser to access the UI.

## To run the server
1. Open the directory `task_1_UI/server`
2. In the terminal, run:
   ```bash
   npm i
   npm start
3. The server will start and listen for requests from the UI.

## .env file (required)

Before running the server, you must create a `.env` file in the root directory of the project.  
This file should contain the following environment variables:

PORT=5000
SECRET_KEY=your-secret-hash

### Explanation
- **PORT** – The port where the server will run (default: `5000`).  
- **SECRET_KEY** – A secret hash string used for encryption/signatures. Make sure to set a strong, secure value.  

### Connecting to the server
Once the `.env` file is created and the server is running, you can connect at:  
http://localhost:<PORT>
where `<PORT>` is the value you defined in the `.env` file.
  
